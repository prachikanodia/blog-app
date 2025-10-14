import os, json
from dotenv import load_dotenv
from flask import Flask
from .extensions import db, mail

def as_bool(v, default=False):
    if v is None:
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}

def _load_params():
    with open('config.json', 'r') as c:
        return (json.load(c) or {}).get("params", {})

def create_app():
    load_dotenv()

    app = Flask(__name__)
    # --- config.json (non-secrets) ---
    app.config["PARAMS"] = _load_params()

    # --- secrets/env ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-fallback")
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER",    app.config["PARAMS"].get("upload_location", "static/uploads"),
)


    app.config["MAIL_SERVER"]   = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"]     = int(os.getenv("MAIL_PORT", "465"))
    app.config["MAIL_USE_SSL"]  = as_bool(os.getenv("MAIL_USE_SSL"), True)
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    LOCAL_SERVER = as_bool(os.getenv("LOCAL_SERVER"), True)
    local_uri = os.getenv("LOCAL_DB_URI")
    prod_uri  = os.getenv("PROD_DB_URI")
    app.config["SQLALCHEMY_DATABASE_URI"] = local_uri if LOCAL_SERVER else prod_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # init extensions
    db.init_app(app)
    mail.init_app(app)

    # blueprints
    from .routes.core import bp as core_bp
    from .routes.auth import bp as auth_bp
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)

    # create tables once
    with app.app_context():
        db.create_all()

    return app