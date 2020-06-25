import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix

import pickle
import datetime

filename = '/Users/katielazell-fairman/Downloads/Training Data - master (1).csv'

def load_data(filename):
    #Import tagged dataset

    df= pd.read_csv(filename)
    print ("Training data", df.shape)
    print("Columns", df.columns)
    print (df.sample(8))

    return df

def save_model(model, version, path, notes=None):

        # Save to model
        model_artifact = {'model': model,
                'version': version,
                'date': datetime.datetime.now(),
                'notes': notes}
        

        pkl_filename = "MultinomialNBClassifier_{}.pkl".format(version)
        try:
            with open(path+pkl_filename, 'wb') as file:
                pickle.dump(model_artifact, file)
            print ("Saved model {} to {}".format(version, path+pkl_filename))
        except:
            print ("Could not save model")


class MultinomialNBClassifier:
    def __init__(self):
        self.model = None
        self.vocab = None
        self.classes = None
        self.vectorizer = None
        pass
    
    def train(self, X, y):

        # Test Train Validate Split
        X_train, X_test, y_train, y_test = train_test_split(X, y
                                                    , test_size=0.15
                                                    , random_state=88)

        # Create vocabulary and vectorize with Term Frequency and Inverse Document Frequency
        vectorizer = TfidfVectorizer(max_features=10000,
                                   ngram_range=(1,2),
                                   use_idf=True,
                                   norm='l2')

        X_train_t = vectorizer.fit_transform(X_train)
        X_test_t = vectorizer.transform(X_test)
        print (vectorizer.vocabulary_)

        # Initiate and fit Model
        model = MultinomialNB()
        model.fit(X_train_t, y_train)

        # Save Model & Data
        self.vectorizer = vectorizer
        self.vocab = vectorizer.vocabulary_
        self.model = model
        self.classes = model.classes_

        # Confirm training
        print ("Trained on {n_records} records {n_features} features".format(n_records=X_train_t.shape[0], 
                                                                                n_features=X_train_t.shape[1]))
        # Model Performance
        print ("Test data accuracy: {accuracy}".format(accuracy=model.score(X_test_t, y_test)))

        

    def predict(self, X, verbose=False):
        # Vectorize
        X_t = self.vectorizer.transform(X)
        # Predict 
        y_pred = self.model.predict(X_t)
        if verbose:
            y_proba = self.model.predict_proba(X_t)
            # Create dict with input and output tuples (with probabilities)
            results = dict()
            for text, cat, p in zip(X, y_pred, y_proba):
                 results[text] = (cat, list(p))
            return results

        return dict(zip(X,y_pred))












