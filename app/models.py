from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class Posts(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=True, server_default=func.current_timestamp())
    tagline = db.Column(db.String(160), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    postcomment=db.relationship('Comments', backref='postc')


class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_pass=db.Column(db.String(280), nullable=False)
    #one user having many posts
    posts = db.relationship('Posts', backref="poster")
    postcommentuser=db.relationship('Comments', backref='postcu')

    def set_password(self, raw_password):
        self.user_pass = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.user_pass, raw_password)

class Comments(db.Model):
    __tablename__ = 'Comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=True, server_default=func.current_timestamp())
    postpost_id = db.Column(db.Integer, db.ForeignKey('posts.sno'), nullable=False)
    postuser_id=db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
