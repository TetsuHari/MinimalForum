from application import app, database
from flask import render_template, request, url_for, redirect
from application.threads.models import Thread
from application.threads.forms import ThreadForm

@app.route("/threads/new")
def new_thread_form():
    return render_template("threads/new.html", form = ThreadForm())

@app.route("/threads/", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads = Thread.query.all())

@app.route("/threads/", methods=["POST"])
def create_thread():
    form = ThreadForm(request.form)

    if not form.validate():
        return render_template("threads/new.html", form = form)

    thread = Thread(form.title.data, form.content.data)
    database.session().add(thread)
    database.session().commit()

    return redirect(url_for("threads_index"))

@app.route("/threads/lock/<thread_id>/", methods=["POST"])
def lock_thread(thread_id):
    thread = Thread.query.get(thread_id)
    thread.locked = True
    database.session.commit()

    return redirect(url_for("threads_index"))
