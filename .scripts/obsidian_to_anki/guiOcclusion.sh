#!/bin/bash

image=$1
deck=$2

curl localhost:8765 -X POST -d "{
    \"action\": \"guiAddCards\",
    \"version\": 6,
    \"params\": {
        \"note\": {
            \"deckName\": \"$deck\",
            \"modelName\": \"Image Occlusion Enhanced\",
            \"fields\": {
                \"Image\": \"$image\"
            },
            \"options\": {
                \"closeAfterAdding\": true
            },
        }
    }
}"
