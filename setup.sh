#!/bin/sh

python3 -m venv env
. env/bin/activate

# Mise à jour de pip et installation des dépendances
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Configuration de la base de données SQLite
sqlite3 olist.db < database_building/create_table.sql
sqlite3 olist.db < database_building/import_table.sql 2>/dev/null

# Définition du chemin pour pytest et exécution des tests
PYTHONPATH=api:$PYTHONPATH pytest

pytest