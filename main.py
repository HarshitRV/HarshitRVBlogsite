from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar

# sqlalchemy is imported for exception handling related to sqlalchemy
import sqlalchemy

# sqlalchemy.orm is required for the crating realtionships between tables
from sqlalchemy.orm import relationship
from post_form import CreatePostForm, CreateLoginForm, CreateRegisterForm, CommentForm
from flask_ckeditor import CKEditor

# imports required for session management
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user

# import required for password hashing
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# creating the wrapper for the admin_only decorator
from functools import wraps

# setting up the app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(
    app, size=100,
    rating='g',
    default='retro',
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None
)

##CONNECT TO DB
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CONFIGURE TABLE USER DB

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    
    # This will act like a List of BlogPost objects attached to each User. 
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")

    # Add parent relationship to Comment class
    # "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")
    
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    
    # Created Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #Create reference to the User object, the "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")
   
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
   

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    # Add child relationship to Comment class
    # "users.id" The users refers to the tablename of the Users class.
    # "comments" refers to the comments property in the User class.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    

# db.create_all()


# admin only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)        
    return decorated_function

@app.route('/')
def home():
    blogs = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=blogs)


@app.route("/post/<int:index>", methods=["GET", "POST"])
def show_post(index):
    form = CommentForm()

    # Get the post from the database
    requested_post = BlogPost.query.get(int(index))

    # Get all the comments for the post
    all_comments = db.session.query(Comment).all()

    # Check if the form was submitted
    if form.validate_on_submit():
        try:
            comment = Comment(text=form.body.data, author_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("show_post", index=index))
        except AttributeError:
            flash("You must be logged in to comment", "danger")
            return redirect(url_for("login"))
    return render_template("post.html", post=requested_post, form=form, comments=all_comments)

@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    today = datetime.datetime.now().date()
    if not current_user.is_authenticated:
        flash("You must be logged in to create a post", "danger")
        return redirect(url_for('login'))
    if form.validate_on_submit():
        new_blog = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=today,

            # author expects the user object to be passed in
            author=current_user,
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


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

@app.route("/edit-post/<int:id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(id):
    to_edit = BlogPost.query.get(id)
    edit_blog = CreatePostForm(
      obj= to_edit 
    )
    if edit_blog.validate_on_submit():
        to_edit.title = edit_blog.title.data
        to_edit.subtitle = edit_blog.subtitle.data
        to_edit.img_url = edit_blog.img_url.data
        to_edit.author = current_user
        to_edit.body = edit_blog.body.data
        db.session.commit()
        
        return redirect(url_for("show_post", index=id))
    return render_template("make-post.html", form=edit_blog, is_edit=True, purpose="Edit Post")

@app.route("/delete-post/<id>")
@login_required
@admin_only
def delete_post(id):
    delete_post = BlogPost.query.get(int(id))
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = CreateLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Password incorrect, please try again.')
                return redirect(url_for('login'))
        except AttributeError:
            flash('No user with that email address exists.')
            return redirect(url_for('register'))

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

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
            flash("Thanks for registering! Login to write, edit comment.")
            return redirect(url_for("login"))
        except sqlalchemy.exc.IntegrityError:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000,debug=True)