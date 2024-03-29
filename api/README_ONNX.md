
# Modèle de data-api

## Objectif

L'objectif de ce projet est de fournir un modèle standard pour la création d'une API de données. 

Il comprend :

- La procédure de construction d'une base de données SQL (SQLite).
- La procédure d'importation des données.
- Une API (FastAPI) avec une authentification basée sur des tokens.
- Des points de terminaison pour effectuer des opérations CRUD sur la table des clients.
- Des tests des points de terminaison liés aux opérations CRUD et à l'authentification.

## Configuration

1. Créez un environnement virtuel et installez les exigences depuis "requirements.txt":

```bash
python3 -m venv env
pip install -r requirements.txt
  
```
il vous manquera c'est instalation suivante
```
pip install onnxruntime      
pip install skl2onnx onnxruntime  

pip install python-jose
pip install passlib
pip install python-dotenv
pip install fastapi==0.95.0   --> cette version pour fonctionner avec "pydantic"
pip install bcrypt
pip install onnxmltools  
pip install pandas
pip install python-multipart 
pip install uvicorn
pip uninstall pydantic

```   
2. Pour créer la base de données Olist, exécutez ces deux commandes :

```bash
sqlite3 olist.db < database_building/create_table.sql
sqlite3 olist.db < database_building/import_table.sql 2>/dev/null
```
ou sous windows 
```powershell
cat .\database_building\create_table.sql | sqlite3 olist.db
cat .\database_building\import_table.sql | sqlite3 olist.db
```

3. Créez des variables d'environnement ;

Dans le dossier api, créez un fichier .env avec une variable SECRET_KEY

4. Vous pouvez exécuter des tests pour vous assurer que la configuration est bonne :

```bash
pytest
```

5. Lancez l'API depuis le dossier api :

```bash
python3 api/main.py
```
ou faire pour éviter d'arrêter est redémarré l'API
```
uvicorn main:app --reload
```

6. Utilisez l'API :

- vérifiez que l'api fonctionne à partir de la racine /
- Allez à /docs pour utiliser l'api
- Utilisez le point de terminaison "get customers" pour tester le point de terminaison non protégé
- Créez un utilisateur avec un mot de passe et un nom d'utilisateur
- Autorisez-vous avec l'utilisateur créé
- Vous pouvez maintenant utiliser les points de terminaison protégés

## Ressources :

- https://fastapi.tiangolo.com/tutorial/security/
- https://github.com/ArjanCodes/examples/tree/main/2023/fastapi-router
- https://github.com/ArjanCodes/examples/tree/main/2023/apitesting

## Modifications

- Le modèle ML a été modifié pour créer un fichier ONNX au lieu d'un pickle.
- Le fichier ONNX permet plus de compatibilité que le fichier PICKLE(pickle ne fonctionne que sous `python`).
- Les bibliothèques supplémentaires ont été ajoutées pour faire fonctionner l'API FastAPI. Ces bibliothèques sont installées en plus des exigences déjà installées dans "requirements.txt".



## Transformation du modèle en ONNX

Dans le fichier `analyse/3_modelisation ONNX.py`, le modèle de machine learning est transformé en ONNX. Le code commence par importer les bibliothèques nécessaires et établir une connexion à la base de données SQLite. Ensuite, il lit la table `TrainingDataset` dans un DataFrame pandas et supprime les valeurs manquantes. Il définit ensuite `score` comme la variable cible et `produit_recu` et `temps_livraison` comme les variables d'entrée. Il divise ensuite les données en ensembles d'entraînement et de test.

Il instancie un modèle de régression logistique et l'entraîne sur les données d'entraînement. Ensuite, il convertit le modèle entraîné en ONNX en utilisant la fonction `convert_sklearn` de la bibliothèque `skl2onnx` car nous avons utiliser des model sklearn dans le cas ou nous aurions pris un autre model exemple (pour `tensorflow`  `tf2onnx` ). Il spécifie le type de données d'entrée pour la conversion, qui est un tenseur flottant de taille indéfinie et de deux colonnes. Enfin, il enregistre le modèle ONNX dans un fichier.

Dans le fichier `utils.py`, la fonction `modelisation` entraîne le modèle, le convertit en ONNX et le sauvegarde. Elle renvoie également un dictionnaire contenant les métriques du modèle. La fonction `train` appelle la fonction `modelisation` pour entraîner le modèle et renvoie les métriques du modèle.

# ne pas oublier de faire les pip install
pip install onnxruntime   (pour faire fonctionner onnx de base)
pip install skl2onnx        (pour faire enregister le model onnx de sklearn)
