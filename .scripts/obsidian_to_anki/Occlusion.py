import re
import Anki
import Obsidian
import Env


class Occlusion:
    def __init__(self, match, file):
        self.file = file
        self.image = match.group(1)
        self.obsidian = Obsidian.Obsidian()
        self.anki = Anki.Anki()

        print(f"IMAGE: {self.image}")

    def add_ankiID_to_card(self):
        if not Env.DEVELOPMENT:
            new_back = f"%%load%% {self.image}"
            self.obsidian.replace_string_in_file(self.file, f"{self.image}", new_back)

    def save(self):
        CURRENT_CARD_EXISTS = "\%\%load\%\%"
        cardExists = re.findall(CURRENT_CARD_EXISTS, self.image)
        image = re.findall("\!\[\[(.*?)\]\]", self.image)[0].split("|")
        path_image = image[0]
        header = ""
        if len(image) == 3:
            header = image[1]
        elif len(image) == 2:
            header = image[1]
            if header.isdigit():
                header = ""

        if not cardExists:
            self.anki.createOcclusion(path_image, header, self.file)
            self.add_ankiID_to_card()
