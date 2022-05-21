# PATH_BOOKS = "./notes/🗄️ Resources/Books/"
PATH_ANNOTATIONS = "./notes/attachments/Books/References"
PATH_BOOKS = "./notes/attachments/Books/Abstracts/"

GET_META_PDF = "---\n((?:(?:.|\n)*)annotation-target: *(.*)(?:(?:.|\n)*))\n---"

ALL_FILES = True

GET_HIGHLIGHTED = "%% ==(.*?)== %%"

GET_TAGS = "%%TAGS%%\n?>(.+)"

GET_COMMENT = "\>\%\%COMMENT\%\%\n((:?.|\n)*?)\>\%\%TAGS\%\%"

GET_LINK = "\>\%\%LINK\%\%\[\[(.+)"

CAPTURE_HIGHLIGHTED = ">%%((?:.|\n)*?)\^\w{4,20}$"
