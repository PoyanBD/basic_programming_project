def top10(counts):
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10]

def unique_words(words):
    return len(set(words))

def words_appearing_only_once(counts):
    return sorted(w for w, c in counts.items() if c == 1)