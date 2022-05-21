#!/bin/bash

PATH_VAULT=$(jq -r .vault ./config.json)
WORKSPACE="$PATH_VAULT/.obsidian/workspace"
CACHE="$PATH_VAULT/.obsidian/last-file.cached.txt"

CACHE=$1

get_lastest_files() {

  jq --raw-output '.lastOpenFiles[]' "$WORKSPACE" >>"$PATH_VAULT/.obsidian/lastFiles.txt"
	cat "$PATH_VAULT/.obsidian/lastFiles.txt" | sort -u >"$PATH_VAULT/.obsidian/lastFiles.temp"
	cat "$PATH_VAULT/.obsidian/lastFiles.temp" >"$PATH_VAULT/.obsidian/lastFiles.txt"
	rm "$PATH_VAULT/.obsidian/lastFiles.temp"
	echo $( --raw-output '.lastOpenFiles[]' "$WORKSPACE")
}

file="$PATH_VAULT/$( jq --raw-output '.lastOpenFiles[]' "$WORKSPACE" | head -1)"

if [[ -f "$CACHE" ]]; then
	lastFile=$(cat "$CACHE")
	echo "Target: $lastFile"
	python3 .scripts/obsidian_to_anki/bin.py -t "$lastFile"
else
	echo "Target: $file"
	python3 .scripts/obsidian_to_anki/bin.py -t "$file"

fi

echo "$file" >"$CACHE"
