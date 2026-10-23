import glob
import os


def check_library():
    book_list = []
    file_list = glob.glob("../basic_programming_project/library/*.txt")
    for book in file_list:
        title = os.path.basename(book)
        book_list.append(title)
    return book_list


def search_file():
    file_name = str(input("Enter file name: "))
    if glob.glob(f"../basic_programming_project/library/{file_name}.txt"):
        return glob.glob(
            f"../basic_programming_project/library/{file_name}.txt")
    else:
        print("File Does not exist")
