#!/usr/bin/python3
import librosa

from genrec.benchmark import ClassifierBenchmark
from genrec.classifier import Classifier
from genrec.config import *
from genrec.db import Dataset
from genrec.features import FeatureExtractor, TimbralFeatures

# Testcases -> list of (classifier parameters, display name) tuples
testcases = [
    ({'type': 'knn', 'clf_kwargs': { 'n_neighbors': 3}, 'name': 'kNN_3' }, 'kNN-3'),
    ({'type': 'knn', 'clf_kwargs': { 'n_neighbors': 5}, 'name': 'kNN_5' }, 'kNN_5'),
    ({'type': 'knn', 'clf_kwargs': { 'n_neighbors': 7}, 'name': 'kNN_7' }, 'kNN_7'),
    ({'type': 'knn', 'clf_kwargs': { 'n_neighbors': 5}, 'name': 'kNN_9' }, 'kNN_9'),
    ({'type': 'svm', 'clf_kwargs': { 'kernel': 'linear', 'cache_size': 2000 }, 'name': 'SVM_Linear' }, 'Linear Kernel SVM'),
    ({'type': 'svm', 'clf_kwargs': { 'kernel': 'rbf', 'cache_size': 2000, 'gamma': 0.15 }, 'name': 'SVM_RBF' }, 'RBF Kernel SVM'),
    ({'type': 'dtree', 'clf_kwargs': { 'criterion': 'entropy'}, 'name': 'Decision_Tree' }, 'Decision Tree'),
    ({'type': 'ada', 'clf_kwargs': { 'n_estimators': 50, 'learning_rate': 0.5 }, 'name': 'AdaBoost' }, 'AdaBoost'),
    ({'type': 'gnb', 'clf_kwargs': { }, 'name':'GaussianNB' }, ' Gaussian Naive-Bayes'),
    ({'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (20,) }, 'name': 'MLP_1S' }, 'MLP_1S'),
    ({'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (50,) }, 'name': 'MLP_1M' }, 'MLP_1M'),
    ({'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (100,) }, 'name': 'MLP_1L'}, 'MLP_1L'),
    ({'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (20, 20) }, 'name': 'MLP_2S' }, 'MLP_2S'),
    ({'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (50, 50) }, 'name': 'MLP_2M' }, 'MLP_2M'),
    ({'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (100,100) }, 'name': 'MLP_2L'}, 'MLP_2L'),
]

def run_tests():
    ft = FeatureExtractor()
    ds = Dataset(GENRES, ft)

    # Calculate timbral features from GTZAN db
    #ds.load_from_dir(GTZAN_DIR)
    #ds.save('./timbral.json')

    # If already have saved the timbral features
    ds.load_from_file('./db/timbral.json')

    data = ds.get_data_as_arrays()
    for clf_params, display_name in testcases:
        # Initialize classifier
        clf_params['dataset'] = 'gtzan'
        clf = Classifier(**clf_params)

        bench = ClassifierBenchmark(clf, GENRES, data, display_name)
        bench.kfold_test(iters=10, plot_cm=False)

if __name__ == '__main__':
    run_tests()

