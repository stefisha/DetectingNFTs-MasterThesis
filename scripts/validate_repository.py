"""Validate research packaging without executing notebook cells or fetching data."""
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
    for name in NOTEBOOKS:
        path = ROOT / name
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        expected = f"https://colab.research.google.com/github/stefisha/DetectingNFTs-MasterThesis/blob/main/{name}"
        if expected not in "".join(cell.get("source", "") for cell in notebook.cells):
            raise ValueError(f"Missing current Colab link: {name}")
        code_cells = sum(cell.cell_type == "code" for cell in notebook.cells)
        print(f"Valid notebook: {name} ({code_cells} code cells; not executed)")

    for document in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
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
