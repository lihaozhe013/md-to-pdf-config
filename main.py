import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF with custom styles")
    parser.add_argument("file", nargs="?", help="Path to the Markdown file")
    parser.add_argument("--name", "-n", dest="name", help="Path to the Markdown file")
    parser.add_argument("--output", "-o", help="Output PDF path (default: same as input with .pdf)")
    args = parser.parse_args()

    if not shutil.which("md-to-pdf"):
        print("Error: md-to-pdf not found. Install it with: npm i -g md-to-pdf", file=sys.stderr)
        sys.exit(1)

    project_root = Path(__file__).resolve().parent
    md_path = args.name or args.file
    if not md_path:
        parser.print_usage()
        print("Error: a Markdown file is required", file=sys.stderr)
        sys.exit(1)
    md_file = Path(md_path).resolve()

    if not md_file.exists():
        print(f"Error: file not found: {md_file}", file=sys.stderr)
        sys.exit(1)

    output = args.output or str(md_file.with_suffix(".pdf"))

    cmd = [
        "md-to-pdf",
        "--stylesheet", str(project_root / "github-markdown.css"),
        "--body-class", "markdown-body",
        "--basedir", str(project_root),
        str(md_file),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    if result.stdout:
        print(result.stdout, end="")


if __name__ == "__main__":
    main()
