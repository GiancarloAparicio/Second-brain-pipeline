#!/bin/bash

noteId=$1
deck=$2

echo "ID: $noteId"
echo "DECK: $deck"

value=$(curl localhost:8765 -X POST -d "{
    \"action\": \"notesInfo\",
    \"version\": 6,
    \"params\": {
        \"notes\": [$noteId]
    }
}" | jq --compact-output --raw-output '.result[].cards')

curl localhost:8765 -X POST -d "{
    \"action\": \"changeDeck\",
    \"version\": 6,
    \"params\": {
        \"cards\":  $value ,
        \"deck\": \"$deck\"
    }
}"
