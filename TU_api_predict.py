import requests, os, json
from datetime import datetime

# définition de l'adresse de l'API
#api_address = os.environ.get('API_ADDRESS')
api_address = "127.0.0.1"
# port de l'API
#api_port = os.environ.get('API_PORT')
api_port = "8000"

def set_result(endpoint:str, username:str, password:str, expected_result:int, status_code:int, item_dict:dict, score:str):
    output = '''
    ============================
            Endpoint test
    ============================
        Date : {date_exec}
    ============================

    request done at ""{endpoint}'"
    | username={username}
    | password={password}
    | item={item_dict}

    expected result = {expected_result}
    actual result = {status_code}

    score = {score}

    ==>  {test_status}

    '''
    # date et heure d'exécution du test
    now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # affichage des résultats
    if status_code == expected_result:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    # impression dans un fichier
    parent_path = "./logs/"
    with open(os.path.join(parent_path, 'api_test.log'), 'a') as file:
        file.write(output.format(endpoint=endpoint, username=username, password=password, date_exec=now_string, expected_result=expected_result, status_code=status_code, test_status=test_status, item_dict=item_dict, score=score))


def TU_rainTomorrow_predict(username:str, password:str, version:str, item_dict:dict):
    headers_dict = {"Authorization" : json.dumps({
            "username": username,
            "password": password
        }),
        "Content-Type": "application/json"
    }
    r = requests.post(
        url='http://{address}:{port}/{version}/rainTomorrow/predict'.format(address=api_address, port=api_port, version=version),
        headers= headers_dict,
        json=item_dict
    )
    set_result('/{version}/rainTomorrow/predict'.format(version=version), username, password, 200, r.status_code, item_dict, r.text)

# TU
item1_v1_dict = {"Humidity9am": 49,"Humidity3pm": 35,"WindGustSpeed": 30,"Pressure9am": 1018.5,"MaxTemp": 23.9,"Rainfall": 0,"WindGustDir": "WNW","Location": "Brisbane","RainToday": "No","Month" : 9}
item2_v1_dict = {"Humidity9am": 92,"Humidity3pm": 91,"WindGustSpeed": 15,"Pressure9am": 1021.4,"MaxTemp": 15,"Rainfall": 24,"WindGustDir": "SSE","Location": "Brisbane","RainToday": "Yes","Month" : 6}
TU_rainTomorrow_predict("alice", "wonderland", "v1", item1_v1_dict)
TU_rainTomorrow_predict("bob", "builder", "v1", item2_v1_dict)

item1_v2_dict = {"MinTemp": 13.4,"MaxTemp": 23.9,"WindGustSpeed": 30,"WindSpeed3pm": 9,"Humidity3pm": 35,"Pressure9am": 1018.5,"Pressure3pm": 1014.6,"RainToday": "No"}
item2_v2_dict = {"MinTemp": 13.1,"MaxTemp": 19.7,"WindGustSpeed": 15,"WindSpeed3pm": 2,"Humidity3pm": 91,"Pressure9am": 1021.4,"Pressure3pm": 1018.5,"RainToday": "Yes"}
TU_rainTomorrow_predict("alice", "wonderland", "v2", item1_v2_dict)
TU_rainTomorrow_predict("bob", "builder", "v2", item2_v2_dict)