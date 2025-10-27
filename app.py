import time
import psycopg2
import redis
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Retry logic to wait for PostgreSQL
def connect_postgres(retries=5, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "db"),
                database=os.getenv("POSTGRES_DB", "usersdb"),
                user=os.getenv("POSTGRES_USER", "user"),
                password=os.getenv("POSTGRES_PASSWORD", "password")
            )
            print("Connected to PostgreSQL")
            return conn
        except Exception as e:
            print(f"Postgres connection failed: {e}. Retrying in {delay} sec...")
            time.sleep(delay)
    raise Exception("Could not connect to PostgreSQL")

# Retry logic to wait for Redis
def connect_redis(retries=5, delay=5):
    for i in range(retries):
        try:
            r = redis.Redis(host=os.getenv("REDIS_HOST", "redis_cache"), port=6379)
            r.ping()
            print("Connected to Redis")
            return r
        except Exception as e:
            print(f"Redis connection failed: {e}. Retrying in {delay} sec...")
            time.sleep(delay)
    raise Exception("Could not connect to Redis")

# Connect to databases
conn = connect_postgres()
cache = connect_redis()

# Initialize DB: create table if it doesn't exist
def init_db():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        )
    """)
    conn.commit()
    cur.close()

init_db()

# Helper function to execute SQL safely
def execute_query(query, params=None, fetch=False):
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall()
        else:
            result = None
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

# Routes
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        execute_query(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (data["name"], data["email"])
        )
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = execute_query("SELECT * FROM users", fetch=True)
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = execute_query("SELECT * FROM users WHERE id=%s", (id,), fetch=True)
        if user:
            return jsonify(user[0])
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    try:
        execute_query(
            "UPDATE users SET name=%s, email=%s WHERE id=%s",
            (data["name"], data["email"], id)
        )
        return jsonify({"message": "User updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        execute_query("DELETE FROM users WHERE id=%s", (id,))
        return jsonify({"message": "User deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
