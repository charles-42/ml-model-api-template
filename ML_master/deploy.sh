#!/bin/bash

# Stopper le script si une commande échoue
set -e

# Optionnel : activer votre environnement virtuel
# source /chemin/vers/votre/environnement/bin/activate

# Mettre à jour pip, setuptools et wheel
echo "Mise à jour de pip, setuptools et wheel..."
pip install --upgrade pip setuptools wheel twine

# Créer les distributions clean
echo "Création des distributions..."
python setup.py sdist bdist_wheel

# Upload la distribution sur PyPI
echo "Upload sur PyPI..."
twine upload dist/*

echo "Terminé."
