# File: install.sh

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

# Install Python
brew install miniconda yt-dlp ffmpeg
conda init bash
conda install -y python=3.13

# Install Node Version Manager (nvm)
brew install nvm
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bash_profile
echo '[ -s "$(brew --prefix)/opt/nvm/nvm.sh" ] && . "$(brew --prefix)/opt/nvm/nvm.sh"' >> ~/.bash_profile
echo '[ -s "$(brew --prefix)/opt/nvm/etc/bash_completion.d/nvm" ] && . "$(brew --prefix)/opt/nvm/etc/bash_completion.d/nvm"' >> ~/.bash_profile
source ~/.bash_profile
nvm install --lts
nvm use --lts
npm install -g npm@latest

# Upgrade pip and install requirements
python3 -m pip install --upgrade pip
pip install -r requirements.txt
