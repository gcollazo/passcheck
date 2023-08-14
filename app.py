import os

import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


@app.get("/")
def index_page():
    return render_template("index.html")


@app.get("/check")
def handle_form():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, value FROM passwords WHERE value = %s",
        (request.args.get("password"),),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    is_bad_password = False

    if len(rows) > 0:
        is_bad_password = True

    return render_template(
        "check.html",
        password=request.args.get("password"),
        is_bad_password=is_bad_password,
    )
