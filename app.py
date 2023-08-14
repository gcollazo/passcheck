from flask import Flask, render_template, request

app = Flask(__name__)


@app.get("/")
def index_page():
    return render_template("index.html")


@app.get("/check")
def handle_form():
    return render_template("check.html", password=request.args.get("password"))
