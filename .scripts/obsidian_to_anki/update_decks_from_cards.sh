#!/bin/bash

noteId=$1
vault=$(jq -r .vault config.json)
deck=$(echo $2 | sed "s/$vault:://g")

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
