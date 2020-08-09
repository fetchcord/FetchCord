#!/bin/bash
pyver=$(python --version | grep -o "3..")
if [ ! $pyver ]; then
  echo "Python3 must be installed to use this script, exiting."
  exit 1
fi
# keep track of path used to run installer
where=$PWD
flatpakdir="$HOME/.var/app/com.discordapp.Discord"
if [ -d $flatpakdir ]; then
  echo "symlinking XDG_RUNTIME_DIR for Discord Flatpak.."
  cd $HOME/.var
  ln -sf {app/com.discordapp.Discord,$XDG_RUNTIME_DIR}/discord-ipc-0
fi

if [ $EUID != 0 ]; then
  cd $where
  sudo -u root bash -c ./install.sh
fi
if [ $EUID == 0 ]; then
  dir="/usr/local/bin/"
  python3 setup.py install --root="/"
  ln -sf /lib/python$pyver/site-packages/fetch_cord/run-rpc.py /usr/local/bin/fetchcord
  cp discord $dir
  chmod 755 ${dir}fetchcord ${dir}discord
  exit 0
fi
