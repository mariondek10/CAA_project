# Image de base légère Python
FROM python:3.11-slim

# Évite les fichiers .pyc et force les logs à apparaître immédiatement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Répertoire de travail dans le container
WORKDIR /app

# Copie et installe les dépendances en premier (cache Docker optimisé)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code
COPY . .

# Port exposé par Flask
EXPOSE 8080

# Lancement avec Gunicorn (plus robuste que le serveur de dev Flask)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
