# Application de Comptabilité LMNP

Cette application web permet de gérer la comptabilité LMNP (Location Meublée Non Professionnelle) et aide à préparer la déclaration fiscale 2044-SPE.

## Fonctionnalités

- Gestion des comptes utilisateurs (inscription, connexion, déconnexion)
- Gestion des logements (ajout, modification, suppression)
- Gestion des recettes (loyers, charges récupérables)
- Gestion des dépenses (intérêts d'emprunt, frais de gestion, travaux, etc.)
- Calcul automatique des amortissements (immobilier, mobilier, frais de notaire)
- Calcul du résultat fiscal
- Export CSV des écritures comptables
- Génération de PDF récapitulatif pour la déclaration 2044-SPE

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un serveur web (pour la production)

## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-depot>
cd lmnp_app
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet en vous basant sur le fichier `.env.example` :

```bash
cp .env.example .env
```

Puis modifiez le fichier `.env` avec vos propres paramètres.

### 5. Initialiser la base de données

Assurez-vous que votre terminal est à la racine du projet (le dossier contenant `run.py` et le dossier `lmnp_app`).

```bash
export FLASK_APP=run.py # Ou utilisez le fichier .flaskenv
flask db init # Seulement la première fois
flask db migrate -m "Initial migration"
flask db upgrade
```

## Lancement

### En développement

Assurez-vous que votre terminal est à la racine du projet.

```bash
export FLASK_APP=run.py # Ou utilisez le fichier .flaskenv
flask run
```

L'application sera accessible à l'adresse http://localhost:5000

### En production

Pour un déploiement en production sur un VPS, nous recommandons d'utiliser Gunicorn comme serveur WSGI et Nginx comme proxy inverse.

#### Installation de Gunicorn

```bash
pip install gunicorn
```

#### Lancement avec Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

#### Configuration Nginx (exemple)

Créez un fichier de configuration dans `/etc/nginx/sites-available/lmnp_app` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Puis activez le site et redémarrez Nginx :

```bash
ln -s /etc/nginx/sites-available/lmnp_app /etc/nginx/sites-enabled/
systemctl restart nginx
```

## Migration vers PostgreSQL

L'application utilise SQLite par défaut, mais peut facilement être migrée vers PostgreSQL pour une utilisation plus intensive.

### 1. Installer PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Créer une base de données et un utilisateur

```bash
sudo -u postgres psql
```

Dans l'invite PostgreSQL :

```sql
CREATE DATABASE lmnp_db;
CREATE USER lmnp_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE lmnp_db TO lmnp_user;
\q
```

### 3. Modifier la configuration

Dans votre fichier `.env`, modifiez la variable `DATABASE_URL` :

```
DATABASE_URL=postgresql://lmnp_user:votre_mot_de_passe@localhost/lmnp_db
```

### 4. Migrer la base de données

```bash
flask db upgrade
```

## Sauvegarde des données

Pour sauvegarder la base de données SQLite :

```bash
cp app.db app.db.backup
```

Pour PostgreSQL :

```bash
pg_dump -U lmnp_user -W -F t lmnp_db > lmnp_backup.tar
```

## Maintenance

- Vérifiez régulièrement les mises à jour des dépendances
- Effectuez des sauvegardes régulières de la base de données
- Surveillez les logs pour détecter d'éventuels problèmes

## Licence

Ce projet est sous licence [MIT](LICENSE).
