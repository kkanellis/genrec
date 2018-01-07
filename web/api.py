from web.classifiers import get_dataset_models

import os.path
import json

class GenrecAPI:
    def __init__(self):
        '''Constructor Method for each object of GenrecAPI Class

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
        print(self.models_dict) # Test

        pass

    def get_available_datasets(self):
        """Get available datasets for training like GTZAN, Spotify
        """

        '''
        exclude_prefixes = ('__', '.')  # Exclusion prefixes for hidden subdirs
        for dataset, _ in get_dataset_models(): # Find path of datasets
            print(dataset)

        '''
        '''exclude_prefixes = ('__', '.')  # exclusion prefixes
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
        '''
        pass
    def get_available_classifiers(self, dataset):
        pass

    def predict_song(self, filepath):
        pass

# Test function only used in the development environment
def main():

    testObject = GenrecAPI()
    #testObject.get_available_datasets()
    pass

main()
