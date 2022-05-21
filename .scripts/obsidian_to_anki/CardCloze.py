import re
import markdown
import Anki
import Obsidian
import Env


class CardCloze:
    def __init__(self, match, file):
        self.file = file
        self.matchs = match.group(1)
        self.id = match.group(2)
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

    def add_ankiID_to_card(self, anki_id):
        matchs = re.findall(r" \^(\w{4,12})$", self.id)

        if not Env.DEVELOPMENT:
            for group in matchs:
                id_obsidian = group
                print(f"REPLACE ID OBSIDIAN: {id_obsidian}::{anki_id}")
                self.obsidian.replace_string_in_all_files(id_obsidian, anki_id)

            else:
                new_back = f"{self.matchs} #anki-cloze ^{anki_id}"
                self.obsidian.replace_string_in_file(
                    self.file, f"{self.matchs}{self.id}", new_back
                )

    def prepare_cloze(self):

        matchs = re.findall(Env.MATCH_CLOZE, self.matchs)
        result = self.matchs
        for index, group in enumerate(matchs):
            matchs = re.findall("(\d{1,2}):(.*)", group)

            for group in matchs:
                num = f"c{group[0]}"
                val = f"{group[1]}"
                result = result.replace(group, f"{num}:{val}")
            else:
                result = result.replace(group, f"c{index+1}:{group}")

        self.front = result.replace("{", "{{").replace("}", "}}").replace(":", "::")
        self.back = ""

        return self.obsidian.convert_markdown_to_html(self)

    def save(self):
        CURRENT_CARD_EXISTS = "\^(\d{13,15}) *$"
        print(f"MIRA {self.id}")
        cardExists = re.findall(CURRENT_CARD_EXISTS, self.id)
        card_in_html = self.prepare_cloze()
        print(card_in_html)

        if cardExists:
            id_anki = cardExists[0]
            self.anki.update_card_cloze(card_in_html, id_anki, self.file)
        else:
            id_anki = self.anki.create_card_cloze(card_in_html, self.file)
            self.add_ankiID_to_card(id_anki)
