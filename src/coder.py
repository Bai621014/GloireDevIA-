"""Module "coder" — Auto‑Coder minimal pour GloireDevIA

Objectifs :
- Parcourir les fichiers Python dans src/
- Analyser la structure des fonctions (AST) et détecter issues simples
  (fonctions très longues, complexité heuristique élevée, arguments sans annotations,
   usage de mutable defaults, TODO/FIXME, bare excepts, prints de debug)
- Produire suggestions et snippets de correction sous forme JSON (ne JAMAIS exécuter
  automatiquement le code généré)
- Fournir generate_update(problem: str, targets: list[str]|None) -> dict
  qui retourne un objet structuré contenant :
    - rationale : pourquoi la modification
    - patches : liste de {path, start_line, end_line, original, suggestion}

Règles de sécurité :
- Le module ne modifie jamais le code directement.
- generate_update retourne toujours des patches/textes — c'est à l'opérateur humain
  de valider et d'appliquer.

Note : Ce module est volontairement heuristique et conservateur. Il vise l'autonomie
initiale du projet lorsque des outils externes manquent.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SRC_DIR = Path(__file__).resolve().parent


def list_python_files(base: Path = SRC_DIR) -> List[Path]:
    """Retourne la liste des fichiers .py sous src/ (exclut venv et .git)."""
    files = [p for p in base.rglob("*.py") if "site-packages" not in str(p) and ".git" not in str(p)]
    return sorted(files)


class FunctionInfo:
    def __init__(self, name: str, start: int, end: int, lineno: int, args: List[str], has_type_hints: bool,
                 mutable_defaults: List[str], complexity: int, docstring: Optional[str]):
        self.name = name
        self.start = start
        self.end = end
        self.lineno = lineno
        self.args = args
        self.has_type_hints = has_type_hints
        self.mutable_defaults = mutable_defaults
        self.complexity = complexity
        self.docstring = docstring

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "lineno": self.lineno,
            "args": self.args,
            "has_type_hints": self.has_type_hints,
            "mutable_defaults": self.mutable_defaults,
            "complexity": self.complexity,
            "docstring_present": bool(self.docstring),
        }


def _heuristic_complexity(node: ast.AST) -> int:
    """Estime une complexité cyclomatique basique en comptant certains noeuds.
    Cette estimation n'est pas parfaite mais utile pour détecter les fonctions
    potentiellement compliquées.
    """
    score = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.AsyncFor, ast.AsyncWith)):
            score += 1
        if isinstance(child, ast.BoolOp):
            score += len(child.values) - 1
        if isinstance(child, ast.IfExp):
            score += 1
        if isinstance(child, (ast.Assert, ast.Raise)):
            score += 0  # pas pénalisant
    return score + 1  # +1 baseline


def analyze_file(path: Path) -> Dict[str, Any]:
    """Analyse statique d'un fichier : extrait fonctions et issues simples."""
    text = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as e:
        return {"path": str(path), "error": f"SyntaxError: {e}"}

    functions: List[FunctionInfo] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = getattr(node, "lineno", 0)
            # end lineno estimation : last child's lineno or same
            end = start
            for n in ast.walk(node):
                if hasattr(n, "lineno"):
                    end = max(end, getattr(n, "lineno"))

            args = [arg.arg for arg in node.args.args]
            # check type hints presence
            has_hints = any(arg.annotation is not None for arg in node.args.args) or (node.returns is not None)

            # mutable default args
            mutable_defaults = []
            defaults = node.args.defaults or []
            # align defaults to last args
            if defaults:
                offset = len(node.args.args) - len(defaults)
                for i, defnode in enumerate(defaults):
                    argname = node.args.args[offset + i].arg
                    if isinstance(defnode, (ast.List, ast.Dict, ast.Set, ast.Call)):
                        # list/dict/set literal or a call (possible factory) -> flag
                        mutable_defaults.append(argname)

            complexity = _heuristic_complexity(node)
            doc = ast.get_docstring(node)
            functions.append(FunctionInfo(node.name, start, end, node.lineno, args, has_hints, mutable_defaults, complexity, doc))

    issues: List[Dict[str, Any]] = []

    # heuristics: long functions, high complexity, missing type hints, TODOs, bare except, print statements
    for func in functions:
        length = func.end - func.start + 1
        if length > 80:
            issues.append({"type": "long_function", "severity": "warning", "message": f"Function {func.name} is long ({length} lines). Consider splitting.", "function": func.to_dict()})
        if func.complexity > 12:
            issues.append({"type": "high_complexity", "severity": "warning", "message": f"Function {func.name} has estimated complexity {func.complexity}.", "function": func.to_dict()})
        if not func.has_type_hints:
            issues.append({"type": "missing_type_hints", "severity": "info", "message": f"Function {func.name} has no type hints.", "function": func.to_dict()})
        if func.mutable_defaults:
            issues.append({"type": "mutable_default_args", "severity": "warning", "message": f"Function {func.name} has mutable default args: {func.mutable_defaults}.", "function": func.to_dict()})

    # file-level scans: TODO/FIXME, bare except, print usage
    file_issues = []
    for n in ast.walk(tree):
        if isinstance(n, ast.ExceptHandler):
            if n.type is None:
                file_issues.append({"type": "bare_except", "lineno": getattr(n, "lineno", None), "message": "bare except detected"})
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
            file_issues.append({"type": "print_debug", "lineno": getattr(n, "lineno", None), "message": "print() used (debug)"})

    # TODO/FIXME in raw text
    for i, line in enumerate(text.splitlines(), start=1):
        if "TODO" in line or "FIXME" in line:
            file_issues.append({"type": "todo", "lineno": i, "message": line.strip()})

    return {
        "path": str(path),
        "functions": [f.to_dict() for f in functions],
        "issues": issues,
        "file_issues": file_issues,
    }


def analyze_repo(base: Path = SRC_DIR) -> Dict[str, Any]:
    """Analyse l'ensemble des fichiers sous src/ et retourne un rapport consolidé."""
    files = list_python_files(base)
    report = {"files": []}
    for f in files:
        report["files"].append(analyze_file(f))
    return report


def _extract_original_snippet(path: Path, start: int, end: int) -> str:
    src = path.read_text(encoding="utf-8").splitlines()
    # lines are 1-indexed
    return "\n".join(src[start - 1 : end])


def _suggest_fix_for_issue(file_path: Path, issue: Dict[str, Any]) -> Dict[str, Any]:
    """Génère une suggestion minimale (texte) pour un issue donné.

    Retourne un dict contenant : path, start, end, original, suggestion, rationale
    """
    itype = issue.get("type")

    if itype == "long_function":
        func = issue["function"]
        start, end = func["start"], func["end"]
        original = _extract_original_snippet(file_path, start, end)
        # Suggest splitting: provide a scaffold for helper extraction
        suggestion = (
            f"# Suggestion: extraire des sous-fonctions pour réduire la longueur.\n"
            f"def {func['name']}_part1(...):\n    # TODO: extraire la première responsabilité\n    pass\n\n"
            f"def {func['name']}_part2(...):\n    # TODO: extraire la seconde responsabilité\n    pass\n\n"
            f"# Réécrire {func['name']} en appelant les helpers ci‑dessus.\n"
        )
        rationale = "Function is long — splitting improves readability and testability." 
        return {"path": str(file_path), "start": start, "end": end, "original": original, "suggestion": suggestion, "rationale": rationale}

    if itype == "high_complexity":
        func = issue["function"]
        start, end = func["start"], func["end"]
        original = _extract_original_snippet(file_path, start, end)
        suggestion = (
            f"# Suggestion: réduire la complexité en isolant les branches complexes et en utilisant des guard clauses.\n"
            f"# Exemple (scaffold) :\n"
            f"def {func['name']}_simplified(...):\n    # 1) Valider les préconditions\n    # 2) Extraire les sous-cas en helpers\n    # 3) Retourner le résultat consolidé\n    pass\n"
        )
        rationale = "High complexity detected — simplify control flow and extract helpers." 
        return {"path": str(file_path), "start": start, "end": end, "original": original, "suggestion": suggestion, "rationale": rationale}

    if itype == "missing_type_hints":
        func = issue["function"]
        start, end = func["start"], func["end"]
        original = _extract_original_snippet(file_path, start, end)
        # basic annotation scaffold using typing.Any
        args = func["args"]
        args_sig = ", ".join(f"{a}: Any" for a in args)
        suggestion = (
            "from typing import Any\n\n"
            f"# Suggestion: ajouter des annotations (Any si incertain) pour améliorer la lisibilité et le typage\n"
            f"def {func['name']}({args_sig}) -> Any:\n    # TODO: remplacer Any par des types précis\n    pass\n"
        )
        rationale = "Add type hints to improve static analysis and readability." 
        return {"path": str(file_path), "start": start, "end": end, "original": original, "suggestion": suggestion, "rationale": rationale}

    if itype == "mutable_default_args":
        func = issue["function"]
        start, end = func["start"], func["end"]
        original = _extract_original_snippet(file_path, start, end)
        margs = func["mutable_defaults"]
        # Provide pattern to replace mutable defaults with None and factory
        replace_lines = []
        for a in margs:
            replace_lines.append(f"    if {a} is None:\n        {a} = []  # or appropriate factory\n")
        suggestion = (
            f"# Suggestion: éviter les mutable default args (utiliser None + factory)\n"
            f"def {func['name']}(..., {', '.join(margs)}=None):\n"
            + "".join(replace_lines)
            + "    # ... reste de la fonction\n"
        )
        rationale = "Mutable default args can lead to shared state across calls." 
        return {"path": str(file_path), "start": start, "end": end, "original": original, "suggestion": suggestion, "rationale": rationale}

    # generic fallback
    return {"path": str(file_path), "start": issue.get("lineno"), "end": issue.get("lineno"), "original": "", "suggestion": "# No automated suggestion available for this issue.", "rationale": "manual review required"}


def generate_patch_from_report(report: Dict[str, Any], max_patches: int = 5) -> List[Dict[str, Any]]:
    """Transforme un rapport d'analyse en une liste de patches/suggestions.

    Limite le nombre de patches pour éviter des propositions trop massives.
    """
    patches: List[Dict[str, Any]] = []
    for file_report in report.get("files", []):
        path = Path(file_report["path"])
        for issue in file_report.get("issues", [])[:max_patches]:
            patch = _suggest_fix_for_issue(path, issue)
            patches.append(patch)
            if len(patches) >= max_patches:
                return patches
        # include file-level issues too
        for file_issue in file_report.get("file_issues", [])[:max_patches]:
            # simple suggestion for file-level problems
            lineno = file_issue.get("lineno") or 1
            original = _extract_original_snippet(path, lineno, lineno)
            suggestion = "# Manual review recommended for this site\n"
            patches.append({"path": str(path), "start": lineno, "end": lineno, "original": original, "suggestion": suggestion, "rationale": file_issue.get("message")})
            if len(patches) >= max_patches:
                return patches
    return patches


def generate_update(problem: str, targets: Optional[List[str]] = None) -> Dict[str, Any]:
    """Point d'entrée : génère des propositions de correction correspondant au 'problem'.

    - problem : description naturelle du problème (ex: "améliorer typing", "réduire complexité").
    - targets : liste optionnelle de chemins de fichiers à analyser (relatifs à src/). Si None, analyse tout src/.

    Retourne un dict JSON-serializable (ne pas exécuter le code produit).
    """
    # conservative default
    base = SRC_DIR
    if targets:
        files = [base / t for t in targets]
    else:
        files = list_python_files(base)

    consolidated_report = {"files": []}
    for f in files:
        try:
            consolidated_report["files"].append(analyze_file(f))
        except Exception as e:
            consolidated_report["files"].append({"path": str(f), "error": str(e)})

    # Decide which issues to propose based on problem keywords
    keywords = problem.lower()
    filtered_report = {"files": []}
    for fr in consolidated_report["files"]:
        # If analysis produced an error, pass through
        if "error" in fr:
            filtered_report["files"].append(fr)
            continue
        # filter issues matching problem
        issues = fr.get("issues", [])
        matched = []
        for issue in issues:
            itype = issue.get("type", "")
            if ("type" in issue and (keywords in itype or any(k in issue.get("message", "").lower() for k in keywords.split()))) or ("audit" in keywords):
                matched.append(issue)
            else:
                # heuristics: if problem asks for typing and issue is missing_type_hints
                if "typing" in keywords and itype == "missing_type_hints":
                    matched.append(issue)
                if "complex" in keywords and itype in ("high_complexity", "long_function"):
                    matched.append(issue)
                if "mutable" in keywords and itype == "mutable_default_args":
                    matched.append(issue)
        # always include file-level issues if audit requested
        if "audit" in keywords:
            fr_copy = {**fr}
            filtered_report["files"].append(fr_copy)
        else:
            if matched:
                fr_copy = {"path": fr["path"], "issues": matched}
                filtered_report["files"].append(fr_copy)

    # Generate patches from filtered report
    patches = generate_patch_from_report(filtered_report if filtered_report["files"] else consolidated_report)

    response = {
        "problem": problem,
        "targets": [str(p) for p in files],
        "analysis_summary": {"total_files": len(files), "patches_proposed": len(patches)},
        "patches": patches,
        "note": "Les patchs sont des suggestions heuristiques — validez manuellement avant application.",
    }

    return response


# Petit utilitaire CLI (sûr, ne modifie rien) — utile en local pour debug
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto‑Coder utility for GloireDevIA (analysis only)")
    parser.add_argument("--problem", type=str, default="audit", help="Problem to analyze (e.g. 'typing', 'complexity', 'audit')")
    parser.add_argument("--targets", type=str, nargs="*", help="Optional list of target files relative to src/")
    args = parser.parse_args()

    result = generate_update(args.problem, args.targets)
    print(json.dumps(result, indent=2, ensure_ascii=False))
