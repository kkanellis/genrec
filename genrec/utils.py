import os
import contextlib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from itertools import cycle
from json import JSONEncoder
from matplotlib import pylab
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, RobustScaler as Scaler

from genrec.config import GENRES, PLOTS_DIR
from mlxtend.plotting import plot_decision_regions

class JSONEncoderObj(JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_json()
        except:
            pass
        return self.default(obj)

@contextlib.contextmanager
def np_printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    try:
        yield
    finally:
        np.set_printoptions(**original)

def chunks(l, chunk_size):
    for i in range(0, len(l), chunk_size):
        yield l[i:i+chunk_size]

def plot_confusion_matrix(cm, plot_title, filename, genres=None):
    if not genres:
        genres = GENRES

    pylab.clf()
    pylab.matshow(cm, fignum=False, cmap='Blues', vmin=0, vmax=100.0)

    axes = pylab.axes()
    axes.set_xticks(range(len(genres)))
    axes.set_xticklabels(genres, rotation=45)

    axes.set_yticks(range(len(genres)))
    axes.set_yticklabels(genres)
    axes.xaxis.set_ticks_position("bottom")

    pylab.title(plot_title, fontsize=14)
    pylab.colorbar()
    pylab.xlabel('Predicted class', fontsize=12)
    pylab.ylabel('Correct class', fontsize=12)
    pylab.grid(False)
    pylab.show()

    #pylab.savefig(os.path.join(PLOTS_DIR, "cm_%s.eps" % filename), bbox_inches="tight")

def plot_classifier_regions(X, y, clf, clf_name=None, mesh_step=0.4):
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
                'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

    # Use integers for labels
    encoder = LabelEncoder()
    y = encoder.fit_transform(y)

    labels = [ encoder.inverse_transform(idx) for idx in range(10) ]

    # Standarize the input data
    scaler = Scaler()
    X = scaler.fit_transform(X)

    # Apply PCA & train classifier
    pca = PCA(n_components=2, copy=False)
    X = pca.fit_transform(X)

    clf.fit(X, y)

    """
    # create a mesh to plot in
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, mesh_step),
                         np.arange(y_min, y_max, mesh_step))

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    cs = plt.contourf(xx, yy, Z, colors=colors, alpha=0.5, antialiased=True)
    plt.axis('tight')

    # Plot also the training points
    marker_gen = cycle('s^oxv<>')
    for i, color in zip(clf.classes_, colors):
        idx = np.where(y == i)
        plt.scatter(X[idx, 0], X[idx, 1], c=color, label=encoder.inverse_transform(i),
                    marker=next(marker_gen), edgecolor='black', s=20)
    """

    plt.figure(figsize=(12, 12))
    plot_decision_regions(X, y, clf=clf, res=0.2, colors=','.join(colors), y_labels=labels)

    plt.title(f'{clf_name}: Decision Regions')
    plt.axis('tight')
    plt.legend()
    plt.show()

    """
    plt.savefig(
        os.path.join("/home/sfi/Programming/genrec/plots/", f"regions_{clf_name}.eps"),
        bbox_inches="tight",
    )
    plt.savefig(
        os.path.join("/home/sfi/Programming/genrec/plots/", f"regions_{clf_name}.png"),
        bbox_inches="tight",
        dpi=300
    )
    """
    plt.close()

