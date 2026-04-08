#Shell Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Start Ollama service
alias ai-start="sudo systemctl start ollama"

# Launch Aider with Qwen 2.5 (Fast)
alias ai-coder="aider --model ollama/qwen2.5-coder:7b"

# Launch Aider with DeepSeek (Smart/Slow)
alias ai-pro="aider --model ollama/deepseek-coder-v2:16b"

# Update all AI models
alias ai-update="ollama list | awk '{print \$1}' | xargs -I {} ollama pull {}"

# Upgrade all AI models with uv
alias ai-upgrade="uv tool upgrade aider-chat && ollama list | awk '{print \$1}' | xargs -I {} ollama pull {}"
