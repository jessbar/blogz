from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'learningblog101'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_comment = db.Column(db.Text)

    def __init__(self, post_title, post_comment):
        self.post_title = post_title
        self.post_comment = post_comment

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