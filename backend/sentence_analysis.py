"""
"https://www.merriam-webster.com/dictionary/sentence": a word, clause, or phrase or a group of clauses or phrases forming a 
syntactic unit which expresses an assertion, a question, a command, a wish, an exclamation, or the performance of an action, 
that in writing usually begins with a capital letter and concludes with appropriate end punctuation, 
and that in speaking is distinguished by characteristic patterns of stress, pitch, and pauses
honorifics: I, Mr, Mrs, Miss, Ms, Mx, Sir, Dame, Dr, Cllr, Lady, or Lord.
"""

def sentence_counter(line):
    sentences_in_line = 0
    for character in line:
        if character == "!" or character == "." or character == "?":
            sentences_in_line += 1
    return int(sentences_in_line)


def words_per_sentence(words, sentences):
    return round(int(words) / int(sentences), 2)


def sentences_in_line(line, sentence):
    sentence_exceptions = [
        "Mr.", "Mrs.", "Miss.", "Ms.", "Mx.", "Sir.", "Dame.", "Dr.", "Cllr.",
        "Lady.", "Lord.", "I."
    ]
    full_sentences = []
    last_five_characters = ""
    line_index = 0
    for character in line:
        last_five_characters += character
        if len(last_five_characters) >= 5:
            last_five_characters = last_five_characters[1:5]

        if character != "!" and character != "." and character != "?":
            sentence += character
        else:
            end_sentence = -1
            for exception in sentence_exceptions:
                if end_sentence == -1:
                    end_sentence = last_five_characters.find(exception)
            if character == "." and line[line_index + 1] == ".":
                end_sentence = 1
            if end_sentence == -1:
                sentence += character
                full_sentences.append(sentence)
                sentence = ""
            else:
                sentence += character
        line_index += 1
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
    
    return this_dict
