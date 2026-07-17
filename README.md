# md-to-pdf-config

Markdown 转 PDF 的配置项目，使用 GitHub 风格的 CSS 和本地字体渲染。

## 依赖

- Node.js: `npm i -g md-to-pdf`
- uv `uv sync`

## GUI

```bash
make
```

### Windows 版打包单文件
```bash
make build-win
```

## CLI用法

```bash
# 直接运行
uv run python main.py 文档.md
uv run python main.py --name 文档.md
uv run python main.py -n 文档.md -o 输出.pdf

# 使用 alias（先运行 setup）
uv run python setup_alias.py
md2p 文档.md
```
