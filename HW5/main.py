# Nate McDorman - CS 4650 - HW #5

import en_core_web_lg
import pandas as pd
import string

from spacy.compat import pickle
from wordcloud import WordCloud
from collections import Counter
from matplotlib import pyplot as plt
from newsapi import NewsApiClient
from datetime import date, timedelta

nlp_eng = en_core_web_lg.load()
newsapi = NewsApiClient(api_key='95355eca0d5e4ca8b290337fb75c5aa4')
endDate = date.today().strftime("%Y-%m-%d")
startDate = (date.today() - timedelta(days=28)).strftime("%Y-%m-%d")
temp = newsapi.get_everything(q='coronavirus', language='en', from_param=startDate, to=endDate, sort_by='relevancy', page_size=100)

# store data
filename = 'articlesVOCIVD.pckl'
pickle.dump(temp['articles'], open(filename, 'wb'))

# ignore some fields we're not going to use
data = []
for index, article in enumerate(temp['articles']):
    title = article['title']
    date = article['publishedAt']
    description = article['description']
    content = article['content']
    data.append({'title': title, 'date': date, 'description': description, 'content': content})

# convert data to dataframe
df = pd.DataFrame(data)
df = df.dropna()
df.head()

#define get_keywords_eng function
def get_keywords_eng(token):
    #token is the entire article's content, split it up
    words = token.split(' ')
    result = []
    for word in words:
        cleanedWord = str()
        if word in nlp_eng.Defaults.stop_words or word.lower() in nlp_eng.Defaults.stop_words:
            continue
        for char in word:
            if char in string.punctuation:
                continue
            else:
                cleanedWord = cleanedWord + str(char)
        result.append(cleanedWord)
    return result

# now retrieve keywords for each article's contents, and append most common 5
results = []
for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])

# add new column to dataframe
df['keywords'] = results
text = str(results)
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()