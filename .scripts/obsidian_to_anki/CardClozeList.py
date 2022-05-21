import re
import markdown
import Anki
import Obsidian
import Env
import Card


class CardClozeList:
    def __init__(self, match, file):
        self.file = file
        self.title = match.group(1)
        self.matchs = match.group(2)
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

    def add_ankiID_to_card(self, card, anki_id):
        matchs = re.findall(r" \^(\w{4,12})$", card)

        if not Env.DEVELOPMENT:
            for group in matchs:
                id_obsidian = group
                print(f"REPLACE ID OBSIDIAN: {id_obsidian}::{anki_id}")
                self.obsidian.replace_string_in_all_files(id_obsidian, anki_id)

            else:
                new_back = f"{card} ^{anki_id}"
                self.obsidian.replace_string_in_file(self.file, card, new_back)

    def prepare_cloze(self, card):
        card = Card.Card.delete_id_anki(card)
        matchs = re.findall(Env.MATCH_CLOZE, card)
        result = f""" {self.title}

{card}"""
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

    def save_list(self):
        cards = re.findall(Env.LIST_CLOZE_MATCH, self.matchs, re.MULTILINE)
        CURRENT_CARD_EXISTS = "\^(\d{13}) *?$"
        print(f"CARDS: {cards}")

        for index, card in enumerate(cards):

            print(f"Card cloze list: {card}")

            card_in_html = self.prepare_cloze(card)
            cardExists = re.findall(CURRENT_CARD_EXISTS, card)
            print(f"CLOZE PREPARE: {card_in_html}")

            matchs = re.findall("{{2}(.*?::.*?)}{2}", card_in_html["front"])
            if matchs:
                if cardExists:
                    id_anki = cardExists[0]
                    self.anki.update_card_cloze(card_in_html, id_anki, self.file)
                else:
                    id_anki = self.anki.create_card_cloze(card_in_html, self.file)
                    self.add_ankiID_to_card(card, id_anki)
