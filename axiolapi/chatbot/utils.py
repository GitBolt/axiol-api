import nltk
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import numpy as np

nltk.download("punkt")

lemmatizer = WordNetLemmatizer()

def tokenize_and_lemmatize(sentence):
    result = [lemmatizer.lemmatize(x.lower()) for x in word_tokenize(sentence)]
    return result

def bag_of_words(sentence, words):
    bag = np.zeros(len(words), dtype=np.float32)
    for index, w in enumerate(words):
        if w in sentence: 
            bag[index] = 1
    return bag

def solve(sentence):
    q = ""
    for i in sentence:
        if not i.isalpha() and i not in [".", ",", "?", "!", "'", "}", "{", "|"]:
            if "^" in list(i):
                q += i.replace("^", "**")
            else:
                q+= i
    quotes = q.replace('\"', '\\"')
    try:
        return eval(quotes)
    except:
        return "Sorry but I was not able to understand the question, either I'm too dumb or question was wrong :p can you rephrase?"
