import os
import json
from datetime import datetime
from backend import basic_statistics
from backend import file_loading
from backend import word_analysis
from backend import sentence_analysis
from backend import character_analysis
from backend import lix

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY_DIR = os.path.join(BASE_DIR, "library")
DATABASE_DIR = os.path.join(BASE_DIR, "backend", "database")

# JSON only allows string keys, so these dictionaries get string keys when
# they are saved. They are converted back to int keys when read from the cache.
INT_KEY_FIELDS = ("sentence_len_distribution", "Word_length_distribution")


def list_books():
    return file_loading.check_library()


def choose_books(choice):
    books = list_books()
    choice = choice.strip()

    if choice.isdigit():
        number = int(choice)
        if 1 <= number <= len(books):
            return books[number - 1]
        return None

    for book in books:
        if choice.lower() in (book.lower(), book.lower().removesuffix(".txt")):
            return book
    return None


def process_book(filename):
    """Analyses a book line by line and returns the results as a dictionary."""
    path = os.path.join(LIBRARY_DIR, filename)

    character_count_space = character_count_nospace = 0
    line_count = word_count = sentence_count = 0
    upper_case_count = lower_case_count = digit_count = 0
    paragraph_count = 1
    longest_sentence = shortest_sentence = current_sentence = ""
    dict_characters = {}
    dict_punctuations = {}
    dict_sentence_len = {}
    dict_words = {}

    with open(path, "r", encoding="utf-8") as book:
        for line in book:
            line_count += 1
            digit_count += sum(char.isdigit() for char in line)

            words_in_line = basic_statistics.line_to_words(line)

            if words_in_line != [""]:
                word_count += len(words_in_line)

            if words_in_line == [""]:
                paragraph_count += 1

            chars_with, chars_without = basic_statistics.count_characters(line)
            character_count_space += int(chars_with)
            character_count_nospace += int(chars_without)

            sentences, current_sentence, sentences_in_line = sentence_analysis.sentences_in_line(line, current_sentence)
            sentence_count += sentences_in_line
            longest_sentence = sentence_analysis.long_sentence(longest_sentence, sentences)
            shortest_sentence = sentence_analysis.short_sentence(shortest_sentence, sentences)
            dict_sentence_len = sentence_analysis.sentence_len_distribution(sentences, dict_sentence_len)

            dict_characters = character_analysis.letter_frequency(words_in_line, dict_characters)
            dict_punctuations = character_analysis.punctuation_statistics(words_in_line, dict_punctuations)
            lower_case_count, upper_case_count = character_analysis.case_distribution(words_in_line, lower_case_count, upper_case_count)

            dict_words = word_analysis.count_words(words_in_line, dict_words)

    # All results are stored in one dictionary which is returned to the caller.
    data = {
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "number_of_lines": line_count,
        "number_of_words": word_count,
        "number_of_characters_with_spaces": character_count_space,
        "number_of_characters": character_count_nospace,
        "number_of_paragraphs": paragraph_count,
        "avg_word_per_line": basic_statistics.words_per_line(
            word_count, line_count),
        "avg_character_per_word": basic_statistics.characters_per_word(
            character_count_nospace, word_count),
        "number_of_sentences": sentence_count,
        "avg_word_per_sentences": sentence_analysis.words_per_sentence(
            word_count, sentence_count),
        "longest_sentence": longest_sentence,
        "shortest_sentence": shortest_sentence,
        "sentence_len_distribution": dict(sorted(dict_sentence_len.items())),
        "character_frequency": dict(sorted(dict_characters.items())),
        "punctuation_frequency": dict(sorted(dict_punctuations.items())),
        "number_of_lowercase": lower_case_count,
        "number_of_uppercase": upper_case_count,
        "number_of_digits": digit_count,
        "Most_common_words": word_analysis.most_common_words(dict_words),
        "Shortest_word": word_analysis.shortest_word(dict_words),
        "Longest_word": word_analysis.longest_word(dict_words),
        "Word_length_distribution": word_analysis.word_length_distribution(dict_words),
        "unique_words": word_analysis.unique_words(dict_words),
        "Words_appearing_once": len(word_analysis.words_appearing_only_once(dict_words)),
    }
    return data


# Finds the book's cache file in the database directory.
def cache_path(filename):
    name = os.path.splitext(filename)[0]
    return os.path.join(DATABASE_DIR, f"{name}.json")


# JSON turns int keys into strings, so convert them back after reading the cache.
def restore_int_keys(data):
    for field in INT_KEY_FIELDS:
        data[field] = {int(key): value for key, value in data[field].items()}
    return data


# Reads the cached data if it exists and the book has not been changed since. If not, returns None.
def read_cache(filename):
    book_path = os.path.join(LIBRARY_DIR, filename)
    try:
        with open(cache_path(filename), "r", encoding="utf-8") as f:
            saved = json.load(f)
        # A cache saved before the digit count existed is treated as outdated.
        if saved["source_mtime"] == os.path.getmtime(book_path) and "number_of_digits" in saved["data"]:
            return restore_int_keys(saved["data"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
        pass
    return None


# Saves the analysis results to the database directory for future use.
def save_cache(filename, data):
    os.makedirs(DATABASE_DIR, exist_ok=True)
    book_path = os.path.join(LIBRARY_DIR, filename)
    saved = {
        "source_mtime": os.path.getmtime(book_path),
        "data": data,
    }
    with open(cache_path(filename), "w", encoding="utf-8") as f:
        json.dump(saved, f, ensure_ascii=False)


# Returns (data, from_cache). Uses the cache if it is up to date,
# otherwise analyses the book and saves the result to the cache.
def load_book(filename):
    data = read_cache(filename)
    if data is not None:
        return data, True

    data = process_book(filename)
    save_cache(filename, data)
    return data, False


def get_line_count(data):
    return data["number_of_lines"]


def get_analysis_date(data):
    return data.get("analyzed_at")


def get_basic_stats(data):
    return {
        "Lines": data["number_of_lines"],
        "Paragraphs": data["number_of_paragraphs"],
        "Sentences": data["number_of_sentences"],
        "Words": data["number_of_words"],
        "Unique Words": data["unique_words"],
        "Characters (with spaces)": data["number_of_characters_with_spaces"],
        "Characters (without spaces)": data["number_of_characters"],
        "Average words per line": data["avg_word_per_line"],
        "Average word length": data["avg_character_per_word"],
        "Average words per sentence": data["avg_word_per_sentences"],
    }


def get_word_frequency(data):
    return {
        "Most_common_words": data["Most_common_words"],
        "Shortest_word": data["Shortest_word"],
        "Longest_word": data["Longest_word"],
        "Average_word_length": data["avg_character_per_word"],
        "Word_length_distribution": data["Word_length_distribution"],
        "Words_appearing_once": data["Words_appearing_once"],
    }


def get_sentence_stats(data):
    return {
        "Total sentences": data["number_of_sentences"],
        "Average words per sentence": data["avg_word_per_sentences"],
        "Longest sentence": data["longest_sentence"],
        "Shortest sentence": data["shortest_sentence"],
        "Sentence length distribution": data["sentence_len_distribution"],
    }


def get_character_stats(data):
    return {
        "Characters (with spaces)": data["number_of_characters_with_spaces"],
        "Characters (without spaces)": data["number_of_characters"],
        "Lowercase letters": data["number_of_lowercase"],
        "Uppercase letters": data["number_of_uppercase"],
        "Letter frequency": data["character_frequency"],
        "Punctuation frequency": data["punctuation_frequency"],
    }


def lix_value(data):
    long_word_count = lix.long_words_count(data["Word_length_distribution"])
    return lix.lix_stat(data["number_of_words"], data["number_of_sentences"], long_word_count)


REPORT_WIDTH = 60


def percent(part, whole):
    return part / whole * 100 if whole else 0


# Returns the `limit` biggest (key, count) pairs, highest count first.
def top_items(distribution, limit):
    return sorted(distribution.items(), key=lambda item: (-item[1], item[0]))[:limit]


# Puts a sentence on one line so it does not break the layout of the report.
def one_line(text):
    return " ".join(text.split())


def section(title, width):
    return ["", title, "-" * width]


# Builds the complete text report for one analysed book and returns it as a string.
def build_report(data, filename):
    letters = data["number_of_lowercase"] + data["number_of_uppercase"]
    total_chars = data["number_of_characters_with_spaces"]
    spaces = total_chars - data["number_of_characters"]
    punctuation = sum(data["punctuation_frequency"].values())
    digits = data["number_of_digits"]
    letter_total = sum(data["character_frequency"].values())
    longest = data["longest_sentence"]
    shortest = data["shortest_sentence"]

    lines = ["=" * REPORT_WIDTH, "TEXT ANALYSIS RESULTS", "=" * REPORT_WIDTH,
             f"File analysed: {filename}",
             f"Analysis date: {data['analyzed_at']}"]

    lines += section("BASIC STATISTICS", 20)
    lines += [f"Lines: {data['number_of_lines']:,}",
              f"Paragraphs: {data['number_of_paragraphs']:,}",
              f"Sentences: {data['number_of_sentences']:,}",
              f"Words: {data['number_of_words']:,}",
              f"Unique words: {data['unique_words']:,}",
              f"Characters (with spaces): {total_chars:,}",
              f"Characters (without spaces): {data['number_of_characters']:,}",
              f"Average words per line: {data['avg_word_per_line']:.1f}",
              f"Average word length: {data['avg_character_per_word']:.1f} characters",
              f"Average words per sentence: {data['avg_word_per_sentences']:.1f}"]

    lines += section("TOP 10 MOST COMMON WORDS", 30)
    for i, (word, count, pct) in enumerate(data["Most_common_words"][:10], start=1):
        lines.append(f"{i:>2}. {word:<10}{count:>8,} times ({pct:>4.1f}%)")

    lines += section("WORD STATISTICS", 20)
    lines += [f"Shortest word: {len(data['Shortest_word'])} characters",
              f"Longest word: {len(data['Longest_word'])} characters",
              f"Words appearing only once: {data['Words_appearing_once']:,}"]

    lines += section("SENTENCE STATISTICS", 25)
    lines += [f"Total sentences: {data['number_of_sentences']:,}",
              f"Shortest sentence: {len(shortest.split())} words",
              f"Longest sentence: {len(longest.split())} words",
              f"Shortest sentence text: {one_line(shortest)}",
              f"Longest sentence text: {one_line(longest)}"]

    lines += section("CHARACTER STATISTICS", 25)
    lines += [f"Letters: {letters:,} ({percent(letters, total_chars):.1f}%)",
              f"Digits: {digits:,} ({percent(digits, total_chars):.1f}%)",
              f"Spaces: {spaces:,} ({percent(spaces, total_chars):.1f}%)",
              f"Punctuation: {punctuation:,} ({percent(punctuation, total_chars):.1f}%)"]

    lines += section("TOP 10 MOST COMMON LETTERS", 30)
    for i, (letter, count) in enumerate(top_items(data["character_frequency"], 10), start=1):
        lines.append(f"{i:>2}. '{letter}' - {count:>8,} times ({percent(count, letter_total):.1f}%)")

    lines += section("READABILITY", 20)
    lines.append(f"LIX readability score: {lix_value(data)}")

    lines += ["", "=" * REPORT_WIDTH, "End of Analysis Report", "=" * REPORT_WIDTH]
    return "\n".join(lines)


# Exports the results to a JSON file named after the book, including the
# top 10 most common words and the LIX score. Returns the path of the file.
def export_results(data, filename):
    os.makedirs(DATABASE_DIR, exist_ok=True)
    name = os.path.splitext(filename)[0]
    out_path = os.path.join(DATABASE_DIR, f"{name}_results.json")

    export = dict(data)
    export["Most_common_words"] = export["Most_common_words"][:10]
    export["lix"] = lix_value(data)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)
    return out_path