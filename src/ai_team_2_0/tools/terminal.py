import subprocess
from pathlib import Path
from langchain_core.tools import tool

PROJECT_DIR = Path('./Output').resolve()

@tool
def execTerminal(command: str) -> str:
    """Run the terminal with the command"""
    result = subprocess.run(
        command,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
        shell=True
    )
    status = "SUCCESS" if result.returncode == 0 else "FAILED"
    return (
        f"STATUS: {status}\nCommand: {command}\n"
        f"stdout:\n{result.stdout or '<no stdout>'}\n"
        f"stderr:\n{result.stderr or '<no stderr>'}"
    )
