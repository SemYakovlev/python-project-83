import os
import psycopg
from datetime import datetime

def connect_db():
    return psycopg.connect(os.getenv('DATABASE_URL'))


def get_urls():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    url_checks.created_at,
                    url_checks.status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id DESC, url_checks.created_at DESC;
            """)
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


def get_checks(url_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, status_code, h1, title, description, created_at 
                FROM url_checks 
                WHERE url_id = %s 
                ORDER BY id DESC;
            """, (url_id,))
            return cur.fetchall()

def add_check(url_id, status_code):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO url_checks (url_id, status_code, created_at) VALUES (%s, %s, %s);",
                (url_id, status_code, datetime.now()))
            conn.commit()
