#!/bin/bash

PATH_VAULT=$(jq -r .vault ./config.json)
WORKSPACE="$PATH_VAULT/.obsidian/workspace"
CACHE="$PATH_VAULT/.obsidian/last-file.cached.txt"

function ctrl_c() {
	echo -e "\n Exit...!\n"
	rm -r "$CACHE"
  bash .scripts/sync.sh
	exit 0
}

trap ctrl_c INT

ls "$WORKSPACE" | entr -r bash .scripts/hot_reload.aux.sh "$CACHE"
