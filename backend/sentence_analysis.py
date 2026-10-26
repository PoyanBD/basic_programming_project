def sentence_counter(line):
    sentences_in_line = 0
    for character in line:
        if character == "!" or character == "." or character == "?":
            sentences_in_line += 1
    return int(sentences_in_line)


def words_per_sentence(words, sentences):
    return round(int(words) / int(sentences), 2)


def sentences_in_line(line, sentence):
    full_sentences = []
    for character in line:
        if character != "!" and character != "." and character != "?":
            sentence += character
        else:
            sentence += character
            full_sentences.append(sentence)
            sentence = ""
    return (full_sentences, sentence)


def long_sentence(longest_sentence, sentences):
    for sentence in sentences:
        this_sentence = sentence.replace("\n", " ").strip()
        if len(longest_sentence) < len(this_sentence):
            longest_sentence = this_sentence

    return (longest_sentence)


def short_sentence(shortest_sentence, sentences):
    for sentence in sentences:
        this_sentence = sentence.replace("\n", " ").strip()
        if shortest_sentence == "":
            shortest_sentence = this_sentence
        if len(shortest_sentence) > len(this_sentence):
            shortest_sentence = this_sentence

    return (shortest_sentence)


def sentence_len_distribution(sentences, dict_sentence_len):
    this_dict = dict_sentence_len

    for sentence in sentences:
        sentence_len = str(len(sentence.split()))
        if sentence_len in this_dict:
            this_dict[sentence_len] += 1
        else:
            this_dict[sentence_len] = 1
            
    top = sorted(this_dict.items(), key=lambda item: (-item[1], item[0]))[:5]
    this_dict = dict(top)
    
    return this_dict
