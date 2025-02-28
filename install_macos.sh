#!/usr/bin/env bash

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update Homebrew
brew update

# Install packages
brew install 7zip git

# Add taps (similar to buckets in Scoop)
brew tap homebrew/cask-fonts
brew tap homebrew/cask-versions
brew tap homebrew/cask-drivers
brew tap homebrew/cask-games
brew tap homebrew/cask
brew tap adoptopenjdk/openjdk
brew tap shivammathur/php
brew tap homebrew/cask-nirsoft


# Install Node Version Manager (nvm)
brew install nvm
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$(brew --prefix)/opt/nvm/nvm.sh" ] && . "$(brew --prefix)/opt/nvm/nvm.sh"' >> ~/.zshrc

# Reload the shell
source ~/.zshrc

# Install nvm and Node.js
nvm install --lts
nvm use --lts
npm install -g npm@latest

# Install Python
brew install miniconda yt-dlp ffmpeg
conda init bash
conda install -y python=3.13