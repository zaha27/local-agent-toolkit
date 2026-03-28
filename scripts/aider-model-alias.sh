#!/bin/bash

ALIAS_LINE='alias ai-coder="aider --model ollama/qwen2.5-coder:7b --read configs/coding-rules.md --read configs/arch-linux-context.md"'

if [[ "$SHELL" == */zsh ]]
then 
	CONF_FILE="$HOME/.zshrc"
elif [[ "$SHELL" == */bash ]]
then 
	CONF_FILE="$HOME/.bashrc"
else 
	echo "unknown shell"
	exit 1
fi

if ! grep -q "alias ai-coder=" "$CONF_FILE"
then 
	echo "" >> "$CONF_FILE"
	echo "# Local Ai Coding Agent Alias" >> "$CONF_FILE"
	echo "$ALIAS_LINE" >> "$CONF_FILE"
	echo "Alias 'ai-coder' added to $CONF_FILE"
else 
	echo "Alias 'ai-coder' already exists"
fi

echo "Please run: source $CONF_FILE"
