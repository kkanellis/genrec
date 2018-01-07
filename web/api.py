from web.classifiers import get_dataset_models

import os.path
import json

class GenrecAPI:
    def __init__(self):
        ''' Constructor Method for each object of GenrecAPI Class

            Constructs `object.models_dict`
        '''

        dict = {} # Init the Dictionary

        # For each dataset
        for dataset, (classifiers, encoderObj, scalerObj) in get_dataset_models():

            # Init object for the dictionary
            dictObject = {
                dataset: {
                    "classifiers": {},
                    "scaler": scalerObj,
                    "encoder": encoderObj
                }
            }

            dict.update(dictObject) # Assign it to the the dictionary

            # Populate the classifiers as 'name: object'
            for classifier in classifiers:
                dict[dataset]["classifiers"][classifier.name] = classifier

        self.models_dict = dict
        # TODO: Test for more than 1 dataset (Spotify, 1MillionSongs, etc)
        #print(self.models_dict) # Test

        pass

    def get_available_datasets(self):
        """ Get available datasets for training like GTZAN, Spotify
            from the corresponding class member of the object
        """

        # Two ways:
        #   -1- list(self.models_dict): returns ['gtzan'],
        #   -2- *dict: returns gtzan

        datasetNames = list(self.models_dict) # Get names from class member
        datasets_dict = { "datasets": datasetNames }; # Build mini-dictionary
        datasets_JSON = json.dumps(datasets_dict) # Serialize it to JSON

        #print(datasets_dict)
        #print(datasets_JSON)

        return datasets_JSON

    def get_available_classifiers(self, dataset):
        pass

    def predict_song(self, filepath):
        pass

# Test function only used in the development environment
def main():

    testObject = GenrecAPI()
    testObject.get_available_datasets()
    #testObject.get_available_datasets()
    pass

main()
