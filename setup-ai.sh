#!/bin/bash

set -e

echo "--arch ai setup--"

# Ask the user which environment they are using
read -r -p "Which environment are you on? [Arch/Debian]: " env

if [[ "$env" == "Arch" ]]; then
    echo "install dependencies..."
    sudo pacman -S --needed --noconfirm \
        base-devel \
        gcc-fortran \
        openblas \
        uv \
        python-pipx \
        nvidia-utils

    # install ollama cuda from aur
    if ! command -v ollama &> /dev/null 
    then
        echo "installing ollama-cuda"
        yay -S --noconfirm ollama-cuda
    else 
        echo "ollama already installed"
    fi

elif [[ "$env" == "Debian" ]]; then
    echo "install dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        build-essential \
        gfortran \
        libopenblas-dev \
        uv \
        python3-pipx \
        nvidia-utils-470

    # install ollama cuda from deb package
    if ! command -v ollama &> /dev/null 
    then
        echo "installing ollama-cuda"
        sudo apt-get install -y ollama-cuda
    else 
        echo "ollama already installed"
    fi

else
    echo "Unsupported environment. Please choose either Arch or Debian."
    exit 1
fi

#enable and start services
echo "starting ollama service..."
sudo systemctl enable --now ollama

#pull models
echo "donwloading models..."
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder-v2:16b

#install aider
echo "installing aider in venv with uv..."
uv python install 3.12
uv tool install aider-chat --python 3.12  --force

export PATH="$HOME/.local/bin:$PATH"
echo "aider managed by uv"

echo "--setup complete--"

echo " "
echo "run: 'aider --model ollama/qwen2.5-coder:7b' ( or just use the alias that i made in docs :) ) to start."

echo "====TO USE THE ALIAS===="
read -r -p "Do you want to apply the ai-coder alias now? [Y/n] " response

response=${response:-Y}

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Applying alias..."
    if [ -f "scripts/aider-model-alias.sh" ]; then
        chmod +x scripts/aider-model-alias.sh
        ./scripts/aider-model-alias.sh
    else
        echo "Error: scripts/aider-model-alias.sh not found!"
    fi
else
    echo "Skipped alias configuration."
fi


echo " "
echo " "

echo "verification:"
ollama --version
aider --version

echo "tip: Add 'export PATH=\$HOME/.local/bin:\$PATH' to your .zshrc if not already there."
