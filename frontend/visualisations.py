import matplotlib.pyplot as plt
import json
import os


# def cache_path(filename):
#     name = os.path.splitext(filename)[0]
#     return os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "database"), f"{name}.json")

# with open("../basic_programming_project/backend/database/data.json", "r") as file: data = json.load(file)
# with open(cache_path("data"), "r", encoding="utf-8") as f: saved = json.load(f)


def character_frequency_visual():
	characters=[]
	character_freq=[]
	max_frequency=0

	for item in data["character_frequency"]:
		characters.append(item)
		item_value=data["character_frequency"][f"{item}"]
		character_freq.append(item_value)
		if max_frequency < item_value:
			max_frequency = item_value

	fig, ax = plt.subplots()
	bar_container = ax.bar(characters, character_freq)
	ax.set(ylabel='Frequency', title='Character frequency', ylim=(0, round(max_frequency+20)))
	ax.bar_label(bar_container, fmt='{:,.0f}')

	plt.show()



