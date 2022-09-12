import re, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.metrics import roc_curve, auc, roc_auc_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


string = "(-2x+2)"


equation = "6(5x + 2) = 6 + 1+ (5)"
# equation = "-2(2x - 2) + 2 = -2 + 2"

def add_spaces(string):
    signs = ["+", "-", "*", "/", "(", ")"]
    trimmed = string.replace(" ", "")
    hashlist = list(trimmed)
    new_string = trimmed
    for i, value in enumerate(string):
        if value in signs:
            hashlist.insert(i-1, ' ')
            hashlist.insert(i+1, ' ')
    hashlist = ''.join(hashlist)
    print(hashlist)

add_spaces(string)


def lemmatizer(string):
    word_pos_tags = word_tokenize(string) # Get position tags
    print(word_pos_tags)

# lemmatizer(string)