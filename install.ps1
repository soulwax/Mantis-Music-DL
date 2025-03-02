# File: install.ps1

# install scoop
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod get.scoop.sh | Invoke-Expression

# install packages
scoop install 7zip, git
scoop bucket add extras
scoop bucket add nonportable
scoop bucket add versions
scoop bucket add sysinternals
scoop bucket add nerd-fonts
scoop bucket add games
scoop bucket add java
scoop bucket add php
scoop bucket add nirsoft

# install python
scoop install miniconda3 yt-dlp ffmpeg
conda init powershell
conda install -y python=3.13

scoop install nvm
nvm install latest
nvm use latest
npm install -g npm@latest

python -m pip install --upgrade pip
pip install -r .\requirements.txt





