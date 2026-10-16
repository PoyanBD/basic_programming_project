import glob
import re


def check_library():
    book_list = []
    file_list = glob.glob("../basic_programming_project/library/*.txt")
    for book in file_list:
      title = re.search(r"\\.*\.txt",book).group()[1:]
      book_list.append(title)
    return book_list


def search_file():
    file_name = str(input("Enter file name: "))
    if glob.glob(f"../basic_programming_project/library/{file_name}.txt"):
      return glob.glob(f"../basic_programming_project/library/{file_name}.txt")
    else:
      print("File Does not exist")

def process_book(path):
    with open(path,"r") as book:
       for line in book:
          print(line)

process_book("../basic_programming_project/library/test.txt")