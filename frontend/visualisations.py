import matplotlib.pyplot as plt

def character_frequency_visual(letter_freq):
	characters=[]
	character_freq=[]
	max_frequency=0

	for item in letter_freq:
		characters.append(item)
		item_value=letter_freq[item]
		character_freq.append(item_value)
		if max_frequency < item_value:
			max_frequency = item_value

	fig, ax = plt.subplots()
	ax.bar(characters, character_freq)
	ax.set(ylabel='Frequency', title='Character frequency')

	# plt.show()

def character_most_common(common_characters):

	characters=[]
	character_counts=[]

	for word in common_characters:
		characters.append(word[0])
		character_counts.append(word[1])

	fig, ax = plt.subplots()
	bar_container = ax.bar(characters, character_counts)
	ax.set(ylabel='Frequency', title='Most common characters')
	ax.bar_label(bar_container, fmt='{:,.0f}')

	plt.show()


def text_composition(lines,sentences,unique_words,paragraphs):

	fig, ax = plt.subplots()

	text = ['Lines', 'Sentences', 'Unique words', 'Paragraphs']
	counts = [lines, sentences, unique_words, paragraphs]
	bar_colors = ['tab:cyan', 'tab:pink', 'tab:red', 'tab:orange']

	ax.bar(text, counts, color=bar_colors)

	ax.set_ylabel('Count')
	ax.set_title('Text composition')

	# plt.show()

def character_type_distribution(characters_w_spaces,characters):
	spaces= characters_w_spaces-characters

	labels = 'Characters', 'Spaces'
	sizes = [characters, spaces]

	fig, ax = plt.subplots()
	ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['pink', 'lightblue'])

	plt.show()

def common_word_frequency(word_list):

	words=[]
	word_counts=[]

	for word in word_list:
		words.append(word[0])
		word_counts.append(word[1])

	fig, ax = plt.subplots()
	bar_container = ax.bar(words, word_counts)
	ax.set(ylabel='Frequency', title='Top 10 most common words')
	ax.bar_label(bar_container, fmt='{:,.0f}')

	# plt.show()

def word_length_distribution(word_len_list):

	word_len=[]
	word_len_counts=[]

	for item in word_len_list:
		word_len.append(item)
		word_len_counts.append(word_len_list[item])

	fig, ax = plt.subplots()
	ax.bar(word_len, word_len_counts)
	ax.set(ylabel='Frequency', title='Word length distribution')

	plt.show()

def sentence_length_distribution(sentence_dict):

	sentence_len_dict={}

	for key, value in sentence_dict.items():
		sentence_len_dict[int(key)] = value
		soreted_dict =dict(sorted(sentence_len_dict.items()))
	
	sentence_len=[]
	sentence_len_counts=[]

	for item in soreted_dict:
		sentence_len.append(item)
		sentence_len_counts.append(soreted_dict[item])

	fig, ax = plt.subplots()
	ax.bar(sentence_len, sentence_len_counts)
	ax.set(ylabel='Frequency', title='Sentence length distribution')

	# plt.show()

def sentence_length_frequency(common_sentence_len):

	sentences_len=[]
	sentences_len_counts=[]

	for word in common_sentence_len:
		sentences_len.append(word[0])
		sentences_len_counts.append(word[1])

	fig, ax = plt.subplots()
	bar_container = ax.bar(sentences_len, sentences_len_counts)
	ax.set(ylabel='Frequency', title='Most common sentence lengths')
	ax.bar_label(bar_container, fmt='{:,.0f}')

	plt.show()