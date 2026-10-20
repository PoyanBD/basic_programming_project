import basic_statistics
import file_loading
import word_analysis
import sentence_analysis


def process_book(path):
    character_count_space = 0
    character_count_nospace = 0
    line_count = 0
    word_count = 0
    sentence_count = 0
    longest_sentence = ""
    curent_sentence = ""
    counts = {}

    with open(path, "r", encoding="utf-8") as book:
        for line in book:
            line_count += 1
            if basic_statistics.line_to_words(line) != [""]:
                word_count += len(basic_statistics.line_to_words(line))
            characters_in_line, characters_without_in_line = basic_statistics.count_characters(
                line)
            character_count_space += int(characters_in_line)
            character_count_nospace += int(characters_without_in_line)
            sentence_count += sentence_analysis.sentence_counter(line)
            longest_sentence, curent_sentence = sentence_analysis.long_sentence(
                line, curent_sentence, longest_sentence)

            # for top_ten()
            for word in line.split():
                word_count +=1 
                word = word.lower().strip(".,!?;:\"'()[]{}")
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1

    top_ten = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10]

    for word, count in word_analysis.top10(counts):
        print(f"{word:<10}{count}")
    
    print(line_count, word_count, character_count_space,
          character_count_nospace)
    print("avg-w-l", basic_statistics.words_per_line(word_count, line_count))
    print(
        "avg-c-w",
        basic_statistics.characters_per_word(character_count_nospace,
                                             word_count))
    print("sentence count:", sentence_count)
    print("avg-w-s",
          sentence_analysis.words_per_sentence(word_count, sentence_count))
    print("Longest sentence:", longest_sentence)

if __name__ == "__main__":
    process_book("../basic_programming_project/library/GostaberlingsSaga.txt")
