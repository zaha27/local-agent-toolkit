# tools/shell.py
import asyncio
import shlex
from pathlib import Path
from tools.registry import registry

BLOCKED_COMMANDS = {
    "rm -rf /", "dd if=", "mkfs", ":(){ :|:& };:",
    "chmod -R 777 /", "wget", "curl"
}

ALLOWED_COMMANDS = {
    "ls", "cat", "grep", "find", "git", "python", "pip",
    "cargo", "gcc", "make", "systemctl", "journalctl",
    "pacman", "paru", "yay", "nvtop", "htop", "df", "du"
}

@registry.register(
    name="run_shell",
    description="Execute a shell command on the Arch Linux system. Use only for safe commands.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The command to execute"
            },
            "working_dir": {
                "type": "string",
                "description": "Working directory (optional)"
            }
        },
        "required": ["command"]
    },
    requires_confirmation=False
)
async def run_shell(command: str, working_dir: str = None) -> str:
    for blocked in BLOCKED_COMMANDS:
        if blocked in command:
            return f"Blocked command: {blocked}"

    cmd_base = shlex.split(command)[0] if command.strip() else ""
    if cmd_base not in ALLOWED_COMMANDS:
        return f"Command '{cmd_base}' is not in the whitelist."

    cwd = Path(working_dir) if working_dir else Path.home()

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)

        output = stdout.decode().strip()
        errors = stderr.decode().strip()

        if proc.returncode != 0:
            return f"Exit {proc.returncode}:\n{errors or output}"
        return output or "(no output)"

    except asyncio.TimeoutError:
        proc.kill()
        return "Timeout after 30s"
    except Exception as e:
        return f"Error: {e}"