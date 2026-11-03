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
	bar_container = ax.bar(characters, character_freq)
	ax.set(ylabel='Frequency', title='Character frequency', ylim=(0, round(max_frequency+20)))
	ax.bar_label(bar_container, fmt='{:,.0f}')

	plt.show()



