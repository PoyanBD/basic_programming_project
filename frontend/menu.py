import os
from backend import backend
from frontend import visualisations


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show(data, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            print(" " * indent + f'{key}:')
            show(value, indent + 2)
        else:
            print(" " * indent + f'{key}: {value}')


def print_menu(current_file):
    print("=" * 50)
    print(f'{"TEXT ANALYSER":^50}')
    print("=" * 50)
    print(" 1. Load text file \n 2. Display basic statistics \n 3. Word frequency analysis \n 4. Sentence analysis \n 5. Character analysis \n 6. Export results \n 7. Exit")
    print("=" * 50)

    if current_file:
        print(f'Current file: {current_file}')
    else:
        print("No file loaded")


def sort_by_count(distribution, limit):
    """Returns the `limit` biggest (key, count) pairs, highest count first."""
    return sorted(distribution.items(), key=lambda item: (-item[1], item[0]))[:limit]


# Option 1. Returns the (possibly new) current file name and data.
def load_file(current_file, data):
    print("\n--- File Selection ---")
    books = backend.list_books()

    if not books:
        print("No books found")
        return current_file, data

    print("Available text files:")
    for i, book in enumerate(books, start=1):
        print(f'{i}. {book}')

    choice = input("\nEnter a number or file name (0 to cancel): ")

    if choice.strip() == "0":
        print("Cancelled.")
        return current_file, data

    picked = backend.choose_books(choice)
    if picked is None:
        print("\nFile does not exist.")
        return current_file, data

    print(f'\nLoading {picked}...')
    new_data, from_cache = backend.load_book(picked)
    if from_cache:
        print("Loaded saved analysis (no need to analyse again).")
    else:
        print("Analysis complete and saved.")
    print(f'Processed {backend.get_line_count(new_data)} lines')
    return picked, new_data


# Option 2
def show_basic_stats(data, current_file):
    print(f'\n--- Basic Statistics for "{current_file}" ---')
    stats = backend.get_basic_stats(data)
    show(stats)
    print(f'\nLIX Readability Score: {backend.lix_value(data)}')

    print("\nGenerating basic statistics visualisation...")
    visualisations.text_composition(stats["Lines"], stats["Sentences"], stats["Unique Words"], stats["Paragraphs"])
    visualisations.character_type_distribution(stats["Characters (with spaces)"], stats["Characters (without spaces)"])


# Option 3
def show_word_analysis(data, current_file):
    print(f'\n--- Word Frequency Analysis for "{current_file}" ---')
    stats = backend.get_word_frequency(data)

    print("Top 10 most common words:")
    for i, (word, count, percentage) in enumerate(stats["Most_common_words"][:10], start=1):
        print(f'{i}. {word:<10}{count} ({percentage:.1f}%)')

    print("\nWord length statistics:")
    print(f'    Shortest word: {len(stats["Shortest_word"])} characters')
    print(f'    Longest word: {len(stats["Longest_word"])} characters')
    print(f'    Average word length: {stats["Average_word_length"]:.1f} characters')
    print(f'Words appearing once: {stats["Words_appearing_once"]}')

    print("\nWord length distribution (top 5):")
    for i, (word_len, count) in enumerate(sort_by_count(stats["Word_length_distribution"], 5), start=1):
        print(f'{i}. {word_len} characters: {count} words')

    print("\nGenerating word frequency visualisation...")
    visualisations.common_word_frequency(stats["Most_common_words"][:10])
    visualisations.word_length_distribution(stats["Word_length_distribution"])


# Option 4
def show_sentence_analysis(data, current_file):
    print(f'\n--- Sentence Analysis for "{current_file}" ---')
    stats = backend.get_sentence_stats(data)
    longest = stats["Longest sentence"]
    shortest = stats["Shortest sentence"]

    print(f'Total sentences: {stats["Total sentences"]}')
    print(f'Average words per sentence: {stats["Average words per sentence"]:.1f}')
    print(f'Longest sentence: {len(longest.split())} words')
    print(f'Shortest sentence: {len(shortest.split())} words')

    print(f'\nShortest sentence text: {shortest}')
    print(f'Longest sentence text: {longest}')

    print("\nSentence length distribution (top 5):")
    common = sort_by_count(stats["Sentence length distribution"], 5)
    for i, (sentence_len, count) in enumerate(common, start=1):
        print(f'{i}. {sentence_len} words: {count} sentences')

    print("\nGenerating sentence analysis visualisation...")
    visualisations.sentence_length_distribution(stats["Sentence length distribution"])
    visualisations.sentence_length_frequency(common)


# Option 5
def show_character_analysis(data, current_file):
    print(f'\n--- Character Analysis for "{current_file}" ---')
    stats = backend.get_character_stats(data)

    print("Character type distribution:")
    print(f'    Lowercase letters: {stats["Lowercase letters"]}')
    print(f'    Uppercase letters: {stats["Uppercase letters"]}')
    print(f'    Punctuation marks: {sum(stats["Punctuation frequency"].values())}')

    print("\nMost Common Letters (top 10):")
    common = sort_by_count(stats["Letter frequency"], 10)
    for i, (char, count) in enumerate(common, start=1):
        print(f'{i}. {char}: {count}')

    print("\nGenerating character analysis visualisation...")
    visualisations.character_frequency_visual(stats["Letter frequency"])
    visualisations.character_most_common(common)


# Option 6
def export_analysis(data, current_file):
    report = backend.build_report(data, current_file)
    print(report)

    path = backend.export_results(data, current_file)
    print(f'\nResults saved to {path}')


# Menu options that need a loaded book. Each takes (data, current_file).
ACTIONS = {
    2: show_basic_stats,
    3: show_word_analysis,
    4: show_sentence_analysis,
    5: show_character_analysis,
    6: export_analysis,
}


def menu():
    current_file = None
    data = None  # analysis of the loaded book, passed to the functions that need it

    while True:
        clear_screen()
        print_menu(current_file)

        try:
            n = int(input("\nEnter a number (1-7) to select a menu option, or 7 to exit: "))
        except ValueError:
            print("Please enter a number.")
            input("\nPress Enter to continue...")
            continue

        if n == 7:
            print("Thank you for using Text Analyser!")
            break
        elif n == 1:
            current_file, data = load_file(current_file, data)
        elif n in ACTIONS:
            if data is None:
                print("\nLoad a file first (option 1).")
            else:
                ACTIONS[n](data, current_file)
        else:
            print("Invalid option. Please enter a number between 1 and 7.")

        input("\nPress Enter to continue...")