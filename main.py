from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bloggingisgood@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'learningblog101'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_comment = db.Column(db.Text)

    def __init__(self, post_title, post_comment, owner):
        self.post_title = post_title
        self.post_comment = post_comment
        self.owner = owener

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    post = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['index', 'blog', 'login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/', methods=['POST','GET'])
def redirect_to_blog():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():
    post_id = request.args.get("id")
    if post_id:
        blog = Blog.query.get(post_id)
        return render_template('single_post.html', blog=blog)
    blogs = Blog.query.all()
    return render_template('main_blog.html', blogs=blogs)

@app.route('/add_blog', methods=['POST', 'GET'])
def add_blog():
    title = ""
    comment = ""
    if request.method == "POST":
        title = request.form['new_blog']
        comment = request.form['blog_entry']
        if title and comment:
            post = Blog(title, comment)
            db.session.add(post)
            db.session.commit()
            post_link = "/blog?id=" + str(post.id)
            return redirect(post_link)
    return render_template('add_blog.html', new_blog=title, blog_entry=comment) 

if __name__ == '__main__':
    app.run()