import subprocess
from pathlib import Path

from langchain_core.tools import tool

PROJECT_DIR = Path('./Output').resolve()

@tool
def execTerminal(command: str) -> str:
    """Run a shell command from the repository root."""
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
            shell=True,
        )
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        return (
            f"STATUS: FAILED\nCommand timed out after 300 seconds: {command}\n"
            f"stdout:\n{stdout or '<no stdout>'}\n"
            f"stderr:\n{stderr or '<no stderr>'}"
        )

    status = "SUCCESS" if result.returncode == 0 else "FAILED"
    return (
        f"STATUS: {status}\nCommand: {command}\n"
        f"stdout:\n{result.stdout or '<no stdout>'}\n"
        f"stderr:\n{result.stderr or '<no stderr>'}"
    )
