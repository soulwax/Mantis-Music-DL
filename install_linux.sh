#!/bin/bash

# Install packages
sudo apt update
sudo apt install -y 7zip git curl

# Install Node Version Manager (nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# Reload the shell
source ~/.bashrc

# Install nvm and Node.js
nvm install --lts
nvm use --lts
npm install -g npm@latest

# Install Python
sudo apt install -y miniconda
conda init bash
conda install -y python=3.13
