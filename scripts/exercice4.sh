
---

## 2`exercice4.sh`

```bash
#!/bin/bash
# Script pour lancer et tester l'exercice 4

echo "=== Lancement des conteneurs ==="
docker compose up -d --build

echo "=== Vérification des conteneurs ==="
docker ps

echo "=== Test health check Flask ==="
curl -s http://localhost:5000/health | jq

echo "=== Test création utilisateur ==="
curl -s -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{"name":"Alice","email":"alice@example.com"}' | jq

echo "=== Test listing utilisateurs ==="
curl -s http://localhost:5000/users | jq

echo "=== Test récupération utilisateur ID=1 ==="
curl -s http://localhost:5000/users/1 | jq

echo "=== Test mise à jour utilisateur ID=1 ==="
curl -s -X PUT http://localhost:5000/users/1 \
-H "Content-Type: application/json" \
-d '{"name":"Alice Smith","email":"alice.smith@example.com"}' | jq

echo "=== Test suppression utilisateur ID=1 ==="
curl -s -X DELETE http://localhost:5000/users/1 | jq

echo "=== Tous les tests terminés ==="
