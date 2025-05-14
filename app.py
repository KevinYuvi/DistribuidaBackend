from flask import Flask, request, jsonify
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    return psycopg2.connect(
        dbname='postgress',
        user='postgres',
        password=os.getenv('POSTGRES_PASSWORD'),
        host='db'
    )

@app.route('/add', methods=['POST'])
def add_name():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Name required'}), 400
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO names (name) VALUES (%s)", (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Saved'})

@app.route('/list', methods=['GET'])
def list_names():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM names")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
