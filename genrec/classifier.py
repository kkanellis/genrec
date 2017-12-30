#!/usr/bin/python3
import json
import os

from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from genrec.logger import get_logger

supported_classifiers = {
    'knn': KNeighborsClassifier,
    'svm': SVC,
    'dtree': DecisionTreeClassifier,
    'gnb': GaussianNB,
    'perc': Perceptron,
    'mlp': MLPClassifier,
    'ada': AdaBoostClassifier,
}

class Classifier:
    """ Container of sklearn's classifier and extra metadata """
    MANDATORY_CLASSIFIER_METADATA_FIELDS = ['name', 'type', 'dataset']
    OPTIONAL_CLASSIFIER_METADATA_FIELDS = [ ('description', ''), ('clf_kwargs', { })]

    def __init__(self, clf_obj=None, **metadata):
        # Process mandatory fields
        for field in self.MANDATORY_CLASSIFIER_METADATA_FIELDS:
            if field not in metadata:
                raise LookupError(f'Field "{field}" not found in metadata"')

            setattr(self, field, metadata[field])

        self.logger = get_logger(f'classifier ({self.name})')

        # Process optional fields
        for field, default in self.OPTIONAL_CLASSIFIER_METADATA_FIELDS:
            value = metadata[field] if field in metadata else default
            setattr(self, field, value)

        self._init_classifier(clf_obj)

    def _init_classifier(self, clf_obj):
        """ Create new sklearn classifier object or set up the provided one """
        if clf_obj:
            if self.clf_kwargs:
                self.logger.warning("Classifier object is given. Ignoring classifier kwargs...")

            self.clf_obj = clf_obj
        else: # Create new classfier object
            if self.type not in supported_classifiers:
                raise LookupError(f'Type "{self.type}" classifier is NOT supported')

            self.clf_obj = supported_classifiers[self.type](**self.clf_kwargs)

        self.logger.info('Classifier: {} (params={})'.format(
            self.clf_obj.__class__.__name__,
            self.clf_kwargs
        ))

    def __getattr__(self, name):
        """ Delegate method calls to sklearn's classifier object """
        return getattr(self.clf_obj, name)

    @classmethod
    def from_file(cls, metadata_filepath):
        """ Import classifier & metadate from file(s) """
        with open(metadata_filepath, 'r') as fp:
            metadata = json.load(fp)

        clf_path = metadata_filepath[:-len('.json')]
        clf_obj = joblib.load(clf_path)

        return cls(clf_obj=clf_obj, **metadata)

    def to_file(self, filepath):
        """ Export classifier & metadate to file(s) """
        dirpath = os.path.realpath(os.path.dirname(filepath))
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        metadata_fields = self.MANDATORY_CLASSIFIER_METADATA_FIELDS + \
                list(map(lambda x: x[0], self.OPTIONAL_CLASSIFIER_METADATA_FIELDS))
        metadata = { k: getattr(self, k) for k in metadata_fields }

        with open(filepath + '.json', 'w') as fp:
            json.dump(metadata, fp, indent=4)

        joblib.dump(self.clf_obj, filepath)

