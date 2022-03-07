import requests, os, json, base64
from datetime import datetime

# définition de l'adresse de l'API
api_address = os.environ.get('API_ADDRESS')
#api_address = "127.0.0.1"
# port de l'API
api_port = os.environ.get('API_PORT')
#api_port = "8000"

def set_result(endpoint:str, username:str, password:str, expected_result:int, status_code:int):
    output = '''
    ============================
            Endpoint test
    ============================
        Date : {date_exec}
    ============================

    request done at "'{endpoint}'"
    | username={username}
    | password={password}

    expected result = {expected_result}
    actual result = {status_code}

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
        file.write(output.format(endpoint=endpoint, username=username, password=password, date_exec=now_string, expected_result=expected_result, status_code=status_code, test_status=test_status))

def base64_encode(message: str):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def TU_status():
    r = requests.get(
        url='http://{address}:{port}/status'.format(address=api_address, port=api_port)
    )
    set_result("/status", "", "",200, r.status_code)

def TU_authorization(username:str, password:str, expected_result:int):
    headers_dict = {"Authorization": "Basic " + base64_encode(username +":"+ password)}
    r = requests.get(
        url='http://{address}:{port}/authorization'.format(address=api_address, port=api_port),
        headers= headers_dict
    )
    set_result('/authorization', username, password, expected_result, r.status_code)

TU_status()

TU_authorization("alice", "wonderland", 200)
TU_authorization("bob", "builder1", 401)
TU_authorization("clementine1", "mandarine", 400)