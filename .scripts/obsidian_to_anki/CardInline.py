import re
import Anki
import Obsidian
import Env


class CardInline:
    def __init__(self, match, file):
        self.file = file
        self.front = match.group(1)
        self.back = match.group(2)
        self.id = match.group(3)
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

        print(f"FRONT: {self.front}")
        print(f"BACK: {self.back}")

    def add_ankiID_to_card(self, anki_id):
        matchs = re.findall(r" \^(\w{4,12})$", self.id)

        if not Env.DEVELOPMENT:
            for group in matchs:
                id_obsidian = group
                print(f"REPLACE ID OBSIDIAN: {id_obsidian}::{anki_id}")
                self.obsidian.replace_string_in_all_files(id_obsidian, anki_id)

            else:
                new_back = f"{self.back} #anki-inline ^{anki_id}"
                self.obsidian.replace_string_in_file(
                    self.file, f"{self.back} {self.id}", new_back
                )

    def save(self):
        CURRENT_CARD_EXISTS = "\^(\d{13}).*?"
        cardExists = re.findall(CURRENT_CARD_EXISTS, self.id)
        card_in_html = self.obsidian.convert_markdown_to_html(self)

        if cardExists:
            id_anki = cardExists[0]
            self.anki.update_card(card_in_html, id_anki, self.file)
        else:
            id_anki = self.anki.create_card_basic(card_in_html, self.file)
            self.add_ankiID_to_card(id_anki)
