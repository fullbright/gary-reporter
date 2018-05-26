#!/usr/bin/python
# -*- coding: UTF-8 -*-

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from nltk.corpus import gutenberg, state_union

#nltk.download()

sentences = """Au commencement, Dieu créa les cieux et la terre. 2 La terre était informe et vide : il y avait des ténèbres à la surface de l'abîme, et l'esprit de Dieu se mouvait au-dessus des eaux. 3 Dieu dit : Que la lumière soit ! Et la lumière fut. 4 Dieu vit que la lumière était bonne; et Dieu sépara la lumière d'avec les ténèbres. 5 Dieu appela la lumière jour, et il appela les ténèbres nuit. Ainsi, il y eut un soir, et il y eut un matin : ce fut le premier jour. 6 Dieu dit : Qu'il y ait une étendue entre les eaux, et qu'elle sépare les eaux d'avec les eaux. 7 Et Dieu fit l'étendue, et il sépara les eaux qui sont au-dessous de l'étendue d'avec les eaux qui sont au-dessus de l'étendue. Et cela fut ainsi. 8 Dieu appela l'étendue ciel. Ainsi, il y eut un soir, et il y eut un matin : ce fut le second jour.9 Dieu dit : Que les eaux qui sont au-dessous du ciel se rassemblent en un seul lieu, et que le sec paraisse. Et cela fut ainsi. 10 Dieu appela le sec terre, et il appela l'amas des eaux mers. Dieu vit que cela était bon. 11 Puis Dieu dit : Que la terre produise de la verdure, de l'herbe portant de la semence, des arbres fruitiers donnant du fruit selon leur espèce et ayant en eux leur semence sur la terre. Et cela fut ainsi. 12 La terre produisit de la verdure, de l'herbe portant de la semence selon son espèce, et des arbres donnant du fruit et ayant en eux leur semence selon leur espèce. Dieu vit que cela était bon. 13 Ainsi, il y eut un soir, et il y eut un matin : ce fut le troisième jour. 14 Dieu dit : Qu'il y ait des luminaires dans l'étendue du ciel, pour séparer le jour d'avec la nuit; que ce soient des signes pour marquer les époques, les jours et les années; 15 et qu'ils servent de luminaires dans l'étendue du ciel, pour éclairer la terre. Et cela fut ainsi. 16 Dieu fit les deux grands luminaires, le plus grand luminaire pour présider au jour, et le plus petit luminaire pour présider à la nuit; il fit aussi les étoiles. 17 Dieu les plaça dans l'étendue du ciel, pour éclairer la terre, 18 pour présider au jour et à la nuit, et pour séparer la lumière d'avec les ténèbres. Dieu vit que cela était bon. 19 Ainsi, il y eut un soir, et il y eut un matin : ce fut le quatrième jour."""

sentences2 = "Jesus est Seigneur. A part Dieu, il n'y a point d'autres Dieu."

sentences3 = """
	Au commencement, Dieu créa les cieux et la terre. La terre était informe et vide : il y avait des ténèbres à la surface de l'abîme, et l'esprit de Dieu se mouvait au-dessus des eaux. Dieu dit : Que la lumière soit ! Et la lumière fut.
		Dieu vit que la lumière était bonne; et 
"""

sentences4 = """
	Au commencement, Dieu crea les cieux et la terre. La terre etait informe et vide : il y avait des tenebres a la surface de l'abime, et l'esprit de Dieu se mouvait au-dessus des eaux. Dieu dit : Que la lumiere soit ! Et la lumiere fut.
		Dieu vit que la lumiere etait bonne; et 
"""

bible_kjv = gutenberg.raw("bible-kjv.txt")
train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

def extract_relations(text):
	# Tockenize words
	text_tokenized = word_tokenize(text)
	sent_tokenized = sent_tokenize(text)
	print("Sentence tokenized : ", sent_tokenized)
	print("Word tokenized : ", text_tokenized)

	text_filtered = remove_stopwords(text_tokenized)
	print("Text filtered : ", text_filtered)

	text_stemmed = stemmer(text_filtered)
	print("Text stemmed : ", text_stemmed)

	#Tag the parts of the sentence
	tag_speech(text)

def remove_stopwords(text_tokenized):
	filtered_words = []
	stop_words = set(stopwords.words("french"))
	for word in text_tokenized:
		if(word not in stop_words):
			filtered_words.append(word)

	return filtered_words

def stemmer(text_tockenized):
	stemmed_words = []
	ps = PorterStemmer()

	for word in text_tockenized:
		#print(ps.stem(word))
		stemmed_words.append(ps.stem(word))

	return stemmed_words

def tag_speech(text):
	custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
	tokenized_text = custom_sent_tokenizer.tokenize(sample_text)

	for word in tokenized_text:
		words = word_tokenize(word)
		tagged = nltk.pos_tag(words)

		chunckGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}"""
		chunkParser = nltk.RegexpParser(chunckGram)
		chunked = chunkParser.parse(tagged)


		print(chunked)

extract_relations(sentences4)