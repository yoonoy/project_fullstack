import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT)")
    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s)", (data["name"],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "added"})

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
