import glob
import os


def check_library():
    book_list = []
    file_list = glob.glob("../basic_programming_project/library/*.txt")
    for book in file_list:
        title = os.path.basename(book)
        book_list.append(title)
    return book_list


def search_file(name):
    name = name.replace(".txt", "")
    file_name = str(name)
    if glob.glob(f"../basic_programming_project/library/{file_name}.txt"):
        return (f"../basic_programming_project/library/{file_name}.txt")
    else:
        print("File Does not exist")
