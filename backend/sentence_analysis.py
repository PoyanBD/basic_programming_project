def sentence_counter(line):
    sentences_in_line = 0
    for character in line:
        if character == "!" or character == "." or character == "?":
            sentences_in_line += 1
    return int(sentences_in_line)


def words_per_sentence(words, sentences):
    return round(int(words) / int(sentences), 2)


def long_sentence(line, sentence, longest_sentence):
    for character in line:
        if character != "!" and character != "." and character != "?":
            sentence += character
        else:
            sentence += character
            if len(sentence) > len(longest_sentence):
                longest_sentence = sentence
            sentence = ""
    return (longest_sentence, sentence)
