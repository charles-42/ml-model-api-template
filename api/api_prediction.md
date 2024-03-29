# API pour la prédiction des modèles ML

Cette API permet d'entraîner des modèles ML, de prédire des valeurs à partir de ces modèles, et de planifier des tâches de prédiction.

## Endpoints disponibles

### Entraînement du modèle

- **URL:** `/prediction/train`
- **Méthode HTTP:** POST
- **Description:** Cette endpoint permet d'entraîner un modèle ML.
- **Paramètres de la requête:**
  - `model_name` (str): Nom du modèle à entraîner.
- **Réponse:**
  - JSON représentant les métriques du modèle entraîné.

### Récupération des modèles entraînés

- **URL:** `/prediction/models`
- **Méthode HTTP:** GET
- **Description:** Cette endpoint permet de récupérer la liste des modèles entraînés.
- **Réponse:**
  - Liste JSON représentant les modèles entraînés.

### Mise à jour du nom du modèle

- **URL:** `/prediction/update`
- **Méthode HTTP:** PUT
- **Description:** Cette endpoint permet de mettre à jour le nom du modèle.
- **Paramètres de la requête:**
  - `model_name` (str): Nouveau nom du modèle.
- **Réponse:**
  - JSON avec un message confirmant la mise à jour du nom du modèle.

### Prédiction d'une nouvelle valeur

- **URL:** `/prediction/to_predict`
- **Méthode HTTP:** POST
- **Description:** Cette endpoint permet de prédire une nouvelle valeur à partir d'un modèle entraîné.
- **Paramètres de la requête:**
  - `order` (obj): Entrée pour la prédiction.
- **Réponse:**
  - JSON contenant l'ID de la prédiction créée.

### Récupération d'une prédiction par ID

- **URL:** `/prediction/prediction`
- **Méthode HTTP:** GET
- **Description:** Cette endpoint permet de récupérer une prédiction à partir de son ID.
- **Paramètres de la requête:**
  - `entry_id` (int): ID de la prédiction.
- **Réponse:**
  - JSON contenant la prédiction correspondante à l'ID spécifié.

### Planification des tâches de prédiction

- **URL:** `/prediction/to_schedule`
- **Méthode HTTP:** POST
- **Description:** Cette endpoint permet de planifier des tâches de prédiction.
- **Réponse:**
  - JSON avec un message confirmant la planification des tâches.
