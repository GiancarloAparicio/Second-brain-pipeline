import re
import Anki
import Obsidian
import Env
import os
import shutil


class CardsForQuestions:
    def __init__(self, match, file):
        self.file = file
        self.front = ""
        self.back = ""
        self.questions = match.group(1)
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

    def add_ankiID_to_card(self, anki_id, row):
        matchs = re.findall(r"\^(\w{6})$", row)

        if not Env.DEVELOPMENT:
            for group in matchs:
                id_obsidian = group
                print(f"REPLACE ID OBSIDIAN: {id_obsidian}::{anki_id}")
                self.obsidian.replace_string_in_all_files(id_obsidian, anki_id)

            else:
                new_row = f"{row} ^{anki_id}"
                self.obsidian.replace_string_in_file(self.file, row, new_row)

    def save(self):
        pattern = re.compile(
            Env.CARDS_QUESTIONS_MATCH,
            re.MULTILINE,
        )

        cards = pattern.finditer(self.questions)

        CURRENT_CARD_EXISTS = "\^(\d{13,15}) *?$"
        print(f"{self.questions}")

        for index, card in enumerate(cards):
            print(f"CARD: {card}")
            self.front = card[1]
            self.back = card[2]

            cardExists = re.findall(CURRENT_CARD_EXISTS, self.back)
            card_in_html = self.obsidian.convert_markdown_to_html(self)

            if cardExists:
                id_anki = cardExists[0]
                self.anki.update_card(card_in_html, id_anki, self.file)
            else:
                id_anki = self.anki.create_card_basic(card_in_html, self.file)
                self.add_ankiID_to_card(id_anki, self.back)
