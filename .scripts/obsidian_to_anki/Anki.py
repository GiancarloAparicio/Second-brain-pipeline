import json
import urllib
import urllib.request
import Env
import Card
import os


class Anki:
    def request(self, action, **params):
        return {"action": action, "params": params, "version": 6}

    def invoke(self, action, **params):
        requestJson = json.dumps(self.request(action, **params))
        response = json.load(
            urllib.request.urlopen(
                urllib.request.Request(
                    "http://localhost:8765", requestJson.encode("utf-8")
                )
            )
        )

        print(f"REQUEST: http://localhost:8765 {requestJson.encode('utf-8')}")

        if len(response) != 2:
            raise Exception("response has an unexpected number of fields")
        if "error" not in response:
            raise Exception("response is missing required error field")
        if "result" not in response:
            raise Exception("response is missing required result field")
        if response["error"] is not None:
            raise Exception(response["error"])
        return response["result"]

    def changeDeck(self, id_card, fullfile):
        deck = (
            fullfile.replace("/", "::")
            .replace(".md", "")
            .replace(f"{Env.VAULT}::", "")
        )
        print(f" CHANGE DECK: {deck} ")
        os.system(
            f"bash .scripts/obsidian_to_anki/update_decks_from_cards.sh '{id_card}' '{deck}' "
        )

        # result = self.invoke("changeDeck", cards=[int(id_card)], deck=f"{deck}")
        # print(f"RESULTADO: {result}")

    def createOcclusion(self, image, header, fullfile):
        deck = self.createDeck(fullfile)
        note = {
            "deckName": f"{deck}",
            "modelName": "Image Occlusion Enhanced",
            "fields": {"Image": f"{image}", "Header": f"{header}"},
            "options": {
                "closeAfterAdding": True,
                "allowDuplicate": False,
                "duplicateScope": "deck",
            },
        }
        try:
            if not Env.DEVELOPMENT:
                new_id = self.invoke("guiAddCards", note=note)
                print(f"NEW CARD: {new_id}")
                return new_id

        except Exception as e:
            print(f"ERROR: An exception occurred on creation basic. {e}")

    def createDeck(self, fullfile):
        decks = (
            fullfile.replace("/", "::")
            .replace(".md", "")
            .replace(f"{Env.VAULT}::", "")
        )
        self.invoke("createDeck", deck=f"{decks}")
        return decks

    def update_card(self, card, id_anki, file):
        front = card["front"].replace("```", "")
        back = card["back"].replace("```", "")

        self.changeDeck(int(id_anki), file)

        note = {
            "id": int(id_anki),
            "fields": {
                "Front": f"{front}",
                "Back": f"{Card.Card.delete_id_anki(back)}",
            },
        }

        try:

            if not Env.DEVELOPMENT:
                self.invoke("updateNoteFields", note=note)
                print(f"UPDATE CARD: {id_anki}")

        except Exception:
            print(f"ERROR: An exception occurred on updated: {id_anki}")

    def update_card_cloze(self, card, id_anki, file):
        self.changeDeck(int(id_anki), file)
        note = {
            "id": int(id_anki),
            "fields": {"Text": f"{card['front']}", "Extra": " "},
        }

        try:

            if not Env.DEVELOPMENT:
                self.invoke("updateNoteFields", note=note)
                print(f"UPDATE CARD: {id_anki}")

        except Exception:
            print(f"ERROR: An exception occurred on updated: {id_anki}")

    def create_card_basic(self, card, file, type_card="Basic"):
        deck = self.createDeck(file)
        front = card["front"].replace("```", "")
        back = card["back"].replace("```", "")
        note = {
            "deckName": f"{deck}",
            "modelName": f"{type_card}",
            "fields": {
                "Front": f"{front}",
                "Back": f"{Card.Card.delete_id_anki(back)}",
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
            },
        }
        try:
            if not Env.DEVELOPMENT:
                new_id = self.invoke("addNote", note=note)
                print(f"NEW CARD: {new_id}")
                return new_id

        except Exception as e:
            print(f"ERROR: An exception occurred on creation basic. {e}")

    def create_card_cloze(self, card, file):
        deck = self.createDeck(file)
        note = {
            "deckName": f"{deck}",
            "modelName": "Cloze",
            "fields": {"Text": f"{card['front']}", "Extra": " "},
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
            },
        }
        print(f"CARTA CREADA {note}")
        try:
            if not Env.DEVELOPMENT:
                new_id = self.invoke("addNote", note=note)
                print(f"NEW CARD: {new_id}")
                return new_id

        except Exception as e:
            print(f"ERROR: An exception occurred on creation cloze. {e}")
