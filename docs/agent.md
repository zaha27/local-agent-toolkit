# CLI Agent (Aider)

Aider is the primary tool for autonomous file editing.

## Basic Usage
1. Open terminal in project root.
2. Start agent: `aider --model ollama/qwen2.5-coder:7b`
3. Commands:
   - `/add <file>` : Add file to context.
   - `/drop <file>` : Remove file from context.
   - `/undo` : Revert last AI change.
   - `/chat` : Just talk, don't edit.

## Workflow
- Ask for features: "Add a login form with validation."
- Fix bugs: Paste the error and ask "Fix this."
- Refactor: "Move this logic to a separate hook."
