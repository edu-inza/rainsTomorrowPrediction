# Import des librairies
import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import confusion_matrix, balanced_accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression

# Variables config
csv_path = "rains.csv"
target_name = "RainTomorrow"

class RainsModel:

    ######################
    #Init
    ######################
    
    def __init__(self):
        self.data = self.importData()
        self.dataPrepocessing()
        self.X = self.data.drop([target_name], axis=1)
        self.y = self.data[target_name]
        self.algoML = LogisticRegression()
    
    
    ######################
    #public methods
    ######################

    def importData(self) -> pd.DataFrame:
        '''Import data from csv'''
        return pd.read_csv(csv_path)

    def processDate(self):
        '''Process date feature : split in 3 columns + drop 'Date' column'''
        # Split in 3 columns : year, month, day
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['year'] = self.data['Date'].dt.year
        self.data['month'] = self.data['Date'].dt.month
        self.data['day'] = self.data['Date'].dt.day
        # Drop date column
        self.data = self.data.drop(['Date'], axis=1)
    
    def processNan(self):
        # Drop 4 columns with more than 30% Nan values
        self.data = self.data.drop(['Cloud9am'], axis=1)
        self.data = self.data.drop(['Evaporation'], axis=1)
        self.data = self.data.drop(['Cloud3pm'], axis=1)
        self.data = self.data.drop(['Sunshine'], axis=1)

        # Drop rows for whiwh "RainTomorrow" = Nan or "RainToday" = Nan
        self.data = self.data.dropna(how='all', subset=['RainTomorrow'], axis=0)
        self.data = self.data.dropna(how='all', subset=['RainToday'], axis=0)

        # Variables quantitatives : remplissage des valeurs avec la valeur médiane de chaque variable
        numerical_data = self.data.select_dtypes(include='float64')
        for col in numerical_data.columns:
            self.data[col] = self.data[col].fillna(self.data[col].median())

        # Variables qualitatives : remplissage des valeurs avec la valeur la plus fréquente
        categorical_data = self.data.select_dtypes(include='O')
        for col in categorical_data.columns:
            self.data[col] = self.data[col].fillna(self.data[col].mode()[0])
    
    def Dict_categorical_data(self, feature : str) -> dict:
        feature_values = self.data[feature].unique()
        result = {}
        for i in range(len(feature_values)):
            result[feature_values[i]] = i
        
        # on stocke le dict pour l'utiliser dans la transformation des données de la prédiction
        if feature == 'Location':
            self.location = result
        elif feature == 'WindGustDir':
            self.windGustDir = result

        return result 

    def replaceCatFeature(self):
        '''Replace categorical features'''
        # RainTomorrow, RainToday
        self.data['RainTomorrow'] = self.data['RainTomorrow'].replace(("No","Yes"),(0,1))
        self.data['RainToday'] = self.data['RainToday'].replace(("No","Yes"),(0,1))

        #'Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm'
        self.data['Location'] = self.data['Location'].replace(self.Dict_categorical_data('Location'))
        self.data['WindGustDir'] = self.data['WindGustDir'].replace(self.Dict_categorical_data('WindGustDir'))
        self.data['WindDir9am'] = self.data['WindDir9am'].replace(self.Dict_categorical_data('WindDir9am'))
        self.data['WindDir3pm'] = self.data['WindDir3pm'].replace(self.Dict_categorical_data('WindDir3pm'))

    def dataPrepocessing(self):
        '''Data cleaning and data preprocessing for machine learning
        Parameter : data : data to clean and process
        Output : processed data'''
        self.processDate()
        self.processNan()
        self.replaceCatFeature()

    def scaleData(self):
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)

    def trainModel(self):
        self.algoML.fit(self.X, self.y)

    def predict(self, inputData):
        if isinstance(inputData, pd.DataFrame):
            data = inputData
        else:
            data = pd.DataFrame(inputData, index=['index'])
        
        return self.algoML.predict(data)

class RainsModelV1(RainsModel):
    def __init__(self):
        super().__init__()
        self.selectFeatures()
        super().scaleData()
        super().trainModel()

    def selectFeatures(self):
        features_selection = ['Humidity9am','Humidity3pm','WindGustSpeed','Pressure9am','MaxTemp','Rainfall','WindGustDir','Location','RainToday','month']
        X = self.data

        for feature in self.data.columns:
            if (feature not in features_selection):
                X = X.drop([feature], axis=1)       
        self.X = X
    
    def transformCatValues(self, inputData):
        if isinstance(inputData, pd.DataFrame):
            data = inputData
        else:
            data = pd.DataFrame(inputData, index=["index"])
        data['RainToday'] = data['RainToday'].replace(("No","Yes"),(0,1))
        data['Location'] = data['Location'].replace(self.location)
        data['WindGustDir'] = data['WindGustDir'].replace(self.windGustDir)

        return data.values.tolist()

class RainsModelV2(RainsModel):
    def __init__(self):
        super().__init__()
        self.selectFeatures()
        super().scaleData()
        super().trainModel()

    def selectFeatures(self):
        features_selection = ['MinTemp','MaxTemp','WindGustSpeed','WindSpeed3pm','Humidity3pm','Pressure9am','Pressure3pm', 'RainToday']
        X = self.data

        for feature in self.data.columns:
            if (feature not in features_selection):
                X = X.drop([feature], axis=1)       
        self.X = X
    
    def transformCatValues(self, inputData):
        if isinstance(inputData, pd.DataFrame):
            data = inputData
        else:
            data = pd.DataFrame(inputData, index=["index"])
        data['RainToday'] = data['RainToday'].replace(("No","Yes"),(0,1))

        return data.values.tolist()