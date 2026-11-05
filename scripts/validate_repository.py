"""Validate notebook syntax and packaging without executing research experiments."""

import ast
import hashlib
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    "Images_NFTs_Master.ipynb",
    "Metadata_NFTs_Master.ipynb",
    "Domains_NFT_Master.ipynb",
)


def main():
    historical_hashes = json.loads(
        (ROOT / "tests" / "historical-evidence.json").read_text(encoding="utf-8")
    )
    for name in NOTEBOOKS:
        path = ROOT / name
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for position, cell in enumerate(notebook.cells, 1):
            if cell.cell_type == "code":
                # IPython setup/magic lines are not ordinary Python statements.
                python_source = "\n".join(
                    "pass" if line.lstrip().startswith(("%", "!")) else line
                    for line in cell.source.splitlines()
                )
                ast.parse(python_source, filename=f"{name}:cell-{position}")
        raw = json.loads(path.read_text(encoding="utf-8"))
        evidence = [
            {key: value for key, value in cell.items() if key != "source"}
            for cell in raw["cells"]
        ]
        digest = hashlib.sha256(
            json.dumps(evidence, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        if digest != historical_hashes["notebooks"][name]:
            raise ValueError(f"Historical cell outputs/metadata changed: {name}")
        expected = f"https://colab.research.google.com/github/stefisha/DetectingNFTs-MasterThesis/blob/main/{name}"
        if expected not in "".join(cell.get("source", "") for cell in notebook.cells):
            raise ValueError(f"Missing current Colab link: {name}")
        code_cells = sum(cell.cell_type == "code" for cell in notebook.cells)
        print(
            f"Valid notebook: {name} ({code_cells} code cells; syntax checked; historical evidence unchanged)"
        )

    for document in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
        for target in re.findall(
            r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")
        ):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            relative_path = target.split("#", 1)[0]
            if not (document.parent / relative_path).exists():
                raise ValueError(f"Broken local link in {document.name}: {target}")

    ET.parse(ROOT / "assets" / "research-banner.svg")
    results = (ROOT / "docs" / "RESULTS.md").read_text(encoding="utf-8")
    for value in ("98.36%", "94.83%", "84.32%"):
        if value not in results:
            raise ValueError(f"Missing reported thesis result: {value}")
    print("Local documentation links, SVG, and thesis result references are valid.")
    print("Citation schema check: run cffconvert --validate separately.")


if __name__ == "__main__":
    main()
