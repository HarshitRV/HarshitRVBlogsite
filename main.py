import re
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from post_form import CreatePostForm, CreateLoginForm, CreateRegisterForm
from flask_ckeditor import CKEditor
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CONFIGURE TABLE BLOG DB
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# CONFIGURE TABLE USER DB

class User(UserMixin, db.Model):
    __tablename__ = "user_db"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000)) 

# db.create_all()
# Getting all posts
posts = db.session.query(BlogPost).all()

@app.route('/')
def home():

    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(int(index))
    return render_template("post.html", post=requested_post)

@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    today = datetime.datetime.now().date()
    if form.validate_on_submit():
        new_blog = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=today,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data
        )
        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("make-post.html", form=form, purpose="Make Post")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit-post/<int:id>", methods=["GET", "POST"])
def edit_post(id):
    to_edit = BlogPost.query.get(id)
    edit_blog = CreatePostForm(
      obj= to_edit 
    )
    if edit_blog.validate_on_submit():
        to_edit.title = edit_blog.title.data
        to_edit.subtitle = edit_blog.subtitle.data
        to_edit.img_url = edit_blog.img_url.data
        to_edit.author = edit_blog.author.data
        to_edit.body = edit_blog.body.data
        db.session.commit()
        
        return redirect(url_for("show_post", index=id))
    return render_template("make-post.html", form=edit_blog, is_edit=True, purpose="Edit Post")

@app.route("/delete-post/<id>")
def delete_post(id):
    delete_post = BlogPost.query.get(int(id))
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = CreateLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateRegisterForm()
    if form.validate_on_submit():
        
        new_user = User(
            name = form.name.data,
            email = form.email.data,
            password = generate_password_hash(
                form.password.data,
                method="pbkdf2:sha256",
                salt_length=8
            )
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("home"))
        except sqlalchemy.exc.IntegrityError:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)