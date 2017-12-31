from copy import copy
from time import perf_counter

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

from genrec.logger import get_logger
from genrec.utils import np_printoptions, plot_confusion_matrix

class ClassifierBenchmark:
    """ Benchmark a classifier with specific data """

    def __init__(self, clf, genres, data, display_name):
        self.logger = get_logger('benchmark')

        self.display_name = display_name
        self.clf = clf
        self.genres = genres
        self.m_genres = { genre:i for i, genre in enumerate(genres) }
        self.scaler = StandardScaler()

        self.X, self.y = data

    def kfold_test(self, k=10, iters=100, plot_cm=False):
        n_genres = len(self.genres)

        train_acc = np.zeros(iters * k)
        test_acc = np.zeros(iters * k)
        cms = np.zeros((iters, n_genres, n_genres))
        clf = self.clf

        self.logger.info('{}-Fold test ({} iterations)'.format(k, iters))
        start = perf_counter()
        for iter in range(iters):
            kf = KFold(n_splits=k, shuffle=True)
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
                self.clf.__class__.__name__
            )

    def get_classifier_obj(self):
        """ Returns the last classifier object used """
        return self.clf


