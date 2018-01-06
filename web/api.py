from web.classifiers import get_dataset_models, _get_valid_dirs

import os.path
import json

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
            available datasets to be chosen as a training set
        """

        exclude_prefixes = ('__', '.')  # Exclusion prefixes for hidden subdirs
        for datasetPath, _ in get_dataset_models(): # Find path of datasets
            pass

        exclude_prefixes = ('__', '.')  # exclusion prefixes
        for _, dirNames, _ in os.walk(datasetPath):
            # Exclude all dirs starting with exclude_prefixes
            dirNames[:] = [dirName
                       for dirName in dirNames
                       if not dirName.startswith(exclude_prefixes)]
            break
        # Now, under 'dirNames', we have an array of our datasets

        datasets_dict = { "datasets": dirNames }; # Build Dictionary
        datasets_JSON = json.dumps(datasets_dict) # Serialize to JSON

        return datasets_JSON

    def get_available_classifiers(self, dataset):
        pass

    def predict_song(self, filepath):
        pass

# Test function only used in the development environment
def main():

    testObject = GenrecAPI()
    testObject.get_available_datasets()
    pass

main()
