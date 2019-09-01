from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
import mistune

from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.comment.models import Comment
from application.comment.forms import CommentForm


@app.route("/threads/new")
@login_required
def new_thread_form():
    return render_template("threads/new.html", form=ThreadForm())


@app.route("/threads/", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads=Thread.query.all())


@app.route("/threads/", methods=["POST"])
@login_required
def create_thread():
    form = ThreadForm(request.form)
    if not form.validate():
        return render_template("threads/new.html", form=form)

    thread = Thread(form.title.data, form.content.data, current_user.id)
    db.session().add(thread)
    db.session().commit()

    return redirect(url_for("threads_index"))


@app.route("/threads/lock/<thread_id>/", methods=["POST"])
@login_required
def lock_thread(thread_id):
    thread = Thread.query.get(thread_id)
    thread.locked = not thread.locked
    db.session.commit()

    return redirect(url_for("thread", thread_id=thread_id))


@app.route("/threads/<thread_id>/", methods=["GET"])
def thread(thread_id, comment_form=None):
    thread = Thread.query.get(thread_id)
    if comment_form is None:
        comment_form = CommentForm()
    if thread:
        is_owner = False
        if hasattr(current_user, 'id'):
            is_owner = current_user.id == thread.author.id
        thread_comms = thread.thread_comments
        comment_html = map(render_comment, thread_comms)
        return render_template("threads/thread.html", thread=thread,
                               content=mistune.markdown(thread.content),
                               comments=comment_html,
                               form=comment_form,
                               owner=is_owner)

    return render_template("threads/not_found.html")

# render_comment :: Comment -> HTML


def render_comment(comment):
    comments = comment.comments
    comments_html = map(render_comment, comments)
    return render_template("/comment/comment.html", comment=comment,
                           content=mistune.markdown(comment.content),
                           comments=comments_html)


@app.route("/threads/<thread_id>/c", methods=["POST"])
@login_required
def comment_to_thread(thread_id):
    form = CommentForm(request.form)
    thread = Thread.query.get(thread_id)
    if thread:
        if form.validate():
            comment = Comment(form.content.data, current_user, thread)
            thread.thread_comments.append(comment)
            db.session.commit()
            return redirect(url_for("thread", thread_id=thread_id))
        else:
            return redirect(url_for("thread", thread_id=thread_id,
                                    comment_form=form))

    return render_template("threads/not_found.html")
