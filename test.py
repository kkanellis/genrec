import librosa

from genrec.classifier import MusicGenreClassifier
from genrec.config import *
from genrec.db import Dataset
from genrec.features import FeatureExtractor, TimbralFeatures

clf_params = [
    #{'type': 'knn', 'clf_kwargs': { 'n_neighbors': 3}  },
    {'type': 'knn', 'clf_kwargs': { 'n_neighbors': 5}, 'name': 'k-NN' },
    #{'type': 'knn', 'clf_kwargs': { 'n_neighbors': 7}  },
    #{'type': 'knn', 'clf_kwargs': { 'n_neighbors': 9}  },
    {'type': 'svm', 'clf_kwargs': { 'kernel': 'linear', 'cache_size': 2000 }, 'name': 'Linear Kernel SVM'},
    {'type': 'svm', 'clf_kwargs': { 'kernel': 'rbf', 'cache_size': 2000, 'gamma': 0.15 }, 'name': 'RBF Kernel SVM'},
    {'type': 'dtree', 'clf_kwargs': { 'criterion': 'entropy'}, 'name': 'Decision Tree'},
    {'type': 'ada', 'clf_kwargs': { 'n_estimators': 100, 'learning_rate': 0.5 }, 'name': 'AdaBoost'},
    {'type': 'gnb', 'clf_kwargs': { }, 'name':'Gaussian Naive-Bayes'},
    #{'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (20,) } },
    #{'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (50,) } },
    {'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (100,) }, 'name': 'MLP'},
    #{'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (20, 20) } },
    #{'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (50, 50) } },
    #{'type': 'mlp', 'clf_kwargs': { 'hidden_layer_sizes': (100, 100) } },
]

def test():
    ft = FeatureExtractor()
    ds = Dataset(GENRES, ft)

    # Calculate timbral features from GTZAN db
    #ds.load_from_dir(GTZAN_DIR)
    #ds.save('./timbral.json')

    # If already have saved the timbral features
    ds.load_from_file('./db/timbral.json')

    data = ds.get_data()
    for clf_param in clf_params:
        clf = MusicGenreClassifier(GENRES, data, **clf_param)
        clf.kfold_test(iters=10, plot_cm=True)

if __name__ == '__main__':
    test()

