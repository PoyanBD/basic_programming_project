import glob
import os

LIBRARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "library")


def get_path(file_name):
    return os.path.join(LIBRARY, file_name)


def check_library():
    pattern = os.path.join(LIBRARY, "*.txt")
    return sorted(os.path.basename(book) for book in glob.glob(pattern))


def search_file(name):
    name = name.replace("text, ", "").strip()
    if not name.endswith(".txt"):
        name += ".txt"
    path = get_path(name)
    if os.path.exists(path):
        return path
    return None