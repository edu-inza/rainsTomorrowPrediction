# 1. Introduction

Ce repository propose une API pour prédire s'il y aura de la pluie à j+1, en Australie.
2 types de prédiction sont proposés par l'API :
- v1 : prédiction à partir d'une sélection de variables suite à une analyse exploratoire
- v2 : prédiction à partir d'une sélection des variables les plus influentes en utilisant un algorithme de régression logistique

L'api est containerisée avec docker pour l'exécution de tests unitaires et le déploiement dans un kubernetes.
Le déploiement sur kubernetes met en place 3 réplicats et une exposition de l'API sur le port 80.

## Pré-requis techniques :
- optionnel - modules python : nécessaires pour l'exécution de l'api en local (voir fichier /api/requirements.txt)
- git
- docker engine : pour l'exécution des tests unitaires et déployer l'api en environnement de production
- kubernetes : pour déployer l'api en environnement de production

## Lancement automatique :
Le fichier setup.sh permet d'automatiser l'ensemble des process pour les tests et le déploiement de l'apidu modèle de prédiction.

# 2. Description
## 2.1. REST API
### 2.1.1. model.py
Il est composé d'une classe mère, RainsModel, et de 2 classes filles, RainsModelV1 et RainsModelV2

#### **RainsModel**
Cette classe permet :
- l'import de données à partir d'un fichier csv ('rains.csv')
- le data preprocessing :
- la séparation des features et de la target pour appliquer un modèle de machine learning
- la normalisation des données
- l'entrainement du modèle
- la prédiction à partir du modèle de machine learning

L'algorithme de machine learning choisi est la régression logistique.

#### **RainsModelV1**
RainsModelV1 hérite de la classe RainsModel.

En plus des fonctionnalités de la classe mère, elle permet :
- la sélection de variables (variables les plus influentes suite à une analyse exploratoire)
- la tranformation de données sur la sélection des variables afin de pouvoir appliquer un modèle de machine learning

#### **RainsModelV2**
RainsModelV2 hérite de la classe RainsModel.

En plus des fonctionnalités de la classe mère, elle permet :
- la sélection de variables (variables les plus influentes suite à une analyse des coefficients de la régression logistique)
- la tranformation de données sur la sélection des variables afin de pouvoir appliquer un modèle de machine learning

### 2.1.2. api
REST API développée avec FastAPI.

L'api expose 4 endpoints :
- GET /status : teste le bon fonctionnement de l'API
- GET /authorization : teste si l'utilisateur est authentifié et authorisé
Rq : dans cette API, on considère que tout utilisateur authentifié est automatiquement authorisé. Il n'y a pas de gestion des authorisations spécifiques. De plus, la base de données des utilisateurs est un dictionnaire inclus dans le fichier de l'api.
- POST /v1/rainTomorrow/predict : prédiction de pluie à j+1 en Australie, à partir d'une sélection de variables (V1Item)
- POST /v2/rainTomorrow/predict : prédiction de pluie à j+1 en Australie, à partir d'une autre sélection de variables (V2Item)

Les données de l'utilisateur sont passés dans le header, sous forme : `"Authorization" : {"username": username, "password": password}`

Le fichier `curl_cmds.txt` contient les commandes cURL pour tester les endpoints.

Les fichiers `TU_model.py` et `rains_tests_data.txt` permettent d'exécuter des tests unitaires sur le modèle de machine learning.

### 2.1.3. Containerisation avec docker
Un `Dockerfile` permet de créer une image docker. Cette image déploie un serveur pour l'api du modèle de prédiction. 
Dans la création de l'image docker on utilise le fichier `requirements.txt` pour installer tous les modules python nécessaires à la bonne exécution du model.py et api.py.
Le port 8000 est exposé afin de consommer les endpoints de l'api.

Cette image pourra être utilisé dans le cas de tests unitaires ou pour le déploiement dans kubernetes.


## 2.2. Tests unitaires
Les tests unitaires de l'api du modèle de prédiction sont décomposés en 2 parties :
- une 1ere partie concernent les méthodes GET (/status, /authorization)
- une 2e partie concerne les méthodes POST (/v1/rainTomorrow/predict, /v2/rainTomorrow/predict)

### 2.2.1. TU_authorization
Le fichier `TU_api_authorization.py` contient le code des tests unitaires des endpoints /status et /authorization.
Le fichier `Dockerfile` permet de créer une image docker pour ces tests unitaires. Dans la création de l'image on utilise le fichier `requirements.txt` pour installer les modules python nécessaires.
L'image docker contient 2 variables d'environnement :
- API_ADDRESS, initialisé à '127.0.0.1'
- API_PORT, initialisé à '8000'

### 2.2.2. TU_prediction
Le fichier `TU_api_predict.py` contient le code des tests unitaires des endpoints /v1/rainTomorrow/predict et /v2/rainTomorrow/predict.
Le fichier `Dockerfile` permet de créer une image docker pour ces tests unitaires. Dans la création de l'image on utilise le fichier `requirements.txt` pour installer les modules python nécessaires.
L'image docker contient 2 variables d'environnement :
- API_ADDRESS, initialisé à '127.0.0.1'
- API_PORT, initialisé à '8000'

### 2.2.3. Exécution des tests unitaires
Pour l'exécution des tests unitaires, on crée 3 containers docker :
- un pour exposer l'api
- un pour exécuter les tests unitaires des méthodes GET
- un pour exécuter les tests unitaires des méthodes POST

Les logs de l'exécution des tests unitaires sont dans le fichier `api_test.log`, se trouvant dans le volume `/tests_logs`.

Le fichier `docker-compose.yaml` lance les 3 containers afin d'exécuter les tests unitaires.

## 2.3. k8s
Le fichier `k8s-api-deployment.yml` permet de déployer un pod avec un container docker pour l'api du modèle de prédiction. L'api est exposé sur le port 8000. 3 réplicats sont configurés.
Le fichier `k8s-service.yml` permet de déployer un service de type ClusterIP. Ceci permet d'exposer l'API à l'intérieur du cluster.
Le fichier `k8s-ingress.yml` permet de déployer un ingress. Ceci permet d'exposer le service précédemment créé à l'extérieur du cluster.

Si kubernetes est déployé sur une machine virtuelle, pour tester l'api, on peut créer un tunnel ssh entre la machine virtuelle et la machine locale. On peut ensuite accéder à la documentation swagger en accédant au endpoint /docs.
