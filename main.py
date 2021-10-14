from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from post_form import CreatePostForm
from flask_ckeditor import CKEditor
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


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

if __name__ == "__main__":
    app.run(debug=True)