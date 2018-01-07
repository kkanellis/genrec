import json
import os.path

from sklearn.externals import joblib

from genrec.classifier import Classifier
from genrec.logger import get_logger

from web.config import *
from web.utils import scandir_filtered

logger = get_logger('classifiers')

def _get_valid_dirs():
    dirpath = os.path.dirname(__file__)

    filters = [
        (lambda entry: entry.is_dir(), None),
        (lambda entry: entry.name in AVAILABLE_DATASETS,
            lambda entry: logger.debug(f'Ignoring directory "{entry.path}"'))
    ]

    yield from map(
        lambda entry: entry,
        scandir_filtered(dirpath, filters)
    )

def _get_classifiers(dir):
    logger.info(f'Scanning directory "{dir}"...')

    filters = [
        (lambda entry: entry.is_file() and entry.name.endswith('.json'), None),
        (lambda entry: os.path.exists(entry.path[:entry.path.rfind('.json')]),
            lambda entry: logger.warning(
                f'Found metadata file for {entry.name} but obj does NOT exists'
            )
        )
    ]

    for entry in scandir_filtered(dir, filters):
        yield Classifier.from_file(entry.path)

def get_dataset_models():
    for direntry in _get_valid_dirs():
        dataset, dirpath = direntry.name, direntry.path

        clf_encoder_path = os.path.join(dirpath, 'clf_encoder')
        clf_scaler_path = os.path.join(dirpath, 'clf_scaler')

        if not os.path.exists(clf_encoder_path):
            logger.error(f'No label encoder found inside dataset "{dataset}"')
            continue


        if not os.path.exists(clf_scaler_path):
            logger.error(f'No scaler found inside dataset "{dataset}"')
            continue

        encoder, scaler = joblib.load(clf_encoder_path), joblib.load(clf_scaler_path)
        logger.info(f'Encoder found: {encoder.__class__.__name__}')
        logger.info(f'Scaler found: {scaler.__class__.__name__}')

        classifiers = [ clf for clf in _get_classifiers(dirpath) ]

        yield dataset, (classifiers, encoder, scaler)

