from copy import copy

import numpy as np
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from genrec.logger import get_logger
from genrec.utils import np_printoptions

class MusicGenreClassifier:
    def __init__(self, genres, data, type='knn', clf_kwargs=None):
        self.logger = get_logger('classifier')

        self.genres = genres
        self.m_genres = { genre:i for i, genre in enumerate(genres) }
        self.randstate = np.random.RandomState()

        self.scaler = None
        if not clf_kwargs:
            clf_kwargs = { }

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
            self.scaler = StandardScaler()
        else:
            raise LookupError('Classifier type "{}" is invalid'.format(type))

        self._convert_data(data)

        self.logger.info('Classifier: {} (params={})'.format(
            self.proto_clf.__class__.__name__,
            clf_kwargs
        ))

    def kfold_test(self, k=10, iters=100):
        n_genres = len(self.genres)

        train_acc = np.zeros(iters * k)
        test_acc = np.zeros(iters * k)
        cms = np.zeros((iters, n_genres, n_genres))
        clf = copy(self.proto_clf)

        self.logger.info('{}-Fold test ({} iterations)'.format(k, iters))
        for iter in range(iters):
            kf = KFold(n_splits=k, random_state=self.randstate, shuffle=True)
            cm = np.zeros((n_genres, n_genres)) # confusion matrix

            for i, (train_idx, test_idx) in enumerate(kf.split(self.X, self.y)):
                idx = iter * k + i
                X_train, X_test = self.X[train_idx], self.X[test_idx]
                y_train, y_test = self.y[train_idx], self.y[test_idx]

                if self.scaler:
                    # normalize data before training
                    self.scaler.fit(X_train)
                    X_train, X_test = self.scaler.transform(X_train), \
                                        self.scaler.transform(X_test)

                clf.fit(X_train, y=y_train)   # train

                # accuracy
                train_acc[idx] = clf.score(X_train, y=y_train)
                test_acc[idx] = clf.score(X_test, y=y_test)


                # confusion matrix
                y_pred = clf.predict(X_test)
                cm += confusion_matrix(y_test, y_pred)

            cms[iter,:,:] = cm

        # Calculate avg confusion matrix
        mean_cm = np.mean(cms, axis=0)

        # Print metrics
        with np_printoptions(precision=3, suppress=True):
            self.logger.info('Train accuracy: {:5.2f}% +- ({:5.2f}%)'.format(
                np.mean(train_acc) * 100.0, np.std(train_acc) * 100.0
            ))
            self.logger.info('Test accuracy: {:5.2f}% +- ({:5.2f}%)'.format(
                np.mean(test_acc) * 100.0, np.std(test_acc) * 100.0
            ))
            self.logger.info('Genres: {}'.format(self.genres))
            self.logger.info('Confusion matrix: \n{}'.format(mean_cm))


    def load(self, filepath):
        self.proto_clf = joblib.load(filepath)

    def save(self, filepath):
        joblib.sump(self.proto_clf, filepath)

    def _convert_data(self, data):
        """ Converts data from dataset to sklearn format """
        X, y = [ ], [ ]
        for genre, aufiles in data.items():
            for aufile in aufiles:
                X.append( aufile.fv )
                y.append( self.m_genres[genre] )

        self.X = np.array(X)
        self.y = np.array(y)

