import json
import random
from pathlib import Path

import numpy as np
import librosa


from genrec.logger import get_logger
from genrec.utils import JSONEncoderObj

class Dataset:
    def __init__(self, genres, feature_extractor):
        self.genres = genres
        self.ft_extractor = feature_extractor

        self.logger = get_logger('dataset')

    def load_from_dir(self, dir, **kwargs):
        """ Load dataset from a directory

        Subfolders names must be the same as genre names

        Example of directory structure:
            -rock
                -rock1.au
                -rock2.au
            -jazz
                -jazz1.au
                -jazz2.au
        """
        dir = Path(dir)
        if not dir.is_dir():
            self.logger.error('"{}" is not a directory'.format(dir))
            return

        files = { genre:[] for genre in self.genres }
        for filepath, genre in self._iter_all_files(dir, **kwargs):
            self.logger.debug('Processing "{}"...'.format(filepath))

            aufile, _ = librosa.load( str(filepath) )
            fv = self.ft_extractor.extract(aufile)

            files[genre].append( AudioFile(filepath, genre, fv) )

        for genre in files:
            self.logger.info('[{}]: {} audio files loaded'.format(
                genre, len(files[genre])
            ))

        self.files = files


    def load_from_file(self, filepath):
        """ Load dataset from previously exported json file """
        if not Path(filepath).exists():
            self.logger.error('File "{}" does not exist"'.format(filepath))
            return

        with open(filepath, 'r') as f:
            files = json.load(f)

        # TODO: set intersection (file_genres & dataset_genres)

        self.files = { genre:[] for genre in files.keys() }
        for genre, filelist in files.items():
            for file in filelist:
                self.files[genre].append(AudioFile.from_json(file))

    def get_data(self):
        return self.files

    def save(self, filepath):
        """ Export dataset to file """
        with open(filepath, 'w') as f:
            json.dump(self.files, f, cls=JSONEncoderObj)


    def _iter_genre_files(self, path, genre, n_samples=None, shuffle=False):
        """ Iterates over a subfolder of a specific music genre """
        files = sorted([ file for file in path.iterdir() if file.is_file() ])

        if n_samples and shuffle:
            files = random.sample(files, n_samples)
        elif shuffle:
            random.shuffle(files)
        elif n_samples:
            files = files[:n_samples]

        for file in files:
            yield file, genre


    def _iter_all_files(self, base_path, **kwargs):
        """ Iterates over all subfolders """
        for genre in self.genres:
            path = (base_path / genre)
            yield from self._iter_genre_files(path, genre, **kwargs)


class AudioFile:
    def __init__(self, path, genre, fv):
        self.path = path
        self.name = path.name
        self.genre = genre
        self.fv = fv

    def to_json(self):
        return {
            'path': str(self.path),
            'name': self.name,
            'genre': self.genre,
            'fv': list(self.fv)
        }

    @classmethod
    def from_json(cls, json):
        aufile = cls(
            Path(json['path']),
            json['genre'],
            np.array(json['fv'])
        )
        return aufile

    def __repr__(self):
        return 'AudioFile({})'.format(self.name)


