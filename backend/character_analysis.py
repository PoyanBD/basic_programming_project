def letter_frequency(words, dict_characters):
    this_dict = dict_characters
    line_stringfy = ""

    for word in words:
        line_stringfy += word.lower().strip(r".,-!?;:\"'“”’()[]{}")

    for character in line_stringfy:
        if character.isalpha() == True:
            if character in this_dict:
                this_dict[character] += 1
            else:
                this_dict[character] = 1

    return this_dict


def punctuation_statistics(words, dict_punctuations):
    this_dict = dict_punctuations
    line_stringfy = ""
    line_punctuatins = ""

    for word in words:
        line_stringfy += word.lower()

    for character in line_stringfy:
        if character.isalnum() == False:
            line_punctuatins += character

    for character in line_punctuatins:
        if character in this_dict:
            this_dict[character] += 1
        else:
            this_dict[character] = 1
    return this_dict


def case_distribution(words, lower_characters, upper_characters):
    line_stringfy = ""

    for word in words:
        line_stringfy += word.strip(r".,!?;:\"'()[]{}")

    for character in line_stringfy:
        if character.islower():
            lower_characters += 1
        elif character.isupper():
            upper_characters += 1

    return (lower_characters, upper_characters)
