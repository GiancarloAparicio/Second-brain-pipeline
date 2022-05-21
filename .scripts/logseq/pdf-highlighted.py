import json
import os

# os.system(" cat notes/attachments/assets/bash-es_1648664422591_0.edn | jet --to json")


json_file = "test.json"

with open(json_file, "r") as j:
    data = json.load(j)

    for line in data["highlights"]:
        page = line["page"]
        id = line["id"]
        text = line["content"]["text"]
        color = line["properties"]["color"]
        template = ""

        # print(f"id: {id}")
        # print(f"text: {text}")
        # print(f"color: {color}")

        if text == "[:span]":
            image = line["content"]["image"]
            template = f"![[{page}_{id}_{image}.png|]]"
        else:
            if color == "red":
                template = f"""## {text}\n---"""
            elif color == "yellow":
                template = f"""\n> {text}\n"""
            elif color == "green":
                template = text
            elif color == "blue":
                template = f"""# {text}\n---"""
            elif color == "purple":
                template = f"### {text}"

        print(template)
