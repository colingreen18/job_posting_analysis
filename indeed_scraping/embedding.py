import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report

df = pd.read_csv('indeed_scraping/job_postings_cleaned.csv')

corpus = df['description']
df['apply'], unique = pd.factorize(df['apply'])
print(unique)
tfidfv = TfidfVectorizer(min_df=0, max_df=1, use_idf=True)
tfidfv_matrix = tfidfv.fit_transform(corpus)
tfidfv_matrix = tfidfv_matrix.toarray()

vocab = tfidfv.get_feature_names()
tfidf_df = pd.DataFrame(np.round(tfidfv_matrix, 2), columns=vocab)

tfidf_df['apply'] = df['apply']

X = tfidf_df.drop('apply', axis='columns')
y = tfidf_df['apply'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

lgr = LogisticRegression(max_iter=1000)
param_grid = [{}]

log_reg_tf = GridSearchCV(lgr, param_grid, cv=KFold(n_splits=2).split(X_train, y_train), verbose=2)
y_preds_log_reg_tf = log_reg_tf.fit(X_train, y_train).predict(X_test)

plot_confusion_matrix(log_reg_tf, X_test, y_test, cmap=plt.cm.Blues, display_labels = ['no', 'yes'], values_format = '')

report_log_reg_tf = classification_report( y_test, y_preds_log_reg_tf)
print(report_log_reg_tf)