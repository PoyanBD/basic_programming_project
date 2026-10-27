def count_words(words_in_line, dict_words):
    PUNCTUATION = ".,!?;:\"'()[]{}»«–—…"
    for word in words_in_line:
        word = word.lower().strip(PUNCTUATION)
        if word and any(ch.isalnum() for ch in word):
            dict_words[word] = dict_words.get(word, 0) + 1
    return dict_words


def most_common_words(dict_words):
    total = sum(dict_words.values())
    top = sorted(dict_words.items(), key=lambda item: (-item[1], item[0]))
    return [(word, count, count / total * 100) for word, count in top]


def shortest_word(dict_words):
    if not dict_words:
        return None
    return min(dict_words, key=lambda word: (len(word), word))


def longest_word(dict_words):
    if not dict_words:
        return None
    return max(dict_words, key=lambda word: (len(word), -ord(word[0])))

def word_length_distribution(dict_words):
    lengths = {}
    for word, count in dict_words.items():
        lengths[len(word)] = lengths.get(len(word), 0) + count
    return dict(sorted(lengths.items()))

def unique_words(dict_words):
    return len(dict_words)


def words_appearing_only_once(dict_words):
    return sorted(word for word, count in dict_words.items() if count == 1)