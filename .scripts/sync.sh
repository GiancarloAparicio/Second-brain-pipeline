#!/bin/bash

TIMESTAMP=$(date)

VAULT=$(jq -r .vault config.json)

python3 .scripts/optimice_images.py

git add .

OS=$(uname -o)

if [ "${OS}" == "Android" ]; then
	# Is termux
	git restore --staged "$VAULT/.obsidian/workspaces.json"
	git restore "$VAULT/.obsidian/workspaces.json"

	git restore --staged "$VAULT/.obsidian/workspace"
	git restore "$VAULT/.obsidian/workspace"
fi

git commit -m "${TIMESTAMP}"

git push --follow-tags origin "$(git rev-parse --abbrev-ref HEAD)"

git pull --rebase --verbose origin "$(git rev-parse --abbrev-ref HEAD)"
