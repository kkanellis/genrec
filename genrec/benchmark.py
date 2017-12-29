from copy import copy
from time import perf_counter

import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
from sklearn.linear_model import Perceptron
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from genrec.logger import get_logger
from genrec.utils import np_printoptions, plot_confusion_matrix

class ClassifierBenchmark:
    supported_classifiers = {
        'knn': KNeighborsClassifier,
        'svm': SVC,
        'dtree': DecisionTreeClassifier,
        'gnb': GaussianNB,
        'perc': Perceptron,
        'mlp': MLPClassifier,
        'ada': AdaBoostClassifier,
    }

    def __init__(self, type, genres, data, name=None, clf_kwargs=None):
        self.logger = get_logger('benchmark')

        if not name:
            name = 'Unamed classifier'
        self.display_name = name

        if type not in self.supported_classifiers:
            raise LookupError("Type '{}' classifier not supported".format(type))

        if not clf_kwargs:
            clf_kwargs = { }

        self.randstate = np.random.RandomState()
        if type in ['svm', 'mlp']:
            clf_kwargs['random_state'] = self.randstate

        # Initialize classifier
        self.proto_clf = self.supported_classifiers[type](**clf_kwargs)

        self.genres = genres
        self.m_genres = { genre:i for i, genre in enumerate(genres) }
        self.scaler = StandardScaler()

        self._convert_data(data)

        self.logger.info('Classifier: {} (params={})'.format(
            self.proto_clf.__class__.__name__,
            clf_kwargs
        ))

    def kfold_test(self, k=10, iters=100, plot_cm=False):
        n_genres = len(self.genres)

        train_acc = np.zeros(iters * k)
        test_acc = np.zeros(iters * k)
        cms = np.zeros((iters, n_genres, n_genres))
        clf = self.proto_clf

        self.logger.info('{}-Fold test ({} iterations)'.format(k, iters))
        start = perf_counter()
        for iter in range(iters):
            kf = KFold(n_splits=k, random_state=self.randstate, shuffle=True)
            cm = np.zeros((n_genres, n_genres)) # confusion matrix

            for i, (train_idx, test_idx) in enumerate(kf.split(self.X, self.y)):
                idx = iter * k + i
                X_train, X_test = self.X[train_idx], self.X[test_idx]
                y_train, y_test = self.y[train_idx], self.y[test_idx]

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

        elapsed = perf_counter() - start
        self.logger.info('Elapsed {:5.3f} secs ({:5.3f} secs per iter)'.format(elapsed, elapsed / (iters * k)))

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

        # Plot confusion matrix
        if plot_cm:
            plot_confusion_matrix(
                cm, self.display_name,
                self.proto_clf.__class__.__name__
            )


    def load(self, filepath):
        self.proto_clf = joblib.load(filepath)

    def save(self, filepath):
        joblib.dump(self.proto_clf, filepath)

    def _convert_data(self, data):
        """ Converts data from dataset to sklearn format """
        X, y = [ ], [ ]
        for genre, aufiles in data.items():
            for aufile in aufiles:
                X.append( aufile.fv )
                y.append( self.m_genres[genre] )

        self.X = np.array(X)
        self.y = np.array(y)

