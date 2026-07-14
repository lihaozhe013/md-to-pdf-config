import platform
import sys
from pathlib import Path


def get_rc_file() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / ".zshrc"
    elif system == "Linux":
        return Path.home() / ".bashrc"
    elif system == "Windows":
        git_bash = Path("C:/Program Files/Git/bin/bash.exe")
        if git_bash.exists():
            return Path.home() / ".bashrc"
        print("Error: Git Bash not found", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Error: unsupported platform: {system}", file=sys.stderr)
        sys.exit(1)


def main():
    rc_file = get_rc_file()
    project_root = Path(__file__).resolve().parent
    venv_python = project_root / ".venv" / "bin" / "python"
    entry_script = project_root / "main.py"

    alias_name = "md2p"
    alias_line = f"alias {alias_name}='{venv_python} {entry_script}'\n"

    content = rc_file.read_text() if rc_file.exists() else ""
    if f"alias {alias_name}=" in content:
        print(f"Alias '{alias_name}' already exists in {rc_file}")
    else:
        with open(rc_file, "a") as f:
            f.write(f"\n# md-to-pdf-config\n{alias_line}")
        print(f"Added to {rc_file}")

    print(f"Run: source {rc_file}")
    print(f"Usage: {alias_name} path/to/file.md")


if __name__ == "__main__":
    main()
