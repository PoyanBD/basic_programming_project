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


def search_file():
    file_name = str(input("Enter file name: "))
    if glob.glob(f"../basic_programming_project/library/{file_name}.txt"):
        return glob.glob(
            f"../basic_programming_project/library/{file_name}.txt")
    else:
        print("File Does not exist")


#print(check_library())
#process_book("../basic_programming_project/library/test.txt")
#print(glob.glob("../basic_programming_project/library/*.txt"))
