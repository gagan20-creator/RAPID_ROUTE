from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(_name_)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="rapidroute",
        user="postgres",
        password="yourpassword",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/ride', methods=['POST'])
def create_ride():
    data = request.get_json()
    rider_id = data.get("rider_id")
    ride_type = data.get("ride_type")  # "quick" or "delayed"
    delay_minutes = data.get("delay_minutes", 0)

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "INSERT INTO rides (rider_id, ride_type, delay_minutes, status) VALUES (%s, %s, %s, %s) RETURNING *;",
        (rider_id, ride_type, delay_minutes, "pending")
    )
    new_ride = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_ride), 201

@app.route('/rides', methods=['GET'])
def list_rides():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM rides;")
    rides = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rides)

if _name_ == '_main_':
    app.run(debug=True)