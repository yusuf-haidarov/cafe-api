import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("menu.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/menu", methods=["GET"])
def get_menu():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes")
    rows = cursor.fetchall()

    conn.close()

    dishes = []
    for row in rows:
        dishes.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "price": row["price"],
            "available": bool(row["available"])
        })

    return jsonify(dishes)


@app.route("/menu/<int:id>", methods=["GET"])
def get_dish(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE id = ?", (id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "Dish not found"}), 404

    dish = {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": row["price"],
        "available": bool(row["available"])
    }
    return jsonify(dish)


@app.route("/menu", methods=["POST"])
def add_dish():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    available = data.get("available", True)

    if not name or not category or price is None:
        return jsonify({"error": "Fields name, category, price are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO dishes (name, category, price, available) VALUES (?, ?, ?, ?)",
        (name, category, price, 1 if available else 0)
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "available": available
    }), 201


if __name__ == "__main__":
    app.run(debug=True)