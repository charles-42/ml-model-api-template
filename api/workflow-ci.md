# Continuous Integration Workflow 

Ce dépôt contient un workflow de Continuous Integration (CI) utilisant GitHub Actions pour exécuter des tests automatisés sur les pull requests effectuées sur la branche principale (`main`). Les tests sont exécutés sur une instance Ubuntu avec Python 3.9.19.

## Prérequis

Avant de pouvoir exécuter ce workflow, assurez-vous que vous disposez des éléments suivants :

- Un compte GitHub avec les autorisations nécessaires pour créer et exécuter des workflows d'actions.
- Un environnement de développement Python.
- Un fichier `requirements.txt` définissant les dépendances du projet.

## Fonctionnement du Workflow

Lorsqu'une pull request est ouverte ou mise à jour sur la branche principale (`main`), ce workflow est déclenché. Voici les étapes exécutées dans ce processus :

1. **Checkout du code :** Le code source de la pull request est récupéré à partir du dépôt GitHub.

2. **Configuration de Python :** La version spécifiée de Python (3.9.19) est configurée pour l'exécution des tests.

3. **Installation des dépendances :** Les dépendances définies dans le fichier `requirements.txt` sont installées à l'aide de `pip`.

4. **Configuration des variables d'environnement :** La variable d'environnement `SECRET_KEY` est configurée en utilisant la valeur stockée dans GitHub.

5. **Exécution des tests :** Les tests sont exécutés à l'aide de Pytest dans le répertoire `api/test`. La couverture de code est mesurée à l'aide de l'option `--cov=api`.


## Variable d'environnement

Ce workflow utilise un secret nommé `SECRET_KEY` pour la configuration de l'environnement. Assurez-vous de configurer ce secret dans les paramètres du dépôt GitHub pour que le workflow puisse fonctionner correctement.

## Auteurs

- Manon Platteau : [@Manonp59](https://github.com/Manonp59)
- Agathe Becquart : [@AgatheBecquart](https://github.com/AgatheBecquart)