import librosa

from genrec.benchmark import ClassifierBenchmark
from genrec.config import *
from genrec.db import Dataset
from genrec.features import FeatureExtractor, TimbralFeatures

# Testcase -> (classifier type, parameters, sanitized name)
testcases = [
    #('knn', { 'clf_kwargs': { 'n_neighbors': 3}, 'name': 'kNN-3' }, 'kNN_3'),
    ('knn', { 'clf_kwargs': { 'n_neighbors': 5}, 'name': 'kNN-5' }, 'kNN_5'),
    #('knn', { 'clf_kwargs': { 'n_neighbors': 7}, 'name': 'kNN-7' }, 'kNN_7'),
    #('knn', { 'clf_kwargs': { 'n_neighbors': 9}, 'name': 'kNN-9' }, 'kNN_9'),
    ('svm', { 'clf_kwargs': { 'kernel': 'linear', 'cache_size': 2000 }, 'name': 'Linear Kernel SVM' }, 'SVM_Linear'),
    ('svm', { 'clf_kwargs': { 'kernel': 'rbf', 'cache_size': 2000, 'gamma': 0.15 }, 'name': 'RBF Kernel SVM' }, 'SVM_RBF'),
    ('dtree', { 'clf_kwargs': { 'criterion': 'entropy'}, 'name': 'Decision Tree' }, 'Decision_Tree'),
    ('ada', { 'clf_kwargs': { 'n_estimators': 50, 'learning_rate': 0.5 }, 'name': 'AdaBoost' }, 'AdaBoost'),
    ('gnb', { 'clf_kwargs': { }, 'name':'Gaussian Naive-Bayes' }, 'GaussianNB'),
    #('mlp', { 'clf_kwargs': { 'hidden_layer_sizes': (20,) } }, 'MLP_1S'),
    #('mlp', { 'clf_kwargs': { 'hidden_layer_sizes': (50,) } }, 'MLP_1M'),
    ('mlp', { 'clf_kwargs': { 'hidden_layer_sizes': (100,) }, 'name': 'MLP'}, 'MLP_1L'),
    #('mlp', { 'clf_kwargs': { 'hidden_layer_sizes': (20, 20) } }, 'MLP_2S'),
    #('mlp', { 'clf_kwargs': { 'hidden_layer_sizes': (50, 50) } }, 'MLP_2M'),
    #('mlp', { 'clf_kwargs': { 'hidden_layer_sizes': (100, 100) } }, 'MLP_2L'),
]

def run_tests():
    ft = FeatureExtractor()
    ds = Dataset(GENRES, ft)

    # Calculate timbral features from GTZAN db
    #ds.load_from_dir(GTZAN_DIR)
    #ds.save('./timbral.json')

    # If already have saved the timbral features
    ds.load_from_file('./db/timbral.json')

    data = ds.get_data()
    for clf_type, clf_params, name in testcases:
        clf = ClassifierBenchmark(clf_type, GENRES, data, **clf_params)
        clf.kfold_test(iters=10, plot_cm=False)
        clf.save('clf_obj/' + name);

if __name__ == '__main__':
    run_tests()

