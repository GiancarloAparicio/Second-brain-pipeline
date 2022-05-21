import re
import Anki
import Obsidian
import Env
import os
import shutil


class CardsForTable:
    def __init__(self, match, file):
        self.file = file
        self.caption = match.group(1)
        self.table = match.group(2)
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

    def add_ankiID_to_card(self, anki_id, row):
        matchs = re.findall(r"\^(\w{4,12})$", row)

        if not Env.DEVELOPMENT:
            for group in matchs:
                id_obsidian = group
                print(f"REPLACE ID OBSIDIAN: {id_obsidian}::{anki_id}")
                self.obsidian.replace_string_in_all_files(id_obsidian, anki_id)

            else:
                new_row = f"{row} ^{anki_id}"
                self.obsidian.replace_string_in_file(self.file, row, new_row)

    def prepare_audio(self, text, lang, label):
        audio = f"{text.strip().replace(' ','-')}-{lang.strip().replace(' ','-')}-{label.strip().replace(' ','-')}.mp3"
        audio = (
            audio.replace("/", "-")
            .replace("(", "-")
            .replace(")", "-")
            .replace("{", "-")
            .replace("}", "-")
            .replace("'", "-")
            .replace('"', "-")
            .replace("´", "-")
            .replace("?", "-")
            .replace("¿", "-")
            .replace("\\", "-")
            .replace("*", "-")
            .replace("'", "-")
            .replace("`", "-")
        )

        print(f"Prepare audio: {text}")
        print(f"Audio generate: {audio}")

        print(f'gtts-cli "{text}" --output {audio}')
        os.system(f'gtts-cli "{text}" --output {audio}')

        shutil.move(f"./{audio}", f"{Env.ATTACHMENTS}/{audio}")
        shutil.copyfile(
            f"{Env.ATTACHMENTS}/{audio}",
            f"{os.path.expanduser('~')}/.local/share/Anki2/Erick Ramos Aparicio/collection.media/{audio}",
        )
        return audio

    def add_audio_to_lang(self, row, other_origin, other, audio):
        new_row = row.replace(f" {other_origin} ", f" [[{audio}\|{other.strip()}]] ", 1)
        self.obsidian.replace_string_in_file(self.file, row, new_row)

    def delete_links(self, text):
        regexp = "\[(.*?)\]\((.*?)\)"
        matchs = re.findall(regexp, text)
        result = text

        for group in matchs:
            caption = f"{group[0]}"
            reference = f"{group[1]}"
            result.replace(f"[{caption}]({reference})", caption)
        return result

    def save(self):
        cards = re.findall(Env.CARD_TABLE_MATCH, self.table)
        other_language = ""
        native_language = ""
        print(self.table)

        for index, card in enumerate(cards):
            print(f"CARD: {card}")
            other = card[0].split(" | ")[0]
            native = card[0].split(" | ")[1]

            id_anki = card[1]
            try:
                example_sentence = card[0].split(" | ")[2]
                example_sentence = f"_{example_sentence.strip()}_".replace("__", "")
            except Exception:
                example_sentence = ""

            if index == 0:
                other_language = other
                native_language = native
            elif index != 1:

                other_origin = other
                if ".mp3" in other:
                    print(f"Update audio: {other}")
                    other = re.findall("\[\[.*\|(.*)\]\]", other)[0]
                audio = self.prepare_audio(other, other_language, self.caption)
                self.back = f"### {self.caption} \n * {other_language.strip()}: {other.strip()} [sound:{audio}] \n {self.delete_links(example_sentence)} "
                self.front = f"### {self.caption} \n * {native_language.strip()}: {self.delete_links(native.strip())}"
                card_in_html = self.obsidian.convert_markdown_to_html(self)
                print(f"CARD HTML: {card_in_html}")

                row = f"|{card[0]}|{id_anki}"
                if id_anki:
                    only_id = re.findall(r"\d+", id_anki)[0]
                    self.anki.update_card(card_in_html, only_id, self.file)
                else:
                    id_anki = self.anki.create_card_basic(
                        card_in_html, self.file, "Basic (and reversed card)"
                    )
                    self.add_ankiID_to_card(id_anki, row)

                self.add_audio_to_lang(row, other_origin.strip(), other, audio)
