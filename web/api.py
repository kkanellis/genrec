from web.classifiers import get_dataset_models

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
        '''
            Args:
                dataset(as string)
            Returns:
                available classifiers(as a dictionary)
        '''
        # Init the dictionary that will be returned
        dict1 = {dataset: {"classifiers":{}}}

        for datasetName, (classifiers, _, _) in get_dataset_models():
            # Only for the specific dataset given:
            if (datasetName == dataset):
                # Loop through each classifiers
                for classifier in classifiers: # TODO: Exclude 'dataset' key-value
                    metadata_fields = classifier.MANDATORY_CLASSIFIER_METADATA_FIELDS[:2] + \
                        list(map(lambda x: x[0], classifier.OPTIONAL_CLASSIFIER_METADATA_FIELDS))

                    #print (metadata_fields)
                    # Build a dictionary out of the classifier's name
                    classifierName = getattr(classifier, 'name')
                    dict2 = { classifierName: {}}

                    # Merge the 3 dictionaries
                    dict3 = { k: getattr(classifier, k) for k in metadata_fields[1:] } # Exclude 'name'
                    dict2[classifierName].update(dict3)
                    dict1[dataset]['classifiers'].update(dict2)

        #print(dict1)
        return dict1

    def predict_song(self, filepath):
        pass

# Test function only used in the development environment
def main():

    testObject = GenrecAPI()
    testObject.get_available_classifiers("gtzan")
    #testObject.get_available_datasets()
    pass

main()
