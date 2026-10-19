import basic_statistics
import file_loading
import word_analysis


def process_book(path):
    character_count_space = 0
    character_count_nospace = 0
    line_count = 0
    word_count = 0

    with open(path, "r") as book:
        for line in book:
            line_count += 1
            if basic_statistics.line_to_words(line) != [""]:
                word_count += len(basic_statistics.line_to_words(line))
            characters_in_line, characters_without_in_line = basic_statistics.count_characters(
                line)
            character_count_space += int(characters_in_line)
            character_count_nospace += int(characters_without_in_line)

    print(line_count, word_count, character_count_space,
          character_count_nospace)
    print("avg-w-l", word_analysis.words_per_line(word_count, line_count))
    print(
        "avg-c-w",
        word_analysis.characters_per_word(character_count_nospace, word_count))


process_book("../basic_programming_project/library/test.txt")
