import re
import env
import os


class Resumen:
    def __init__(self, fullfile):
        self.fullfile = fullfile

    def getMatchs(self, regexp, note):
        matchs = re.findall(regexp, note)

        for group in matchs:
            return group

    def getLink(self, note):
        matchs = re.findall(env.GET_LINK, note)

        for group in matchs:
            print(f"LINK: [[{self.fullfile}{group}")
            return f"[[{self.fullfile}{group}"

    def getMetaData(self):
        # Open file as file object and read to string
        file = open(self.fullfile, "r")

        # Read file object to string
        text = file.read()

        # Close file object
        file.close()

        # Regex pattern
        pattern = re.compile(
            env.GET_META_PDF,
            re.MULTILINE,
        )

        metadata = pattern.finditer(text)

        return metadata

    def getMatchsHighlighted(self):
        # Open file as file object and read to string
        file = open(self.fullfile, "r")

        # Read file object to string
        text = file.read()

        # Close file object
        file.close()

        # Regex pattern
        pattern = re.compile(
            env.CAPTURE_HIGHLIGHTED,
            re.MULTILINE,
        )

        highlighteds = pattern.finditer(text)

        return highlighteds

    def convertHtmlToMarkdown(self, text, tag, comment, link):
        result = text
        text = text.replace(">", "")
        comment = comment

        if tag == "#h1":
            result = f"""

# {text}
---
"""
        elif tag == "#h2":
            result = f"""

## {text}
---
"""
        elif tag == "#h3":
            result = f"""

### {text}
---
"""
        elif tag == "#h4":
            result = f"""

#### {text}
---
"""
        elif tag == "#h5":
            result = f"""

##### {text}
---
"""
        elif tag == "#h6":
            result = f"""

###### {text}
---
"""
        elif tag == "#code":
            result = f"""
```{comment.replace(">","")}
    {text}
```
 """
        elif tag == "#br":
            result = f"""

{text}"""

        elif tag == "#quote":
            result = f"""
> {text}   {link.replace('show annotation','🔗')}

"""
        elif tag == "#p":
            result = f" {text} {comment.replace('>','')} "

        elif tag == "#cite":
            result = f"""
> [!CITE]
> {text} {link.replace('show annotation','🔗')}

"""
        elif tag == "#img":
            result = f"""
{text}
{comment.replace(">","")}  {link.replace('show annotation','🔗')}
"""

        elif tag == "#bold":
            result = f""" **{text}** {link.replace('show annotation','🔗')} """

        elif tag == "#danger":
            result = f""" {text}
> [!DANGER]
{comment} {link.replace('show annotation','🔗')}

"""

        elif tag == "#question":
            result = f""" {text}
> [!QUESTION]
{comment} {link.replace('show annotation','🔗')}

"""
        elif tag == "#li":
            result = f"""
* {text}
"""
        elif tag == "#li+":
            result = f"""
* {text} {comment.replace(">","")}
"""

        elif tag == "#em":
            result = f"""
*"{text}"*
"""

        elif tag == "#ref":  # Convierte el comentario en un link
            result = f" {link.replace('show annotation',comment)} "

        elif tag == "#sref":  # Convierte el texto subrayado en un link
            result = f""" {link.replace('show annotation',text)}
"""

        elif tag == "#href":  # Agrega al final del texto un link
            result = f"""{text} {link.replace('show annotation','🔗')}
"""

        elif tag == "#ignore": # Util para dar mas contexto en el libro, pero que se ignore en el resumen
            result = ""

        elif tag == "#add": # Util para dar mas contexto en el resumen, pero que se ignore en el libro.
            result = f"""
{comment.replace(">","")}
"""


        return f"{result} "

    def generateMarkdownFrom(self, highlighted, link, comment, tags):
        name = os.path.splitext(os.path.basename(self.fullfile))[0]
        fullname = f"{env.PATH_BOOKS}{name}.md".replace("(References)", "(Resumen)")
        result = self.convertHtmlToMarkdown(highlighted, tags, comment, link)
        file = open(fullname, "a")

        file.write(result)
        # Agregar comentarios propios
        print(f"TABL: {result}")
        if (
            comment.replace(">","")
            and tags != "#img"
            and tags != "#ignore"
            and tags != "#ref"
            and tags != "#add"
            and tags != "#p"
        ):
            file.write(
                f"""
> [!INFO]
{comment} {link.replace('show annotation','🔗')}

"""
            )
        file.close()

    def printMetaData(self):
        name = os.path.splitext(os.path.basename(self.fullfile))[0]
        fullname = f"{env.PATH_BOOKS}{name}.md".replace("(References)", "(Resumen)")
        result = self.getMetaData()
        for data in result:
            file = open(fullname, "a")
            file.write(
                f"""
---{data[1].replace(f"annotation-target: {data[2]}","").replace("(References)","(Resumen)").replace("tags: ","tags: book, ")}
---
PDF: [[{data[2].strip()}]]
"""
            )
            file.close()

    def convert(self):
        highlighteds = self.getMatchsHighlighted()

        name = os.path.splitext(os.path.basename(self.fullfile))[0]
        fullname = f"{env.PATH_BOOKS}{name}.md".replace("(References)", "(Resumen)")
        if os.path.exists(fullname):
            os.remove(fullname)

        self.printMetaData()

        for note in highlighteds:
            note = note.group(1)
            highlighted = self.getMatchs(env.GET_HIGHLIGHTED, note)
            link = self.getLink(note).replace("notes/", "", 1)
            comment = (
                self.getMatchs(env.GET_COMMENT, note)[0].rstrip()
            )
            print(f"NOTE: {note}")
            print(f"COMENT: *{comment}*")
            tags = self.getMatchs(env.GET_TAGS, note)

            self.generateMarkdownFrom(highlighted, link, comment, tags)
