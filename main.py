import argparse
import sys
from pathlib import Path

from converter import (
    check_md_to_pdf,
    convert_file,
    ensure_config,
    get_project_root,
)
from i18n import _, detect_system_lang, load_language


def main():
    load_language(detect_system_lang())

    parser = argparse.ArgumentParser(description=_("Convert Markdown to PDF with custom styles"))
    parser.add_argument("file", nargs="?", help=_("Path to the Markdown file or directory"))
    parser.add_argument("--name", "-n", dest="name", help=_("Path to the Markdown file"))
    parser.add_argument("--output", "-o", help=_("Output PDF path (default: same as input with .pdf)"))
    parser.add_argument("--recursive", "-r", action="store_true",
                        help=_("Recursively convert all .md files in the given directory"))
    args = parser.parse_args()

    if not check_md_to_pdf():
        print(_("Error: md-to-pdf not found. Install it with: npm i -g md-to-pdf"), file=sys.stderr)
        sys.exit(1)

    project_root = get_project_root()
    config_file = ensure_config(project_root)

    if args.recursive:
        md_path = args.name or args.file
        if not md_path:
            parser.print_usage()
            print(_("Error: a directory path is required with -r"), file=sys.stderr)
            sys.exit(1)
        root_dir = Path(md_path).resolve()
        if not root_dir.is_dir():
            print(_("Error: not a directory: {path}").format(path=root_dir), file=sys.stderr)
            sys.exit(1)

        md_files = sorted(root_dir.rglob("*.md"))
        if not md_files:
            print(_("No .md files found in {path}").format(path=root_dir))
            return

        for md_file in md_files:
            print(_("Converting file {path}...").format(path=md_file))
            result = convert_file(md_file, project_root, config_file)
            if result.success:
                print(_("  -> {output_path}").format(output_path=result.output_path))
            else:
                print(_("  ERROR: {error}").format(error=result.error), file=sys.stderr)
    else:
        md_path = args.name or args.file
        if not md_path:
            parser.print_usage()
            print(_("Error: a Markdown file is required"), file=sys.stderr)
            sys.exit(1)
        md_file = Path(md_path).resolve()

        if not md_file.exists():
            print(_("Error: file not found: {path}").format(path=md_file), file=sys.stderr)
            sys.exit(1)

        output = args.output or str(md_file.with_suffix(".pdf"))
        result = convert_file(md_file, project_root, config_file, output)
        if result.success:
            print(_("Converted: {input_path} -> {output_path}").format(input_path=md_file, output_path=result.output_path))
        else:
            print(_("Error: {error}").format(error=result.error), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
