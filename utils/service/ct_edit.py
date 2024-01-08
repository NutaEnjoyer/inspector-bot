from typing import List, Type
from pandas import Series


def remove_non_exist(
	words: List[str],
	main_list: List[str]
) -> List[str]:
	non_exist = list()

	for word in words:

		try:
			main_list.remove(word)
		except ValueError:
			non_exist.append(word)

	return non_exist


def remove_exist(
	words: List[str],
	main_list: List[str]
) -> List[str]:
	exist = list()

	for word in words:

		if word not in main_list:
			continue

		exist.append(word)

	return exist


def remove_items(main: List[str], items: List[str]) -> None:
	for item in items:
		main.remove(item)


def series_words_list(series: List[Series]) -> List[str]:
	result = list()

	for _ in series:
		result += _

	return result