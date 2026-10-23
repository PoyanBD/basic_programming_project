import os
import json
from backend import basic_statistics
from backend import file_loading
from backend import word_analysis
from backend import sentence_analysis
from backend import character_analysis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY_DIR = os.path.join(BASE_DIR, "library")
DATABASE_DIR = os.path.join(BASE_DIR, "backend", "database")

results = {}


def list_books():
    return file_loading.check_library()


def process_book(filename):
    global results

    path = os.path.join(LIBRARY_DIR, filename)

    character_count_space = character_count_nospace = 0
    line_count = word_count = sentence_count = 0
    upper_case_count = lower_case_count = 0
    longest_sentence = shortest_sentence = current_sentence = ""
    dict_characters = {}
    dict_punctuations = {}
    dict_sentence_len = {}
    counts = {}

    with open(path, "r", encoding="utf-8") as book:
        for line in book:
            line_count += 1

            words_in_line = basic_statistics.line_to_words(line)
            if words_in_line != [""]:
                word_count += len(words_in_line)

            chars_with, chars_without = basic_statistics.count_characters(line)
            character_count_space += int(chars_with)
            character_count_nospace += int(chars_without)

            sentence_count += sentence_analysis.sentence_counter(line)
            sentences, current_sentence = sentence_analysis.sentences_in_line(
                line, current_sentence)
            longest_sentence = sentence_analysis.long_sentence(
                longest_sentence, sentences)
            shortest_sentence = sentence_analysis.short_sentence(
                shortest_sentence, sentences)
            dict_sentence_len = sentence_analysis.sentence_len_distribution(
                sentences, dict_sentence_len)

            dict_characters = character_analysis.letter_frequency(
                words_in_line, dict_characters)
            dict_punctuations = character_analysis.punctuation_statistics(
                words_in_line, dict_punctuations)
            lower_case_count, upper_case_count = character_analysis.case_distribution(
                words_in_line, lower_case_count, upper_case_count)

            # for top10()
            for word in line.split():
                word = word.lower().strip(".,!?;:\"'()[]{}")
                counts[word] = counts.get(word, 0) + 1

    data = {
        "number_of_lines": line_count,
        "number_of_words": word_count,
        "number_of_characters_with_spaces": character_count_space,
        "number_of_characters": character_count_nospace,
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
        "unique_words": word_analysis.unique_words(counts),
        "words_appearing_once": len(word_analysis.words_appearing_only_once(counts))
    }

    results = {"filename": filename, "data": data, "counts": counts}


def is_loaded():
    return bool(results)


def get_basic_stats():
    d = results["data"]
    return {
        "lines": d["number_of_lines"],
        "words": d["number_of_words"],
        "characters (with spaces)": d["number_of_characters_with_spaces"],
        "characters (no spaces)": d["number_of_characters"],
        "avg words per line": d["avg_word_per_line"],
        "avg characters per word": d["avg_character_per_word"],
    }


def get_word_frequency():
    d = results["data"]
    return {
        "top 10": word_analysis.top10(results["counts"]),
        "unique words": d["unique_words"],
        "words appearing once": d["words_appearing_once"],
    }


def get_sentence_stats():
    d = results["data"]
    return {
        "sentence count": d["number_of_sentences"],
        "avg words per sentence": d["avg_word_per_sentences"],
        "longest sentence": d["longest_sentence"],
        "shortest sentence": d["shortest_sentence"],
        "sentence length distribution": d["sentence_len_distribution"],
    }


def get_character_stats():
    d = results["data"]
    return {
        "with spaces": d["number_of_characters_with_spaces"],
        "without spaces": d["number_of_characters"],
        "lowercase letters": d["number_of_lowercase"],
        "uppercase letters": d["number_of_uppercase"],
        "letter frequency": d["character_frequency"],
        "punctuation frequency": d["punctuation_frequency"],
    }


def export_results():
    """Write the analysis to backend/database/data.json and return the path."""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    out_path = os.path.join(DATABASE_DIR, "data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results["data"], f, ensure_ascii=False, indent=2)
    return out_path