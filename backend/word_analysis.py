PUNCTUATION = ".,!?;:\"'()[]{}»«–—…"


def count_words(words_in_line, counts):
    for word in words_in_line:
        word = word.lower().strip(PUNCTUATION)
        if word and any(ch.isalnum() for ch in word):
            counts[word] = counts.get(word, 0) + 1
    return counts


def top10(counts):
    total = sum(counts.values())
    top = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]
    return [(word, count, count / total * 100) for word, count in top]


def shortest_word(counts):
    if not counts:
        return None
    return min(counts, key=lambda w: (len(w), w))


def longest_word(counts):
    if not counts:
        return None
    return max(counts, key=lambda w: (len(w), -ord(w[0])))


def unique_words(counts):
    return len(counts)


def words_appearing_only_once(counts):
    return sorted(w for w, c in counts.items() if c == 1)