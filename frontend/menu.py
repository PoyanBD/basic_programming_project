import os
import json
from backend import backend

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show(data, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            print(" " * indent + f"{key}:")
            show(value, indent + 2)
        else:
            print(" " * indent + f"{key}: {value}")

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
        
        try:
            n = int(input("\nEnter a number (1-7) to select a menu option, or 7 to exit:"))
        except ValueError:
            print("Please enter a number next time.")
            input("\nPress Enter to continue...")
            n = 0
            continue
    
    
        if n == 1:
            print("\n--- File Selection ---")
            books = backend.list_books()

            if not books:
                print("No books found")
            else:
                print("Available text files:")
                for i, book in enumerate(books, start=1):
                    print(f"{i}. {book}")

                choice = input("\nEnter a number or file name (0 to cancel): ")

                if choice.strip() == "0":
                    print("Cancelled.")
                else:
                    picked = backend.choose_books(choice)
                    if picked is None:
                        print("\nFile does not exist.")
                        input("\nPress Enter to continue...")
                    else:
                        current_file = picked
                        print(f'\nLoading {current_file}...')
                        from_cache = backend.load_book(current_file)
                        if from_cache:
                            print("Loaded saved analysis (no need to analyse again).")
                        else:
                            print("Analysis complete and saved.")
                        print(f'Processed {backend.get_line_count()} lines')
                        input("\nPress Enter to continue...")
           
        elif n in (2, 3, 4, 5, 6) and not backend.is_loaded():
            print("\nLoad a file first (option 1).")
            input("\nPress Enter to continue...")
                
        elif n == 2:
            print(f'\n--- Basic Statistics for "{current_file}" ---')
            show(backend.get_basic_stats())
            
            print("\nGenerating basic statistics visualisation...")
            input("\nPress Enter to continue...")
            
        elif n == 3:
            print(f'\n--- Word Frequency Analysis for "{current_file}" ---')
            stats = backend.get_word_frequency()

            print("Top 10 most common words:")
            for i, (word, count, percentage) in enumerate(stats["Most_common_words"][:10], start=1):
                print(f"{i}. {word:<10}{count} ({percentage:.1f}%)")

            print("\nWord length statistics:")
            print(f"    Shortest word: {len(stats['Shortest_word'])} characters")
            print(f"    Longest word: {len(stats['Longest_word'])} characters")
            print(f"    Average word length: {stats['Average_word_length']:.1f} characters")
            print(f"Words appearing once: {stats['Words_appearing_once']}")

            print("\nWord length distribution (top 5):")
            common_lengths = sorted(stats["Word_length_distribution"].items(),
                                    key=lambda item: (-item[1], item[0]))[:5]
            for i, (word_len, count) in enumerate(common_lengths, start=1):
                print(f"{i}. {word_len} characters: {count} words")

            print("\nGenerating word frequency visualisation...")
            input("\nPress Enter to continue...")
            
        elif n == 4:
            print(f'\n--- Sentence Analysis for "{current_file}" ---')
            stats = backend.get_sentence_stats()
            print(f"Total sentences: {stats['Total sentences']}")
            print(f"Average words per sentence: {stats['Average words per sentence']:.1f}")
            print(f"Longest sentence: {len(stats['Longest sentence'])} words")
            print(f"Shortest sentence: {len(stats['Shortest sentence'])} words")

            print(f"\nShortest sentence text: {stats['Shortest sentence']}")
            print(f"Longest sentence text: {stats['Longest sentence']}")
            
            print("\nSentence length distribution (top 5):")
            common = sorted(stats["Sentence length distribution"].items(),
                            key=lambda item: (-item[1], item[0]))[:5]
            for i, (sentence_len, count) in enumerate(common, start=1):
                print(f"{i}. {sentence_len} words: {count} sentences")

            print("\nGenerating sentence analysis visualisation...")
            input("\nPress Enter to continue...")
            
        elif n == 5:
            print(f'\n--- Character Analysis for "{current_file}" ---')
            stats = backend.get_character_stats()
            print("Character type distribution:")
        
            print("\nMost Common Letters (top 10):")
            common = sorted(stats["Letter frequency"].items(),
                            key=lambda item: (-item[1], item[0]))[:10]
            for i, (char, count) in enumerate(common, start=1):
                print(f"{i}. {char}: {count}")
                
            print("\nGenerating character analysis visualisation...")
            input("\nPress Enter to continue...")
            
        elif n == 6:
            print(f'\n--- Export Results for "{current_file}" ---')
            path = backend.export_results()
            print(f"Results saved to {path}")
            input("\nPress Enter to continue...")
            
        elif n == 7:
            print("Thank you for using Text Analyser!")
        else:
            print("Invalid option. Please enter a number between 1 and 7.")
            input("\nPress Enter to continue...")