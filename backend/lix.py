def long_words_count(Word_len_list):
	long_words=0
	for item in Word_len_list:
		if int(item)>6:
			long_words+= Word_len_list[item]

	return long_words

def lix_stat(words,sentences,long_words):

	lix=round((words/sentences)+((long_words/words)*100),2)

	if lix < 24:
		return "Very Easy, Suitable for children's books or simple texts."
	elif lix <34:
		return "Easy, Suitable for a general audience with basic reading skills."
	elif lix <44 :
		return "Medium, Typical readability for novels or newspapers."
	elif lix<54 :
		return "Difficult, Suitable for academic texts or technical documents."
	elif 55<=lix:
		return "Very Difficult, Suitable for specialized literature or scientific papers."
	else:
		return "Something went wrong" 