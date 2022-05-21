import markdown
import shutil
import re
import os
import Env
from urllib.parse import quote


class Obsidian:

    directory = "./"

    def replace_string_in_file(self, fullfile, old, new):
        fin = open(fullfile, "rt")
        data = fin.read()
        data = data.replace(old.strip(), new.strip())
        fin.close()

        fin = open(fullfile, "wt")
        fin.write(data)
        fin.close()

    def replace_string_in_all_files(self, old, new):
        print(f"Replace in all files: {old}::{new}")
        for root, dirs, files in os.walk(self.directory, topdown=False):
            for file in files:
                if file.lower().strip().endswith(".md"):
                    fullfile = os.path.join(root, file)
                    self.replace_string_in_file(fullfile, f"{old}", f"{new}")

    def delete_id_obsidian(self, text):
        regexp = " \^(.*) "
        matchs = re.findall(regexp, text)
        if matchs:
            text = text.replace(f"^{matchs[0]}", "")
        return text

    def prepare_resource_to_anki(self, resource):
        fileExternals = resource.lower().endswith(
            (
                ".svg",
                ".png",
                ".gif",
                ".jpg",
                ".jpeg",
                ".pdf",
                ".mp4",
                ".mp3",
            )
        )

        print(f"Move resource: {resource}")

        if not Env.DEVELOPMENT:
            # Si es un archivo externo
            if fileExternals:
                shutil.copyfile(
                    f"{os.getcwd()}{Env.ATTACHMENTS[1:]}/{resource}",
                    f"{os.path.expanduser('~')}/.local/share/Anki2/Erick Ramos Aparicio/collection.media/{resource}",
                )

    def wikilink_to_markdown(self, line):
        # Recibe BACK o FRONT
        regexp = "\[\[(.*?)\]\]"
        matchs = re.findall(regexp, line)

        for group in matchs:
            if "|" in group:
                link = group.split("|")
                reference = link[0]
                caption = link[1]
                self.prepare_resource_to_anki(reference)

                # Si es un archivo externo
                new_link = f"[{caption}]({reference})"
                old_link = f"[[{group}]]"
                line = line.replace(old_link, new_link)
                print(f"NEW LINK {new_link}")
                print(f"OLD LINK {old_link}")
            else:
                new_link = f"[{group}]({group})"
                old_link = f"[[{group}]]"
                self.prepare_resource_to_anki(group)
                line = line.replace(old_link, new_link)

        return line.strip()

    def convert_markdown_to_html(self, card):
        print(f"CARD: {card}")
        front = card.front
        back = card.back
        markdown_front = self.wikilink_to_markdown(front)
        markdown_back = self.wikilink_to_markdown(back)
        regexp = re.compile("^[*-] ", re.MULTILINE)
        markdown_front = regexp.sub("\n\n* ", markdown_front)
        markdown_back = regexp.sub("\n\n* ", markdown_back)

        front_html = markdown.markdown(
            markdown_front,
            extensions=["fenced_code", "codehilite"],
        ).replace("\n", "")
        back_html = (
            markdown.markdown(
                markdown_back,
                extensions=["fenced_code", "codehilite"],
            )
            .replace("```", "")
            .replace("\n", "")
        )

        file = os.path.splitext(quote(card.file))[0].replace("notes/", "", 1)
        url = f"obsidian://open?vault=notes&file={file}"
        tag = f'<div> <a class="tag" href="{url}">#obsidian</a> </div>'

        return {"front": f"{front_html} \n {tag}", "back": f"{back_html}"}
