from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm, ModifyUserForm


@app.route("/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data,
                                password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form,
                               error="No such username or password")

    login_user(user)
    return redirect(url_for("index"))


@app.route("/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form=RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        print(form.errors)
        print("NOT VALIDATED")
        return render_template("auth/registerform.html", form=form)

    new_user = User(form.username.data, form.password.data)
    db.session().add(new_user)
    db.session().commit()
    login_user(new_user)
    return redirect(url_for("index"))


@app.route("/user/<uname>", methods=["GET"])
def auth_userpage(uname):
    user = User.query.filter_by(username=uname).first()
    if not user:
        return render_template("auth/user_not_found.html")

    # TODO get data about user, eg how many comments has posted

    is_current_user = False
    if hasattr(current_user, 'username'):
        is_current_user = user.username == current_user.username

    return render_template("auth/userpage.html",
                           user=user,
                           is_current_user=is_current_user,
                           form=ModifyUserForm())


@app.route("/user/<uname>", methods=["POST"])
@login_required
def auth_modify_user(uname):
    if uname != current_user.username:
        render_template("auth/access_denied.html")

    form = ModifyUserForm(request.form)

    if not form.validate():
        return render_template("auth/userpage.html",
                               user=current_user,
                               is_current_user=True,
                               form=form)

    user = User.query.get(current_user.id)
    if len(form.new_username.data) > 0:
        user.username = form.new_username.data

    if len(form.new_password.data) > 0:
        user.password = form.new_password.data

    if form.delete_user.data:
        db.session.delete(user)

    db.session.commit()
    return redirect(url_for("index"))
