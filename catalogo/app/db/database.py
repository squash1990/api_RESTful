import psycopg2
from flask import g
import os

def get_db():

    db_user = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME', None)

    if 'db' not in g and not db_connection_name:
		# Si no hay "db_connection_name" entonces nos estamos conectando usando 
		# TCP socket, por tanto, necesitamos un HOST y PORT para conectarnos.
        db_host = os.environ.get('DB_HOST')
        db_port = os.environ.get('DB_PORT')
        g.db = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
    if 'db' not in g and db_connection_name:
        # Si existe "db_connection_name" nos estamos conectando a un
		# unix socket, cuyo nombre es google-scpecific.
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        g.db = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=unix_socket,
            database=db_name
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
