from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '7h1sh@sb33n7h3h@rd3s7p@r7'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/blogs?id={0}'.format(blog.id))
        else:
            flash('User/password incorrect or user does not exist', 'error')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        error = ''
        

        if len(email) < 3 or len(email) > 20 or " " in email or email == "":
            error = "Your entry must be between 3 and 20 characters and contain no spaces. Required field."
        if len(password) < 3 or len(password) > 20 or " " in password or password == "":
            error = "Your entry must be between 3 and 20 characters and contain no spaces. Required field."
        if len(verify) < 3 or len(verify) > 20 or " " in verify or verify == "":
            error = "Your entry must be between 3 and 20 characters and contain no spaces. Required field."
            
        if email:
            if "." not in email and "@" not in email:
                error = "Please check and re-submit. Please do not use spaces."

        if password != verify:
            error = "Password and Verify Password fields must match."

        if not error:
            email = request.form['email']
            session['email'] = email
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('blogs.html', email=email)
            
        else:
            return render_template('register.html', email=email, password='', verify='',  error = error)

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:            
            return redirect('/blogs')
        else:
            return "<h1>User already exists.</h1>"

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

@app.route('/blogs', methods=['POST', 'GET'])
def index():   
    owner = User.query.filter_by(email=session['email']).first()
    blogid = request.args.get('id')
    if request.method == 'POST':
        blog = request.form['name', 'body']
        new_blog = Blog(blog, owner)
        db.session.add(new_blog)
        db.session.commit()
        if blogid:
            blogid = int(blogid)
            blogs = Blog.query.get(blogid)
            return render_template('ind_post.html', blogs=blogs)

    blogs = Blog.query.filter_by(owner=owner).all()
    return render_template('blogs.html',title="My Blogs", 
        blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    owner = User.query.filter_by(email=session['email']).first()
    name = ""
    body = ""
    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']
        error = False
        if not name:
            flash("Blog must have a Title!", 'error')
            error = True
        if not body:
            flash("Blog must have a Body!", 'error')
            error = True
        if not error:
            blog = Blog(name,body,owner)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blogs?id={0}'.format(blog.id))
    blogs = Blog.query.filter_by(owner=owner).all()
    return render_template('newpost.html',title="New Post", 
        blogs=blogs)

if __name__ == '__main__':
    app.run()