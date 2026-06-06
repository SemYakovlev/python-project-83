import os
import psycopg
from datetime import datetime

def connect_db():
    return psycopg.connect(os.getenv('DATABASE_URL'))


def get_urls():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM urls ORDER BY id;")
            return cur.fetchall()


def get_url_by_id(id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM urls WHERE id = %s;", (id,))
            return cur.fetchone()


def get_url_by_name(name):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM urls WHERE name = %s;", (name,))
            return cur.fetchone()


def add_url(name):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;",
                (name, datetime.now())
            )
            url_id = cur.fetchone()[0]
            conn.commit()
            return url_id