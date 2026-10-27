import matplotlib.pyplot as plt
import json

with open("../basic_programming_project/backend/database/data.json", "r") as file: data = json.load(file)


def character_frequency_visual():
	characters=[]
	character_freq=[]
	max_frequency=0

	for item in data["character_frequency"]:
		characters.append(item)
		character_freq.append(data["character_frequency"][f"{item}"])
		if max_frequency < data["character_frequency"][f"{item}"]:
			max_frequency= data["character_frequency"][f"{item}"]

	fig, ax = plt.subplots()
	bar_container = ax.bar(characters, character_freq)
	ax.set(ylabel='Frequency', title='Character frequency', ylim=(0, round(max_frequency+20)))
	ax.bar_label(bar_container, fmt='{:,.0f}')

	plt.show()