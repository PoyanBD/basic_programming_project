import glob
import os

LIBRARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "library")

def get_path(file_name):
    return os.path.join(LIBRARY, file_name)

def check_library():
    book_list = []
    file_list = glob.glob("../basic_programming_project/library/*.txt")
    for book in file_list:
        title = os.path.basename(book)
        book_list.append(title)
    return book_list


def search_file(name):
    name = name.replace("text, ", "")
    file_name = str(name)
    if glob.glob(f"../basic_programming_project/library/{file_name}.txt"):
        return (f"../basic_programming_project/library/{file_name}.txt")
    else:
        print("File Does not exist")