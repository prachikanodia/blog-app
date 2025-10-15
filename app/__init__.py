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
    
    app.config["PARAMS"] = _load_params()

    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-fallback")
    upload_dir = app.config["PARAMS"].get("upload_location", "static/assets/img")

    if not os.path.isabs(upload_dir):
        upload_dir = os.path.join(os.getcwd(), upload_dir)
    try:
        os.makedirs(upload_dir, exist_ok=True)
    except Exception:
        upload_dir = "/tmp/uploads"
        os.makedirs(upload_dir, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = upload_dir

    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "False"),
        MAIL_USE_SSL=os.getenv("MAIL_USE_SSL", "True"),
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER") or os.getenv("MAIL_USERNAME"),
        MAIL_SUPPRESS_SEND=os.getenv("MAIL_SUPPRESS_SEND", "False").lower() == "true",
    )

    
    uri = (os.getenv("DATABASE_URL")
           or os.getenv("MYSQL_URL")
           or "mysql+pymysql://root:root@127.0.0.1:8889/CodingThunder")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
    if uri.startswith("mysql://"):
        uri = uri.replace("mysql://", "mysql+pymysql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
    db.init_app(app)
    mail.init_app(app)

    # blueprints
    from .routes.core import bp as core_bp
    from .routes.auth import bp as auth_bp
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)

    
    with app.app_context():
        db.create_all()

    return app
