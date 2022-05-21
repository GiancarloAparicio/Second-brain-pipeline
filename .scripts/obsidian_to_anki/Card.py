import re
import Anki
import Obsidian
import Env


class Card:
    def __init__(self, match, file):
        self.file = file
        self.front = match.group(1).replace("%%", "").replace("    ```", "```")
        self.back = match.group(2).replace("    ```", "```")
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

        print(f"FRONT: {self.front}")
        print(f"BACK: {self.back}")

    @classmethod
    def delete_id_anki(cls, back):
        # regexp = "(\^\w{4,} *$)"
        regexp = "(\^\w{5,15})"
        newBack = re.sub(regexp, " ", back)
        print(f"NEW BACK: {newBack}")
        return newBack

    def add_ankiID_to_card(self, anki_id):
        id_obsidian = re.findall(r" \^(\w{4,12}) *$", self.back.strip())

        if not Env.DEVELOPMENT:
            for group in id_obsidian:
                id_obsidian = group
                print(f"REPLACE ID OBSIDIAN: {id_obsidian}::{anki_id}")
                self.obsidian.replace_string_in_all_files(id_obsidian, anki_id)

            else:
                print(f"ADD ID ANKI: {anki_id}")
                print(f"BACK OLD: {self.back}")
                new_back = f"{self.back} ^{anki_id}".replace(
                    "``` ^",
                    """```
^""",
                )

                self.obsidian.replace_string_in_file(
                    self.file, f"{self.back}", new_back
                )

    def save(self):
        CURRENT_CARD_EXISTS = "\^(\d{13,15}) *?$"
        cardExists = re.findall(CURRENT_CARD_EXISTS, self.back)
        card_in_html = self.obsidian.convert_markdown_to_html(self)

        if cardExists:
            id_anki = cardExists[0]
            self.anki.update_card(card_in_html, id_anki, self.file)
        else:
            id_anki = self.anki.create_card_basic(card_in_html, self.file)
            self.add_ankiID_to_card(id_anki)
