from copy import copy

import numpy as np

from sklearn.externals import joblib
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier


from genrec.logger import get_logger

class MusicGenreClassifier:
    def __init__(self, genres, data, type='knn', clf_kwargs=None):
        self.genres = genres
        self.m_genres = { genre:i for i, genre in enumerate(genres) }

        self.logger = get_logger('classifier')

        if not clf_kwargs:
            clf_kwargs = { }

        self.req_scaling = False
        if type == 'knn':
            self.proto_clf = KNeighborsClassifier(**clf_kwargs)
        elif type == 'svm':
            self.proto_clf = LinearSVC(**clf_kwargs)
        elif type == 'dtree':
            self.proto_clf = DecisionTreeClassifier(**clf_kwargs)
        elif type == 'gnb':
            self.proto_clf = GaussianNB(**clf_kwargs)
        elif type == 'mlp':
            self.proto_clf = MLPClassifier(**clf_kwargs)
            self.req_scaling = True
        else:
            raise LookupError('Classifier type "{}" is invalid'.format(type))

        self._convert_data(data)
        self.randstate = np.random.RandomState()

    def kfold_test(self, k=10, times=1000):
        accuracy = np.zeros(times)

        i = 0
        for _ in range(times // k):
            kf = KFold(n_splits=k, random_state=self.randstate, shuffle=True)

            for train_idx, test_idx in kf.split(self.X, self.y):
                X_train, X_test = self.X[train_idx], self.X[test_idx]
                y_train, y_test = self.y[train_idx], self.y[test_idx]

                if self.req_scaling:
                    X_train, X_test = self._scale_data(X_train, X_test)

                clf = copy(self.proto_clf)
                clf.fit(X_train, y_train)

                accuracy[i] = clf.score(X_test, y_test)
                i += 1

        self.logger.info('Mean accuracy: {:5.2f}% +- ({:5.2f}%)'.format(
            np.mean(accuracy) * 100.0, np.std(accuracy) * 100.0
        ))

    def load(self, filepath):
        self.proto_clf = joblib.load(filepath)

    def save(self, filepath):
        joblib.sump(self.proto_clf, filepath)

    def _convert_data(self, data):

        X, y = [ ], [ ]
        for genre, aufiles in data.items():
            for aufile in aufiles:
                X.append( aufile.fv )
                y.append( self.m_genres[genre] )

        self.X = np.array(X)
        self.y = np.array(y)

    def _scale_data(self, X_train, X_test):
        scaler = StandardScaler()
        scaler.fit(X_train)
        return scaler.transform(X_train), scaler.transform(X_test)

