# Exercice 4 : Orchestration d'une application Web avec Docker

## Objectif
Déployer une application complète avec Docker Compose comprenant :

- **Flask** pour l'API web
- **PostgreSQL** pour stocker les utilisateurs
- **Redis** pour le cache
- **Adminer** pour administrer la base

## Structure de la stack

### Services Docker
1. **web (Flask)**
   - Connexion à PostgreSQL (`db`) et Redis (`cache`)
   - Endpoints CRUD :
     - `POST /users` : créer un utilisateur
     - `GET /users` : lister tous les utilisateurs
     - `GET /users/<id>` : récupérer un utilisateur
     - `PUT /users/<id>` : mettre à jour un utilisateur
     - `DELETE /users/<id>` : supprimer un utilisateur
   - Endpoint `/health` pour le health check (DB + Redis)

2. **db (PostgreSQL)**
   - Base `usersdb` avec table `users`
   - Volumes persistants (`db_data`)
   - Health check intégré via Docker

3. **cache (Redis)**
   - Cache pour la session / test rapide
   - Health check intégré via Docker

4. **adminer**
   - Interface web pour gérer PostgreSQL
   - Accessible sur `http://localhost:8080`

### Points clés
- Les variables d'environnement sont utilisées pour configurer DB et Redis.
- Les conteneurs dépendent les uns des autres (`depends_on`) pour que Flask attende DB et Redis.
- Les health checks permettent de détecter rapidement si un service est indisponible.
- La table `users` est créée automatiquement à l'initialisation si elle n'existe pas.

---

## Tests à réaliser

1. Health check : `http://localhost:5000/health`
2. Création d’un utilisateur : `POST /users`
3. Listing des utilisateurs : `GET /users`
4. Récupération d’un utilisateur : `GET /users/<id>`
5. Mise à jour d’un utilisateur : `PUT /users/<id>`
6. Suppression d’un utilisateur : `DELETE /users/<id>`
7. Accéder à Adminer : `http://localhost:8080`

---

## Commandes Docker utiles

- Lancer la stack :  
```bash
docker compose up -d --build
Voir les logs :

bash
Copier le code
docker compose logs -f
Vérifier les conteneurs :

bash
Copier le code
docker ps
Arrêter la stack :

bash
Copier le code
docker compose down