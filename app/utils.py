import re
from functools import wraps
from flask import session, redirect, url_for, request

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,80}$")

#so tht no person can use the protected url by just typing it in google or whatever.. (can use JWT for external apis returning json values)
def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login", next=request.url))
        return view(*args, **kwargs)
    return wrapper

def validate_signup(username, password):
    errors = {}
    username = username
    password = password
    if not USERNAME_RE.match(username):
        errors["urusername"] = "Username must be alphanumeric, and not more than 80 words."
    if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        errors["userpass"] = "Minimum 8 characters, include letters & a number."
    return username, password, errors

def validate_login(username, password):
    errors = {}
    username = username
    password = password
    if not username: errors["uname"] = "Username required."
    if not password: errors["pass"]  = "Password required."
    return username, password, errors
