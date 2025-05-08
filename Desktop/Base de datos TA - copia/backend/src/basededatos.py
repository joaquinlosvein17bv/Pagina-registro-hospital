import mysql.connector
config = {
    "host": "127.0.0.1",
    "port": "3306",
    "database": "clinica_bienestar",
    "user": "root",
    "password": "Quintanasalas17."
}

def get_db_connection():
    return mysql.connector.connect(**config)
