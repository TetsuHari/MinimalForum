from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
import mistune

from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.comment.models import Comment, Upvote
from application.comment.forms import CommentForm


def check_owner(authored, current_user):
    is_owner = False
    if hasattr(current_user, 'id'):
        is_owner = current_user.id == authored.author.id
    return is_owner


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
    if thread:
        is_owner = check_owner(thread, current_user)
        if not is_owner:
            return render_template("threads/unauthorized.html")
        thread.locked = not thread.locked
        db.session.commit()
        return redirect(url_for("thread", thread_id=thread_id))
    return render_template("threads/not_found.html")


@app.route("/threads/<thread_id>/", methods=["GET", "POST"])
def thread(thread_id):
    thread = Thread.query.get(thread_id)
    if thread:
        if request.method == "POST":
            comment_form = CommentForm(request.form)
            if comment_form.validate():
                comment = Comment(comment_form.content.data,
                                  current_user, thread)
                thread.thread_comments.append(comment)
                db.session.commit()
                return redirect(url_for("thread", thread_id=thread_id))
        else:
            comment_form = CommentForm()

        is_owner = check_owner(thread, current_user)
        thread_comms = thread.thread_comments
        comment_html = map(render_comment, thread_comms)
        return render_template("threads/thread.html", thread=thread,
                               content=mistune.markdown(thread.content),
                               comments=comment_html,
                               comment_form=comment_form,
                               owner=is_owner)

    return render_template("threads/not_found.html")


def allowed_to_vote(user, comment, upvote):
    if user.is_authenticated:
        if upvote:
            for vote in comment.upvotes:
                if vote.is_up and vote.author_id == user.id:
                    return False
            return True
        else:
            for vote in comment.upvotes:
                if (not vote.is_up) and (vote.author_id == user.id):
                    return False
            return True
    else:
        return False


def get_votes(comment):
    total_votes = 0
    for vote in comment.upvotes:
        if vote.is_up:
            total_votes += 1
        else:
            total_votes -= 1
    return total_votes


def render_comment(comment):
    comment_thread = Thread.query.get(comment.thread_id)
    is_authored_to_modify = check_owner(comment, current_user)
    is_authored_to_delete = is_authored_to_modify
    if comment_thread:
        is_authored_to_delete = check_owner(
            comment_thread, current_user) or is_authored_to_modify
    can_upvote = False
    can_downvote = False
    if current_user.is_authenticated:
        can_upvote = allowed_to_vote(current_user, comment, True)
        can_downvote = allowed_to_vote(current_user, comment, False)

    upvotes = get_votes(comment)
    return render_template("/comment/comment.html", comment=comment,
                           content=mistune.markdown(comment.content),
                           modify=is_authored_to_modify,
                           delete=is_authored_to_delete,
                           can_upvote=can_upvote,
                           can_downvote=can_downvote,
                           upvotes=upvotes)


@app.route("/threads/<thread_id>/m", methods=["GET", "POST"])
@login_required
def modify_thread(thread_id):
    form = ThreadForm()
    thread = Thread.query.get(thread_id)
    if thread:
        is_owner = check_owner(thread, current_user)
        if not is_owner:
            return render_template("threads/unauthorized.html")
        if request.method == "GET":
            form.title.data = thread.title
            form.content.data = thread.content
            return render_template("threads/new.html", form=form,
                                   thread_id=thread_id)

        form = ThreadForm(request.form)
        if form.validate():
            thread.content = form.content.data
            thread.title = form.title.data
            db.session.commit()
            return redirect(url_for("thread", thread_id=thread_id))
        return render_template("threads/new.html", form=form,
                               thread_id=thread_id)
    return render_template("threads/not_found.html")


@app.route("/comments/<comment_id>/m", methods=["GET", "POST"])
@login_required
def modify_comment(comment_id):
    form = CommentForm()
    comment = Comment.query.get(comment_id)
    if comment:
        is_owner = check_owner(comment, current_user)
        if not is_owner:
            return render_template("threads/unauthorized.html")
        if request.method == "GET":
            form.content.data = comment.content
            return render_template("comment/modify.html", comment_form=form,
                                   comment_id=comment_id)

        form = CommentForm(request.form)
        if form.validate():
            comment.content = form.content.data
            db.session.commit()
            return redirect(url_for("thread", thread_id=comment.thread_id))
        return render_template("comment/modify.html", comment_form=form,
                               comment_id=comment_id)
    return render_template("threads/not_found.html")


@app.route("/threads/delete/<thread_id>", methods=["POST"])
@login_required
def delete_thread(thread_id):
    thread = Thread.query.get(thread_id)
    if thread:
        is_owner = check_owner(thread, current_user)
        if not is_owner:
            return render_template("threads/unauthorized.html")
        for comment in thread.thread_comments:
            db.session.delete(comment)
        db.session.delete(thread)
        db.session.commit()
        return redirect(url_for("threads_index"))
    return render_template("threads/not_found.html")


@app.route("/comments/delete/<comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        thread = Thread.query.get(comment.thread_id)
        can_delete = check_owner(comment, current_user)
        if thread:
            can_delete = can_delete or check_owner(thread, current_user)
        if not can_delete:
            return render_template("threads/unauthorized.html")
        db.session.delete(comment)
        db.session.commit()
        if thread:
            return redirect(url_for("thread", thread_id=thread.id))
        else:
            return redirect(url_for("threads_index"))


@app.route("/comments/vote/<comment_id>/<is_up>", methods=["POST"])
@login_required
def vote_comment(comment_id, is_up):
    if is_up == 'True':
        is_upvote = True
    else:
        is_upvote = False
    comment = Comment.query.get(comment_id)
    if comment:
        can_vote = allowed_to_vote(current_user, comment, is_upvote)
        if can_vote:
            vote = Upvote.query.filter_by(author_id=current_user.id,
                                          comment_id=comment_id).first()
            if vote:
                vote.is_up = is_upvote
            else:
                vote = Upvote(current_user, comment, is_upvote)
                db.session.add(vote)
            db.session.commit()
        return redirect(url_for("thread", thread_id=comment.thread_id))

    return render_template("threads/not_found.html")
