#!/bin/bash

model_name="remote_run"
# Spécifiez le chemin du fichier à rechercher
fichier_a_chercher="api/"+$model_name+".pkl"

# Vérifiez si le fichier existe
if [ -f "$fichier_a_chercher" ]; then
    echo "model chargé"
else
    echo "Le model n'est pas trouvé, chargement du modèle"
    # Exécutez votre script Python alternatif
    python -m api.model_loader $model_name;
fi

uvicorn api.main:app --reload