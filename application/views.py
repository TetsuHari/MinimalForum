from flask import redirect, url_for
from application import app


@app.route("/")
def index():
    return redirect(url_for("threads_index"))
