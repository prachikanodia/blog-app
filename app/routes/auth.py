from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from ..extensions import db
from ..models import Users, Posts
from ..utils import validate_signup, validate_login, login_required

bp = Blueprint("auth", __name__)

@bp.route("/signup", methods=['GET','POST'])
def signup():
    params = current_app.config.get("PARAMS", {})
    uid = session.get('user_id')
    if uid:
        return redirect('/')
    if request.method=='POST':
        username, password, errors = validate_signup(
            request.form.get('urusername'),
            request.form.get('userpass')
        )
        if errors:
            flash("Please fix the highlighted fields.", "danger")
            return render_template("signup.html", params=params, errors=errors,form={"urusername": username}),400
        u=Users(user_name=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect('/login')
    return render_template("signup.html", params=params)

@bp.route("/login", methods=['GET','POST'])
def login():
    params = current_app.config.get("PARAMS", {})
    uid=session.get('user_id')
    if uid:
        return redirect('/')
    if request.method=='POST':
        username, password, errors = validate_login(
            request.form.get("uname"),
            request.form.get("pass")
        )
        if errors:
            flash("Please fill in both fields properly.", "danger")
            return render_template("login.html", params=params, errors=errors,
                                   form={"uname": username}), 400
        u = Users.query.filter_by(user_name=username).first()
        if not u or not u.check_password(password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html", params=params,form={"uname": username})
        session.clear()
        session["user_id"] = u.user_id
        flash("Welcome to your dashboard!", "success")
        return redirect('/dashboard')
    return render_template('login.html', params=params)

@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    params = current_app.config.get("PARAMS", {})
    uid=session.get('user_id')
    u=Users.query.get(uid)#user_id being the primary key
    posts = Posts.query.filter_by(poster_id=uid).all()
    return render_template("dashboard.html", params=params, posts=posts, users=u)

@bp.route("/logout")
def logout():
    session.pop('user_id')
    return redirect('/')

