#!/bin/bash

install() {
	echo $@ | xargs -n 1 sudo apt install --fix-missing -y
}

OS=$(uname -o)

if ! [ "${OS}" == "Android" ]; then
	# Is not termux
	wget https://github.com/borkdude/jet/releases/download/v0.1.0/jet-0.1.0-linux-amd64.zip
	unzip jet-0.1.0-linux-amd64.zip
	sudo mv jet /usr/bin
	rm jet-0.1.0-linux-amd64.zip
fi

apt update && apt upgrade -y

#-------------------------------------------------------------------
# Install dependencies
install pip3 jq python3-pip python3-dev mpg321 sox libsox-fmt-all jpegoptim optipng

pip3 install pyttsx3

pip3 install markwdown

python -m pip install pygments

sudo -H pip3 install gtts
