import sys
import os
import json

#sys.path.append(os.path.join(os.getcwd(), "basic_programming_project"))
sys.path.append('../basic_programming_project/backend')

import back_end
import file_loading


def menu():
    n = 0
    current_file = None

    while n != 7:

        print("=" * 50)
        print(f'{"TEXT ANALYSER":^50}')
        print("=" * 50)

        print(
            " 1. Book selection \n 2. Display basic statistics \n 3. Word frequency analysis \n 4. Sentence analysis \n 5. Character analysis \n 6. Export results \n 7. Exit"
        )
        print("=" * 50)

        if current_file:
            print(f'Current file: {current_file}')
            back_end.process_book(current_file)
        else:
            print("No file loaded")

        with open("../basic_programming_project/backend/database/data.json",
                  "r") as file:
            data = json.load(file)

        n = int(
            input(
                "Enter a number (1-7) to select a menu option, or 7 to exit: ")
        )

        if n == 1:
            print("--- File Selection ---")
            books = file_loading.check_library()

            if not books:
                print("No books found")
            else:
                for i, book in enumerate(books, start=1):
                    print(f'{i}. {book}')

                try:
                    pick = input(
                        "Enter the number of the file to load or write the name of the book (0 to cancel): "
                    )
                    pick = int(pick)
                except ValueError:
                    current_file = file_loading.search_file(pick)
                else:

                    if pick == 0:
                        print("cancelled")
                    elif 1 <= pick <= len(books):
                        current_file = file_loading.search_file(books[pick -
                                                                      1])

                    else:
                        print("That number isn't in the list")

        elif n == 2:
            print(f"--- Basic Statistics for {current_file}---")
            print("Lines:", data["number_of_lines"])
            print("Paragraphs:", data["number_of_paragraph"])
            print("Sentences:", data["number_of_sentences"])
            print("Words:", data["number_of_words"])
            print("Unique words:", "not implemented")
            print("Characters (with spaces):",
                  data["number_of_characters_with_spaces"])
            print("Characters (without spaces):", data["number_of_characters"])
            print("Average words per line:", data["avg_word_per_line"])
            print("Average word length:", "not implemented")
            print("Average words per sentence:",
                  data["avg_word_per_sentences"])
        elif n == 3:
            print("You selected option 3: Word frequency analysis.")
        elif n == 4:
            print("You selected option 4: Sentence analysis.")
        elif n == 5:
            print("You selected option 5: Character analysis.")
        elif n == 6:
            print("You selected option 6: Export results.")
        elif n == 7:
            print("Exiting the program. Goodbye!")
        else:
            print("Invalid option. Please enter a number between 1 and 7.")


menu()
