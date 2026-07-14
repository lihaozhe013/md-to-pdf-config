default: run
run:
	md-to-pdf --stylesheet github-markdown.css --body-class markdown-body name.md
format:
	prettier . --write