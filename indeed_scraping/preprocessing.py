import pandas as pd
import re
import nltk
import string
stopwords = nltk.corpus.stopwords.words("english")
df = pd.read_csv('indeed_scraping/job_postings.csv')

def cleanhtml(description):
    """removes anything inbetween <>"""
    description = str(description)
    cleanr = re.compile('<.*?>')
    description = re.sub(cleanr, '', description)
    return description

descriptions_list = list(df['description'])
descriptions_list = [cleanhtml(description) for description in descriptions_list]


def tokenize(description):
    """Removes brackets, braces, excess whitespace, sets to lowercase. Returns a list of tokens."""
    description = "".join(description.lower()).strip().split()
    description = [word.translate(str.maketrans('','', string.punctuation)) for word in description]
    return description

descriptions_list = [tokenize(description) for description in descriptions_list]


def remove_stopwords(description):
    """remove stopwords and 'amp' """
    description = [word for word in description if word != 'amp']
    description = [word for word in description if word not in stopwords]
    return description

descriptions_list = [remove_stopwords(description) for description in descriptions_list]

"""replace the old descriptions with the clean description"""
df['description'] = descriptions_list
path = 'C:\\Users\\green\Documents\\projects\\job_search\\indeed_scraping\\'
df.to_csv(path + "job_postings_cleaned.csv")
