import os
import sys


def optimice_png():
    os.system(
        "printf \"$(git status -sb | grep '.png' "
        "| awk '{$1=\"\"; print $0}' | tr -d '\"' )\" > unused.files.txt"
    )
    unused_files = open("unused.files.txt", mode="r", encoding="utf-8")

    for photo in unused_files:
        photo = photo.strip()

        if os.path.exists(f"{photo}"):
            print(f"Optimice: {photo}")
            os.system(f"optipng --quiet -o3 {photo}")

    os.remove("unused.files.txt")


def optimice_jpg():
    os.system(
        "printf \"$(git status -sb | grep -E '.jpg|.jpeg' "
        "| awk '{$1=\"\"; print $0}' | tr -d '\"' )\" > unused.files.txt"
    )
    unused_files = open("unused.files.txt", mode="r", encoding="utf-8")

    for photo in unused_files:
        photo = photo.strip()

        if os.path.exists(f"{photo}"):
            print(f"Optimice: {photo}")
            os.system(f"jpegoptim –strip-all -m80 {photo}")

    os.remove("unused.files.txt")


def main(argv):
    optimice_png()
    optimice_jpg()


if __name__ == "__main__":
    main(sys.argv[1:])
