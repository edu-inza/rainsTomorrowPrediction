from model import RainsModelV1, RainsModelV2
import pandas as pd

# Tests data
# Data processing
def Dict_categorical_data(feature : str, feature_values) -> dict:
    result = {}
    for i in range(len(feature_values)):
        result[feature_values[i]] = i
    return result 

# TODO : modifier pour appeler la méthode transformCatValues
def importAndProcessTestDatav1() -> pd.DataFrame:
    v1_tests_data = pd.read_excel("rains_tests_data.xlsx", ["v1_tests_data"])
    X_v1 = v1_tests_data['v1_tests_data'].drop(['Date', 'RainTomorrow'], axis=1)

    X_v1['RainToday'] = X_v1['RainToday'].replace(("No","Yes"),(0,1))
    X_v1['WindGustDir'] = X_v1['WindGustDir'].replace(Dict_categorical_data('WindGustDir', X_v1['WindGustDir'].unique()))
    X_v1['Location'] = X_v1['Location'].replace(Dict_categorical_data('Location', X_v1['Location'].unique()))

    return X_v1

def importAndProcessTestDatav2() -> pd.DataFrame:
    v2_tests_data = pd.read_excel("rains_tests_data.xlsx", ["v2_tests_data"])
    X_v2 = v2_tests_data['v2_tests_data'].drop(['RainTomorrow'], axis=1)

    X_v2['RainToday'] = X_v2['RainToday'].replace(("No","Yes"),(0,1))

    return X_v2

# TU v1 model
X_v1 = importAndProcessTestDatav1()
rains_model = RainsModelV1()
rainTomorrow_v1 = rains_model.predict(X_v1)

print("prédictions v1 : ", rainTomorrow_v1)

# TU v2 model
X_v2 = importAndProcessTestDatav2()
rains_model = RainsModelV2()
rainTomorrow_v2 = rains_model.predict(X_v2)

print("prédictions v2 : ", rainTomorrow_v2)