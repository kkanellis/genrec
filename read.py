import numpy as np

def au_readframes(au_file, to_read):
    data = b''
    while to_read > 0:
        read = au_file.readframes(to_read)
        if read == b'':
            break # no more data to read

        # append new data
        data += read
        to_read -= len(read) // au_file._framesize

    return np.fromstring(data, dtype=np.int16)


