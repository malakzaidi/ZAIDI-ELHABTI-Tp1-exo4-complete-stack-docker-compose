# TP1 Exercice 4 : Stack Complète avec Docker Compose

> **Orchestration d’une application web complète avec base de données et cache à l’aide de Docker Compose**


<img width="836" height="886" alt="image" src="https://github.com/user-attachments/assets/d4baaece-f6bc-483e-b452-ad1cfbbfbd85" />


Ce projet met en œuvre une **stack applicative complète** composée de :
- Une **application web** (Node.js + Express)
- Une **base de données** (MySQL)
- Un **système de cache** (Redis)

Le tout est orchestré via **Docker Compose**, permettant un déploiement rapide, reproductible et isolé.

---

## 📋 Sommaire

- [Aperçu](#aperçu)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancement](#lancement)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Configuration](#configuration)
- [Tests](#tests)
- [Arrêt et nettoyage](#arrêt-et-nettoyage)
- [Dépannage](#dépannage)
- [Auteurs](#auteurs)

---

## Aperçu

Ce projet illustre une architecture microservices légère mais réaliste :
- L’**application web** expose une API REST simple.
- Elle **persiste les données** dans une base MySQL.
- Elle utilise **Redis** comme cache pour accélérer les requêtes fréquentes.
- Tout est **containerisé** et orchestré avec `docker-compose.yml`.

---

## Architecture

```
+----------------+       +----------------+       +----------------+
|   Frontend     | <---> |  API (Node.js) | <---> |  MySQL         |
|   (Browser)    |       |  (app)         |       |  (DB)          |
+----------------+       +--------+-------+       +--------+-------+
                                  ^                    ^
                                  |                    |
                             +----+-----+      +-------+--------+
                             |  Redis   |      | Docker Network |
                             | (Cache)  |      | (bridge)       |
                             +----------+      +----------------+
```

---

## Prérequis

Assurez-vous d’avoir installé :

- [Docker](https://www.docker.com/get-started) (≥ 20.10)
- [Docker Compose](https://docs.docker.com/compose/install/) (≥ v2.0)
- Un terminal (Linux, macOS, ou Windows avec WSL2)

> Vérifiez avec :
> ```bash
> docker --version
> docker compose version
> ```

---

## Installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/malakzaidi/ZAIDI-ELHABTI-Tp1-exo4-complete-stack-docker-compose.git
   cd ZAIDI-ELHABTI-Tp1-exo4-complete-stack-docker-compose
   ```

2. **Vérifiez la présence des fichiers** :
   - `docker-compose.yml`
   - `app/` (code de l’application Node.js)
   - `docker/` (Dockerfiles si nécessaire)
   - `.env` (variables d’environnement)

---

## Lancement

### Démarrer toute la stack

```bash
docker compose up -d
```

> L’option `-d` lance les conteneurs en arrière-plan.

### Vérifier que tout fonctionne

```bash
docker compose ps
```

Vous devriez voir 3 services en état `Up` :
- `app` (port 3000)
- `mysql` (port 3306)
- `redis` (port 6379)

---

## Utilisation

### Accéder à l’API

Ouvrez votre navigateur ou utilisez `curl` :

```bash
curl http://localhost:3000
```

**Endpoints disponibles** :

| Méthode | URL               | Description |
|--------|-------------------|-----------|
| `GET`  | `/`               | Message de bienvenue |
| `GET`  | `/users`          | Liste les utilisateurs (avec cache Redis) |
| `POST` | `/users`          | Ajoute un utilisateur (JSON) |

#### Exemple : Ajouter un utilisateur

```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

> La première requête `/users` sera lente (lecture DB), les suivantes seront **instantanées** grâce au cache Redis.

---

## Structure du projet

```
.
├── docker-compose.yml          # Orchestration des services
├── .env                        # Variables d'environnement
├── app/
│   ├── server.js               # Application Express
│   ├── db.js                   # Connexion MySQL
│   ├── cache.js                # Client Redis
│   └── package.json
├── docker/
│   └── app.Dockerfile          # (Optionnel) Image personnalisée
└── README.md                   # Ce fichier
```

---

## Configuration

### Fichier `.env`

```env
# MySQL
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=appdb
MYSQL_USER=appuser
MYSQL_PASSWORD=apppass

# Redis
REDIS_PASSWORD=redispass

# App
PORT=3000
DB_HOST=mysql
REDIS_HOST=redis
```

> **Ne commitez jamais `.env` en production !** Utilisez `.gitignore`.

---

## Tests

### Vérifier la connexion à MySQL

```bash
docker exec -it mysql mysql -u appuser -p'apppass' -e "SELECT NOW();"
```

### Vérifier Redis

```bash
docker exec -it redis redis-cli -a redispass PING
# Réponse attendue : PONG
```

### Logs de l’application

```bash
docker compose logs -f app
```

---

## Arrêt et nettoyage

### Arrêter les conteneurs

```bash
docker compose down
```

### Supprimer les volumes (données persistantes)

```bash
docker compose down -v
```

> Attention : cela supprime la base de données !

---

## Dépannage

| Problème | Solution |
|--------|---------|
| `Connection refused` MySQL | Attendez 10-20s après `up` (initialisation DB) |
| Port 3000 déjà utilisé | Changez `PORT` dans `.env` ou libérez le port |
| Redis auth failed | Vérifiez `REDIS_PASSWORD` dans `.env` et `docker-compose.yml` |
| Données non persistantes | Vérifiez les volumes dans `docker-compose.yml` |

---

## Auteurs

- **Malak Zaidi** – [malakzaidi](https://github.com/malakzaidi)
- **Elhabti** – Co-auteur

---

## Licence

Ce projet est à usage pédagogique dans le cadre du TP1.

---

> **Projet réalisé avec ❤️ pour l'apprentissage de Docker & Docker Compose**
```

Votre dépôt sera désormais **professionnel, clair et prêt pour l’évaluation** !  
Besoin d’une version anglaise ou d’un badge ? Dites-moi !
