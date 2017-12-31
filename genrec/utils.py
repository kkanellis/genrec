import os
import contextlib
from json import JSONEncoder
from matplotlib import pylab

import numpy as np

from genrec.config import GENRES, PLOTS_DIR

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
    #pylab.show()
    #pylab.savefig(os.path.join(PLOTS_DIR, "cm_%s.eps" % filename), bbox_inches="tight")



