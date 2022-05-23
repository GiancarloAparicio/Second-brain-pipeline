import os
import sys
import getopt
import Note
import Env
import Card
import CardInline
import CardCloze
import CardsForQuestions
import CardClozeList
import CardsForTable
import Occlusion


def run_sync_anki(modified_files):
    for file in modified_files:
        file = file.strip()

        print(os.path.exists(f"{file}"))
        if os.path.exists(f"{file}"):
            print(f"Exits: {file}")
            print(f"find cards on file : {file}")
            note = Note.Note(file)

            # Create cards basic
            cards = note.find_cards(Env.CARD_BASIC)
            for card in cards:
                print(f"CARD BASIC: {card}")
                # Create Decks
                card = Card.Card(card, file)
                card.save()

            # Create cards basic inline
            cards = note.find_cards(Env.CARD_BASIC_INLINE)
            for card in cards:
                print(f"CARD INLINE: {card}")
                # Create Decks
                card = CardInline.CardInline(card, file)
                card.save()

            # Create cards definition
            cards = note.find_cards(Env.CARD_DEFINITION)
            for card in cards:
                print(f"CARD DEFINITION: {card}")
                # Create Decks
                card = CardCloze.CardCloze(card, file)
                card.save()

            # Create cards cloze
            cards = note.find_cards(Env.CARD_CLOZE)
            for card in cards:
                print(f"CARD CLOZE: {card}")
                # Create Decks
                card = CardCloze.CardCloze(card, file)
                card.save()

            # Create list cards cloze
            cards = note.find_cards(Env.LIST_CARD_CLOZE)
            for card in cards:
                print(f"LIST CARD CLOZE: {card}")
                # Create Decks
                card = CardClozeList.CardClozeList(card, file)
                card.save_list()

            # Create cards for table
            cards = note.find_cards(Env.FIND_TABLE)
            for card in cards:
                print(f"CARDS FOR TABLE: {card}")
                # Create Decks
                card = CardsForTable.CardsForTable(card, file)
                card.save()

            # Create cards for occlusion
            cards = note.find_cards(Env.OCCLUSION)
            for card in cards:
                print(f"CARDS FOR OCCLUSION: {card}")
                # Create Decks
                card = Occlusion.Occlusion(card, file)
                card.save()

            # Create cards definition
            cards = note.find_cards(Env.CARDS_QUESTIONS)
            for card in cards:
                print(f"CARD QUESTION: {card}")
                # Create Decks
                card = CardsForQuestions.CardsForQuestions(card, file)
                card.save()

    modified_files.close()


def main(argv):

    opts, args = getopt.getopt(argv, "t:f:")
    print(f"OPT anki sync (bin.py): {opts}")
    if opts:
        for opt, arg in opts:
            if opt == "-t":
                os.system(f" echo '{arg}'  > modified.files.git.txt")

            if opt == "-f":
                os.system(f" cat '{arg}'  > modified.files.git.txt")

    else:

        if not Env.ALL_FILES:
            os.system(
                "printf \"$(git status -sb | grep '.md' "
                "| awk '{$1=\"\"; print $0}' | tr -d '\"' )\""
                " > modified.files.git.txt"
            )
        else:
            os.system("fd -e md | cut -c3-  > modified.files.git.txt")

    os.system(
        f"cat modified.files.git.txt | grep -v  "
        f"'{Env.VAULT}/300 - 🗄️ Resources/' "
        f"| grep -v '{Env.VAULT}/400 - 🐣 Immature/' |"
        f" grep -v '{Env.VAULT}/README' > modified.files.txt"
    )
    modified_files = open("modified.files.txt", mode="r", encoding="utf-8")
    run_sync_anki(modified_files)

    os.remove("modified.files.git.txt")
    os.remove("modified.files.txt")


if __name__ == "__main__":
    main(sys.argv[1:])
