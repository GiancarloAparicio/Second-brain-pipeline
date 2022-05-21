import os
import env
import Resumen

print("start")
if not env.ALL_FILES:
    os.system(
        "printf \"$(git status -sb | grep './notes/attachments/Annotator' | awk '{$1=\"\"; print $0}' | tr -d '\"' )\" > annotator.files.txt"
    )

else:
    os.system(
        f"fd --full-path {env.PATH_ANNOTATIONS} -t f | cut -c3- > annotator.files.txt"
    )

modified_files = open("annotator.files.txt", mode="r", encoding="utf-8")

for file in modified_files:
    file = file.strip()
    print(f"Convert: {file}")

    if os.path.exists(file):
        resumen = Resumen.Resumen(file)
        resumen.convert()

os.remove("annotator.files.txt")
