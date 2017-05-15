from json import JSONEncoder
import contextlib

import numpy as np

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

