FROM python:3.10.14

# Création d'un utilisateur non root pour une meilleure sécurité
RUN useradd -m myuser

WORKDIR /.

# Installation de sqlite3
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*

COPY setup.sh .
COPY requirements.txt .
COPY database_building/ database_building/


# Assurez-vous que le script est exécutable
RUN chmod +x ./setup.sh

# Copie des fichiers et dossiers nécessaires


RUN ./setup.sh

COPY . .

# Changement de l'utilisateur à non root
USER myuser

CMD [ "python3", "api/main.py" ]