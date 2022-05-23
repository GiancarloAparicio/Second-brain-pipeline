import json


def getVault():
    with open('config.json') as file:
        data = json.load(file)
    return data['vault']


DEVELOPMENT = False
ALL_FILES = True
VAULT = getVault()
ATTACHMENTS = f"{VAULT}/300 - 🗄️ Resources/380 - 🗃️ Attachments/Media"

CARD_BASIC = "(?:`{3,6})?(?:ad-\w+\n?)?((?:[^\n>])+) #anki +.*\n*((?:\n(?:^.{1,3}$|^.{4}.*))+)(?:\n*`{3,6} *\n)?"
CARD_BASIC_INLINE = "^(.*[^\n:]{1}):{2}([^\n:]{1}.*) (#anki-inline.*)"
CARDS_QUESTIONS = "#anki-questions ?\n*((?:.|\n)+)?"
CARDS_QUESTIONS_MATCH = "((?:[^\n>])+)\n*((?:\n(?:^.{1,3}$|^.{4}.*))+)"
OCCLUSION = " *#occlusion(.*\!\[\[.*\]\] *(?:\^\w{3,16})?)"


# Captura lista de cards cloze
LIST_CARD_CLOZE = (
    "((?:[^\n>-][\n]?)+) #anki-list-cloze ?\n*((?:\n(?:^.{1,3}$|^.{4}.*))+)"
)
# Obtiene los card de la lista
LIST_CLOZE_MATCH = "^ *([*+-123456789] .+)"

# Captura una tabla markdown
FIND_TABLE = "(.*): *#anki-list *\n+((?:.||\n)*)\n$"
# Convierte las lineas de la tabla en campos
CARD_TABLE_MATCH = "\|(.*)\|( +\^\w{13})?"

# Captura todo la linea para cloze
# CARD_CLOZE = "((?:[^\n>-][\n]?)+)(?:#anki-cloze *)[^-]\^?(\w+)?"
CARD_CLOZE = "((?:[^\n>-][\n]?)+)(#anki-cloze *\^?(?:\w+)? *)"
CARD_DEFINITION = "((?:[^\n>-][\n]?)+)(?:#definition +)[^-]\^?(\w+)?"

# Obtiene cada cloze anterior
MATCH_CLOZE = "{{1,2}(.*?)}{1,2}[^${]"
