from flask import Flask, jsonify
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'servidor-bd-ejemplo')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'sre_db')


@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "mensaje": "API SRE desplegada exitosamente",
        "institucion": "SENA - CBA Mosquera",
        "programa": "Analisis y Desarrollo de Software (ADSO)"
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/db-status')
def db_status():
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, connect_timeout=5
    )
    cur = conn.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    conn.close()
    return jsonify({"db_status": "connected", "mysql_version": version[0]})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port)  # nosec B104 - necesario para exponer el contenedor Docker
