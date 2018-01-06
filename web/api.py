from web.classifiers import get_dataset_models

class GenrecAPI:
    def __init__(self):
        pass

    def get_available_datasets(self):
        """Get available datasets for training like GTZAN, Spotify

        Uses the 'get_dataset_models' function from 'web.classifiers'
        (Another way to do this is by iterating over the 'config.py' file)

        Args:
            self: object of the GenrecAPI Class
        Returns:
            available datasets
        """

        pass

    def get_available_classifiers(self, dataset):
        pass

    def predict_song(self, filepath):
        pass
