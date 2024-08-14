FROM mongo:latest

# Créer un répertoire pour les données
RUN mkdir -p /data

# Copier le fichier JSON dans le conteneur
COPY data.json /data/data.json

# Copier le script d'initialisation dans le répertoire spécial
COPY init.sh /docker-entrypoint-initdb.d/

# Rendre le script exécutable
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
