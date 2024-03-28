FROM python:3.10.14



WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=api:$PYTHONPATH


# Installation de sqlite3
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Copie de tout le contenu du dossier actuel dans /app dans l'image
COPY . .

# Assurez-vous que le script est exécutable
RUN chmod +x ./setup.sh

# Exécution du script setup.sh
RUN ./setup.sh


CMD [ "python3", "api/main.py" ]
