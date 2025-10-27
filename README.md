# Fullstack App - Exercice 4 TP Orchestration Docker Compose

> **Orchestration complète d’une API Flask (Python) avec PostgreSQL, Redis et Adminer via Docker Compose**

<img width="788" height="606" alt="image" src="https://github.com/user-attachments/assets/549e9df9-f569-48a7-8931-0518a72689fe" />


Ce projet met en œuvre une **stack fullstack containerisée** avec :
- Une **API REST CRUD** en **Python Flask**
- Une base de données **PostgreSQL** (persistance)
- Un **cache Redis** pour les sessions utilisateur
- **Adminer** pour administrer la base
- **Health checks** et **dépendances entre services**

---

## 📋 Sommaire

- [Aperçu](#aperçu)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Lancement](#lancement)
- [Endpoints API](#endpoints-api)
- [Accès à Adminer](#accès-à-adminer)
- [Tests de connectivité](#tests-de-connectivité)
- [Health Checks](#health-checks)
- [Arrêt et nettoyage](#arrêt-et-nettoyage)
- [Dépannage](#dépannage)
- [Auteurs](#auteurs)

---

## Aperçu

Une API Flask expose des **opérations CRUD** sur des utilisateurs :
- Stockage persistant dans **PostgreSQL**
- Cache des sessions avec **Redis**
- Administration visuelle via **Adminer**
- Tout est orchestré avec **Docker Compose**

---

## Architecture

```
+----------------+       +----------------+       +----------------+
|   Client       | <---> |   Flask API    | <---> |  PostgreSQL    |
| (curl/Postman) |       |    (web)       |       |     (db)       |
+----------------+       +--------+-------+       +--------+-------+
                                  ^                    ^
                                  |                    |
                             +----+-----+      +-------+--------+
                             |  Redis   |      | Docker Network |
                             | (cache)  |      | (bridge)       |
                             +----------+      +-------+--------+
                                          \
                                      +----------+
                                      | Adminer  |
                                      | (admin)  |
                                      +----------+
```

---

## Prérequis

- [Docker](https://www.docker.com/get-started) (≥ 20.10)
- [Docker Compose](https://docs.docker.com/compose/install/) (≥ v2.0)

> Vérifiez :
> ```bash
> docker --version
> docker compose version
> ```

---

## Structure du projet

```
fullstack-app/
├── docker-compose.yml
├── .env
├── web/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── data/                   # Volume persistant (créé automatiquement)
└── README.md
```

---

## Installation

1. **Créez le dossier et entrez-y** :
   ```bash
   mkdir fullstack-app && cd fullstack-app
   ```

2. **Créez la structure** :
   ```bash
   mkdir web && touch web/app.py web/requirements.txt web/Dockerfile .env docker-compose.yml
   ```

3. **Collez les fichiers** (voir sections ci-dessous)

---

## Lancement

```bash
docker compose up -d
```

> Attend 15-20 secondes pour l'initialisation de PostgreSQL.

Vérifiez les conteneurs :
```bash
docker compose ps
```

---

## Endpoints API

| Méthode | URL                  | Description |
|--------|----------------------|-----------|
| `POST`   | `/users`             | Créer un utilisateur |
| `GET`    | `/users`             | Lister tous les utilisateurs |
| `GET`    | `/users/<id>`        | Récupérer un utilisateur |
| `PUT`    | `/users/<id>`        | Mettre à jour un utilisateur |
| `DELETE` | `/users/<id>`        | Supprimer un utilisateur |

### Exemple : Créer un utilisateur

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

### Lister les utilisateurs

```bash
curl http://localhost:5000/users
```

---

## Accès à Adminer

Ouvrez dans le navigateur :
[http://localhost:8080](http://localhost:8080)

**Identifiants Adminer** :
- **Système** : `PostgreSQL`
- **Serveur** : `db`
- **Utilisateur** : `appuser`
- **Mot de passe** : `apppass`
- **Base de données** : `appdb`

---

## Tests de connectivité

### 1. Vérifier Flask
```bash
curl http://localhost:5000/
```

### 2. Vérifier PostgreSQL
```bash
docker exec -it db psql -U appuser -d appdb -c "SELECT NOW();"
```

### 3. Vérifier Redis
```bash
docker exec -it cache redis-cli PING
# → PONG
```

### 4. Vérifier Adminer
→ Ouvrir [http://localhost:8080](http://localhost:8080)

---

## Health Checks

Tous les services ont un **health check** configuré :

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

- **Flask** : `GET /health`
- **PostgreSQL** : `pg_isready`
- **Redis** : `redis-cli ping`
- **Adminer** : vérification du port

---

## Fichiers clés

### `web/requirements.txt`
```txt
Flask==2.3.3
psycopg2-binary==2.9.7
redis==5.0.1
gunicorn==21.2.0
```

### `web/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### `.env`
```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppass
POSTGRES_DB=appdb
POSTGRES_HOST=db

REDIS_HOST=cache
REDIS_PORT=6379

FLASK_ENV=production
```

### `docker-compose.yml` (extrait clé)
```yaml
services:
  web:
    build: ./web
    ports:
      - "5000:5000"
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7
    command: redis-server --requirepass redispassword
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## Arrêt et nettoyage

```bash
# Arrêter
docker compose down

# Supprimer les volumes (données perdues)
docker compose down -v
```

---

## Dépannage

| Problème | Solution |
|--------|---------|
| `web` ne démarre pas | Attendez que `db` soit `healthy` (`depends_on`) |
| Connexion PostgreSQL refusée | Vérifiez `.env` et redémarrez |
| Redis auth error | Mot de passe dans `docker-compose.yml` doit être `redispassword` |
| Port 5000/8080 occupé | Changez les ports dans `docker-compose.yml` |

---

## Auteurs

- **ZAIDI Malak**
- **ELHABTI**

---

## Licence

Projet réalisé dans le cadre du **TP Orchestration Docker Compose**.

---

> **Stack prête à l’emploi, robuste et pédagogique**
```
