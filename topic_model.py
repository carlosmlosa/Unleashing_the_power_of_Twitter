import pandas as pd
import numpy as np
from bertopic import BERTopic
import matplotlib.pyplot as plt
import re
import string
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.utils import simple_preprocess




#### PARAMS
min_topic_size = 150
model_path = 'models/topic_model3'
results_path = 'topic_results/tweet_dataset_with_topics3.csv'


nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

df = pd.read_csv('tweet_dataset.csv')
embeddings = pd.read_csv('embeddings.csv').to_numpy()




misspell_dict = {"aren't": "are not", "can't": "cannot", "couldn't": "could not",
                 "didn't": "did not", "doesn't": "does not", "don't": "do not",
                 "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
                 "he'd": "he would", "he'll": "he will", "he's": "he is",
                 "i'd": "I had", "i'll": "I will", "i'm": "I am", "isn't": "is not",
                 "it's": "it is", "it'll": "it will", "i've": "I have", "let's": "let us",
                 "mightn't": "might not", "mustn't": "must not", "shan't": "shall not",
                 "she'd": "she would", "she'll": "she will", "she's": "she is",
                 "shouldn't": "should not", "that's": "that is", "there's": "there is",
                 "they'd": "they would", "they'll": "they will", "they're": "they are",
                 "they've": "they have", "we'd": "we would", "we're": "we are",
                 "weren't": "were not", "we've": "we have", "what'll": "what will",
                 "what're": "what are", "what's": "what is", "what've": "what have",
                 "where's": "where is", "who'd": "who would", "who'll": "who will",
                 "who're": "who are", "who's": "who is", "who've": "who have",
                 "won't": "will not", "wouldn't": "would not", "you'd": "you would",
                 "you'll": "you will", "you're": "you are", "you've": "you have",
                 "'re": " are", "wasn't": "was not", "we'll": " will", "tryin'": "trying"}


def _get_misspell(misspell_dict):
    misspell_re = re.compile('(%s)' % '|'.join(misspell_dict.keys()))
    return misspell_dict, misspell_re


def replace_typical_misspell(text):
    misspellings, misspellings_re = _get_misspell(misspell_dict)
    def replace(match):
        return misspellings[match.group(0)]
    return misspellings_re.sub(replace, text)
    

puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']',
          '>', '%', '=', '#', '*', '+', '\\', '•', '~', '@', '£', '·', '_', '{', '}', '©', '^',
          '®', '`', '<', '→', '°', '€', '™', '›', '♥', '←', '×', '§', '″', '′', 'Â', '█',
          '½', 'à', '…', '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶',
          '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', '▒', '：', '¼',
          '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲',
          'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', '∙', '）', '↓', '、', '│', '（', '»', '，', '♪',
          '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹', '≤', '‡', '√']


def clean_text(x):
    x = str(x)
    for punct in puncts + list(string.punctuation):
        if punct in x:
            x = x.replace(punct, f' {punct} ')
    return x


def clean_numbers(x):
    return re.sub(r'\d+', ' ', x)



# Remove URLs and mentions
df['text'] = df['text'].str.replace('http\S+|www.\S+|@\S+', '', case=False)
# Remove punctuation and make lowercase
df['text'] = df['text'].str.lower().str.replace('[^\w\s]','')
# clean misspellings
df['text'] = df['text'].apply(replace_typical_misspell)
# clean the text
df['text'] = df['text'].apply(clean_text)
# clean numbers
df['text'] = df['text'].apply(clean_numbers)
# strip
df['text'] = df['text'].str.strip()
# Tokenize text
df['tokens'] = df['text'].apply(word_tokenize)
# Remove stop words
stop_words = set(stopwords.words('english'))
df['tokens'] = df['tokens'].apply(lambda x: [word for word in x if word not in stop_words])
# Lemmatize words
lemmatizer = WordNetLemmatizer()
df['tokens'] = df['tokens'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
# Apply simple_preprocess to each token
df['tokens'] = df['tokens'].apply(lambda x: [simple_preprocess(word) for word in x])
# Flatten list of lists into single list of words
df['tokens'] = df['tokens'].apply(lambda x: [item for sublist in x for item in sublist])
# Remove any tokens with only one character
df['tokens'] = df['tokens'].apply(lambda x: [word for word in x if len(word) > 1])
# Drop empty tweets
df['text'].replace('', np.nan, inplace=True)

df.dropna(inplace=True)
df = df.reset_index()
print(df.head())

df['preprocessed_text'] = df.tokens.apply(lambda x: ' '.join(x))

print(df.head())

embedding_model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
embeddings = embedding_model.encode(df.preprocessed_text, show_progress_bar=True, batch_size=256)


model = BERTopic(verbose=True, calculate_probabilities=False, min_topic_size=min_topic_size, language = "english", n_gram_range=(1,3))
topics, _ = model.fit_transform(df['text'], embeddings)

print('done')
df['topic'] = topics
model.save(model_path)
df.to_csv(results_path, index=True)
