# md2p-gui

A Markdown-to-PDF conversion tool with beautiful styling, LaTeX math support, and both CLI and GUI interfaces. Uses [md-to-pdf](https://www.npmjs.com/package/md-to-pdf) under the hood with pre-configured CSS themes, custom fonts, and MathJax rendering.

## Features

- **CLI & GUI** — command-line batch conversion and a PySide6 drag-and-drop GUI
- **Multiple CSS themes** — `rose.css`, `kiro.css`, `github-markdown.css`
- **LaTeX math** — inline `$...$` and display `$$...$$` via MathJax
- **Mermaid diagrams** — flowcharts, sequence diagrams, Gantt charts, and more (`` ```mermaid ``)
- **Custom fonts** — JetBrains Mono Nerd Font, Inter, Noto Sans SC, Open Sans
- **Pre / post-processing** — automatic markdown fixes and PDF metadata injection
- **Configurable output** — page size, margins, headers & footers

## Prerequisites

- **Node.js** (for `md-to-pdf`)
- **Python** >= 3.13
- **uv** (Python package manager)

```bash
# Install md-to-pdf globally
npm i -g md-to-pdf

# Install Python dependencies
uv sync
```

## Usage

### CLI

```bash
# Convert a single file
uv run python main.py doc.md

# Specify output path
uv run python main.py doc.md -o output.pdf

# Recursively convert all .md files in a directory
uv run python main.py -r docs/

# View help
uv run python main.py --help
```

### Shell alias (optional)

```bash
uv run python setup_alias.py
source ~/.zshrc   # or ~/.bashrc
md2p doc.md
```

### GUI

```bash
make gui
# or
uv run python gui_main.py
```

Drag & drop a Markdown file, select a CSS theme and output options, then click convert.

## Development

```bash
# Install dev dependencies (e.g. PyInstaller)
uv sync --group dev

# Build Windows standalone executable
make build-win
```

## Credits

- `css/rose.css` — derived from [Typora's theme.typora.io](https://github.com/typora/theme.typora.io/tree/gh-pages)
- `css/github-markdown.css` — derived from [github-markdown-css](https://github.com/sindresorhus/github-markdown-css)

## Project structure

```
md-to-pdf-config/
├── main.py              # CLI entry point
├── gui_main.py          # GUI entry point
├── converter.py         # Core conversion logic
├── preprocess.py        # Markdown pre-processing
├── postprocess.py       # PDF post-processing (metadata)
├── setup_alias.py       # Shell alias installer
├── .md-to-pdf.json      # Generated md-to-pdf config
├── .md-to-pdf.json.example # Config template
├── gui/                 # PySide6 GUI components
├── css/                 # Stylesheets (rose, kiro, github-markdown)
├── fonts/               # Bundled fonts
├── js/                  # MathJax script
└── scripts/             # Build scripts
```
