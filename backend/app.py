import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_conn():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        sslmode="require"
    )


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()



@app.route("/")
def home():
    return "Backend is running!"


@app.route("/api/data", methods=["GET"])
def get_data():
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM items")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)


@app.route("/api/data", methods=["POST"])
def add_data():
    init_db()
    data = request.json

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO items (name) VALUES (%s)",
        (data["name"],)
    )

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)