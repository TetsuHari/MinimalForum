from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.comment.models import Comment

@app.route("/threads/new")
@login_required
def new_thread_form():
    return render_template("threads/new.html", form = ThreadForm())

@app.route("/threads/", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads = Thread.query.all())

@app.route("/threads/", methods=["POST"])
@login_required
def create_thread():
    form = ThreadForm(request.form)
    if not form.validate():
        return render_template("threads/new.html", form = form)

    thread = Thread(form.title.data, form.content.data, current_user.id)
    db.session().add(thread)
    db.session().commit()

    return redirect(url_for("threads_index"))

@app.route("/threads/lock/<thread_id>/", methods=["POST"])
@login_required
def lock_thread(thread_id):
    thread = Thread.query.get(thread_id)
    thread.locked = True
    db.session.commit()

    return redirect(url_for("threads_index"))
