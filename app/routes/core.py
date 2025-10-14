import math, os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, current_app, session
from werkzeug.utils import secure_filename
from flask_mail import Message
from ..extensions import db, mail
from ..models import Posts, Users, Comments, Contacts
from ..utils import login_required

bp = Blueprint("core", __name__)

@bp.route("/")
def home():
    params = current_app.config.get("PARAMS", {})
    posts = Posts.query.filter_by().all()
    last=math.ceil(len(posts)/int(params['no_of_posts']))
    page=request.args.get('page')
    if(not str(page).isnumeric()):
        page=1
    page=int(page)
    posts=posts[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+int(params['no_of_posts'])]
    if (page==1):
        prev="#"
        next="/?page="+str(page+1)
    elif(page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)
    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)

@bp.route("/about")
def about():
    params = current_app.config.get("PARAMS", {})
    return render_template('about.html', params=params)

@bp.route('/add')
def add_data():
    user1 = Users(user_name="Prachi")
    user1.set_password("Gishin")
    db.session.add(user1)
    db.session.commit()
    post1 = Posts(title="My firstest blog", content="Hello Flask!", slug="idkwhattheheck", tagline="something", poster_id=user1.user_id)
    db.session.add(post1)
    db.session.commit()
    comment1=Comments(comment="Nice!", date=datetime.now(), postuser_id=user1.user_id, postpost_id=post1.sno)
    db.session.add(comment1)
    db.session.commit()
    return "Data added successfully!"

@bp.route("/edit/<string:sno>", methods=['GET', 'POST'])
@login_required
def edit(sno):
    params = current_app.config.get("PARAMS", {})
    uid=session.get('user_id')
    if request.method=='POST':
        box_title=request.form.get('title')
        tline=request.form.get('tline')
        slug=request.form.get('slug')
        content=request.form.get('content')
        img_file=request.form.get('img_file')
        date = datetime.now()
        poster_id= uid

        if sno=='0':
            post=Posts(title=box_title,slug=slug,content=content,tagline=tline,img_file=img_file, date=date, poster_id=poster_id)
            db.session.add(post)
            db.session.commit()
        else:
            post=Posts.query.filter_by(sno=sno).first()
            if not post:
                return "Not found", 404
            if post.poster_id != uid:
                return "Forbidden", 403

            post.title=box_title
            post.slug=slug
            post.content=content
            post.tagline=tline
            post.img_file=img_file
            post.date=date
            post.poster_id=poster_id
            db.session.commit()
        return redirect('/edit/'+sno)
    post=Posts.query.filter_by(sno=sno).first()
    if post and post.poster_id != session.get('user_id'):
        return "Forbidden", 403
    u = Users.query.get(session.get('user_id'))
    return render_template('edit.html', params=params, post=post, users=u)

@bp.route("/uploader", methods=['POST'])
@login_required
def uploader():
    if request.method=='POST':
        f=request.files['file1']
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return "Uploaded successfully"

@bp.route("/delete/<string:sno>", methods=['GET','POST'])
@login_required
def delete(sno):
    uid=session.get('user_id')
    post=Posts.query.filter_by(sno=sno).first()#we want post not a list of posts
    if not post:
        return "Not found", 404
    if post.poster_id != uid:
        return "Forbidden", 403
    db.session.delete(post)
    db.session.commit()
    return redirect('/dashboard')

@bp.route("/contact", methods=['GET','POST'])
def contact():
    params = current_app.config.get("PARAMS", {})
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        # take entry and put in database
        entry = Contacts(name=name, email=email, phone_num=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('new message from blog',
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=message+"\n"+phone
                          )
        flash("Thank you for your valuable feedback!","success")


    return render_template('contact.html', params=params)

@bp.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    params = current_app.config.get("PARAMS", {})
    post = Posts.query.filter_by(slug=post_slug).first()
    comments=Comments.query.filter_by(postpost_id=post.sno)
    user_id = session.get("user_id")
    return render_template('post.html', params=params, post=post , comments=comments, user_id=user_id)

@bp.route("/post/<string:post_slug>/comment", methods=['POST'])
@login_required
def comment(post_slug):
    params = current_app.config.get("PARAMS", {})
    uid=session.get('user_id')
    if not uid:
        return "you are not logged in"
    post = Posts.query.filter_by(slug=post_slug).first()
    comments=request.form.get('comment')
    c=Comments(comment=comments,postpost_id=post.sno,postuser_id=uid)
    db.session.add(c)
    db.session.commit()
    comments = Comments.query.filter_by(postpost_id=post.sno)
    return render_template('post.html', params=params, post=post, comments=comments)