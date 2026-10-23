import os
from backend import backend

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show(data, indent=0):
    for k, v in data.items():
        if isinstance(v, dict):
            print(" " * indent + f"{k}:")
            show(v, indent + 2)
        else:
            print(" " * indent + f"{k}: {v}")

def menu(): 
    n = 0
    current_file = None
    
    while n != 7:
        
        clear_screen()
        
        print("="*50)
        print(f'{"TEXT ANALYSER":^50}')
        print("="*50)
    
        print(" 1. Load text file \n 2. Display basic statistics \n 3. Word frequency analysis \n 4. Sentence analysis \n 5. Character analysis \n 6. Export results \n 7. Exit")
        print("="*50)

        if current_file:
            print(f'Current file: {current_file}')
        else: 
            print("No file loaded")
        
        n = int(input("Enter a number (1-7) to select a menu option, or 7 to exit: "))
    
    
        if n == 1:
            print("--- File Selection ---")
            books = backend.list_books()

            if not books:
                print("No books found")
            else:
                for i, book in enumerate(books, start=1):
                    print(f'{i}. {book}')

                try:
                    pick = int(input("Enter the number of the file to load (0 to cancel): "))
                except ValueError:
                    print("Pleae enter a number ")
                else:
                    if pick == 0:
                        print("cancelled")
                    elif 1 <= pick <= len(books):
                        current_file = books[pick - 1]
                        backend.process_book(current_file)
                    else:
                        print("That number isn't in the list")
                
        elif n == 2:
            print("You selected option 2: Display basic statistics.")
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