import sys

sys.path.insert(0, "/home/jovyan/basic_programming_project")

from backend.file_loading import check_library, search_file, process_book

def menu(): 
    n = 0
    current_file = None
    
    while n != 7:
        
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
            print(check_library())
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