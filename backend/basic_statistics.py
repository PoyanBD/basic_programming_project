def line_to_words(line):
    line = line.strip()
    words = line.split(" ")
    return words


def count_characters(line):
    characters_with_spaces = len(line)
    characters_without_spaces = len(line.replace(" ", ""))
    return (characters_with_spaces, characters_without_spaces)
