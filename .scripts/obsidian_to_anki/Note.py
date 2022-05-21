import re
import Env


class Note:
    def __init__(self, fullfile):
        self.fullfile = fullfile.strip().replace('"', "")

    def find_cards(self, regexp):

        # Open file as file object and read to string
        print(f"file : {self.fullfile}")
        file = open(f"{self.fullfile}", "r")

        # Read file object to string
        text = file.read()

        # Close file object
        file.close()

        # Regex pattern
        pattern = re.compile(
            regexp,
            re.MULTILINE,
        )

        cards = pattern.finditer(text)

        return cards
