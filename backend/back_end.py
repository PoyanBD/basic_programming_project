import basic_statistics
import file_loading
import word_analysis
import sentence_analysis
import character_analysis

import json


def process_book(path):
    character_count_space = 0
    character_count_nospace = 0
    line_count = 0
    word_count = 0
    sentence_count = 0
    upper_case_count = 0
    lower_case_count = 0
    longest_sentence = ""
    shortest_sentence = ""
    current_sentence = ""
    sentences = []
    words_in_line = []
    dict_characters = {}
    dict_punctuations = {}
    dict_sentence_len = {}
    counts = {}
    data = {}

    with open(path, "r", encoding="utf-8") as book:
        for line in book:
            line_count += 1

            words_in_line = basic_statistics.line_to_words(line)
            if words_in_line != [""]:
                word_count += len(words_in_line)
            characters_in_line, characters_without_in_line = basic_statistics.count_characters(
                line)
            character_count_space += int(characters_in_line)
            character_count_nospace += int(characters_without_in_line)
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

            # for top_ten()
            for word in line.split():
                word_count += 1
                word = word.lower().strip(".,!?;:\"'()[]{}")
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1

    top_ten = sorted(counts.items(), key=lambda item: item[1],
                     reverse=True)[:10]

    # for word, count in word_analysis.top10(counts):
    #     print(f"{word:<10}{count}")
    data["number_of_lines"] = line_count
    data["number_of_words"] = word_count
    data["number_of_characters_with_spaces"] = character_count_space
    data["number_of_characters"] = character_count_nospace
    data["avg_word_per_line"] = basic_statistics.words_per_line(
        word_count, line_count)
    data["avg_character_per_word"] = basic_statistics.characters_per_word(
        character_count_nospace, word_count)
    data["number_of_sentences"] = sentence_count
    data["avg_word_per_sentences"] = sentence_analysis.words_per_sentence(
        word_count, sentence_count)
    data["longest_sentence"] = longest_sentence
    data["shortest_sentence"] = shortest_sentence
    data["sentence_len_distribution"] = dict(sorted(dict_sentence_len.items()))
    data["character_frequency"] = dict(sorted(dict_characters.items()))
    data["punctuation_frequency"] = dict(sorted(dict_punctuations.items()))
    data["number_of_lowercase"] = lower_case_count
    data["number_of_uppercase"] = upper_case_count

    with open("../basic_programming_project/backend/database/data.json",
              mode="w",
              encoding="utf-8") as export_data:
        json.dump(data, export_data)
