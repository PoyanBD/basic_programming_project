def top10(counts):
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10]

def unique_words(words):
    return len(set(words))

def words_appearing_only_once(word, words):
    word_counts = {}
    for w in words:
        word_counts[w] = word_counts.get(w, 0) + 1
    return word_counts.get(word, 0) == 1