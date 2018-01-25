import json
import librosa
import numpy as np
import operator

from genrec.features import FeatureExtractor
from web.classifiers import get_dataset_models

class GenrecAPI:
    def __init__(self):
        """
        Constructor Method for each object of GenrecAPI Class

        Constructs `object.models_dict`
        """
        dict = { } # Init the Dictionary

        # For each dataset
        for dataset, (classifiers, encoder, scaler) in get_dataset_models():
            # Init object for the dictionary
            dataset_dict = {
                dataset: {
                    "classifiers": {},
                    "scaler": scaler,
                    "encoder": encoder
                }
            }
            dict.update(dataset_dict) # Assign it to the the dictionary

            # Populate the classifiers as 'name: object'
            for classifier in classifiers:
                dict[dataset]["classifiers"][classifier.name] = classifier

        self.models_dict = dict
        self.features_extractor = FeatureExtractor()

    def get_available_datasets(self):
        """ Get available datasets for training like GTZAN, Spotify
            from the corresponding class member of the object

            Returns:
                available datasets (dictionary) as JSON
        """

        # Two ways:
        #   -1- list(self.models_dict): returns ['gtzan'],
        #   -2- *dict: returns gtzan

        datasetNames = list(self.models_dict) # Get names from class member
        datasets_dict = { "datasets": datasetNames } # Build mini-dictionary
        datasets_JSON = json.dumps(datasets_dict) # Serialize it to JSON

        #print(datasets_dict)
        #print(datasets_JSON)

        return datasets_JSON

    def get_available_classifiers(self, dataset):
        '''
            Args:
                dataset(as string)
            Returns:
                available classifiers (dictionary) as JSON
        '''
        # Init the dictionary that will be returned
        dict1 = {dataset: {"classifiers":{}}}

        dictToSearch = self.models_dict[dataset]["classifiers"]
        for classifierName in dictToSearch:

            # Get value of key/classifierName
            classifierObject = dictToSearch[classifierName]

            # Get specific metadata fields
            metadata_fields = classifierObject.MANDATORY_CLASSIFIER_METADATA_FIELDS[:2] + \
                list(map(lambda x: x[0], classifierObject.OPTIONAL_CLASSIFIER_METADATA_FIELDS))

            # Build a dictionary out of the classifier's name
            classifierName = getattr(classifierObject, 'name')
            dict2 = { classifierName: {}}

            # Merge the 3 dictionaries
            dict3 = { k: getattr(classifierObject, k) for k in metadata_fields[1:] } # Exclude 'name'
            dict2[classifierName].update(dict3)
            dict1[dataset]['classifiers'].update(dict2)

        #dict1_JSON = json.dumps(dict1)
        return dict1

    def predict_song(self, filepath, dataset, classifier):
        # Read audio file
        sig, _ = librosa.load(filepath, sr=22050, res_type='kaiser_fast')

        # Extract feature vectors
        fvs = list(self.features_extractor.extract_fvs(sig))
        fv = self.features_extractor.extract_fv(sig)

        if dataset not in self.models_dict:
            raise Exception(f"Invalid dataset: {dataset}")

        # Retrieve classifiers, scaler & encoder
        models = self.models_dict[dataset]
        scaler, encoder = models["scaler"], models["encoder"]

        try:
            clf = models["classifiers"][classifier]
        except KeyError:
            raise Exception(f"Invalid classifier ({classifier})")

        # Feature vectors for each interval
        nonsilent_wnds_idx = [ idx for idx, fv in enumerate(fvs) if fv ]
        X = np.array([ fvs[idx] for idx in nonsilent_wnds_idx ] + [fv])
        X = scaler.transform(X)

        # Prediction probabilities using the desired classifier
        proba = clf.predict_proba(X)
        predictions = { idx : proba[i].tolist() for i, idx in enumerate(nonsilent_wnds_idx) }

        # Prediction for the whole audio file
        overall_proba = proba[-1]
        overall_class, overall_confidence = max(enumerate(overall_proba), key=operator.itemgetter(1))
        overall_class = encoder.inverse_transform(np.array(overall_class))

        return {
            "prediction_interval_secs": 1,
            "predictions": predictions,
            "overall_prediction_class": overall_class,
            "overall_prediction_confidence": overall_confidence * 100,
            "genres": encoder.classes_.tolist(),
        }

if __name__ == '__main__':
    testObject = GenrecAPI()
    #testObject.get_available_classifiers("gtzan")
    #testObject.get_available_datasets()
    print(testObject.predict_song("./web/youtube.opus", "gtzan", "Ensemble"))

