from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password 

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect("/newpost")
        else:
            flash('User password incorrect, or user does not exsist', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if username == "" or password == "" or verify == "":
            flash("One or more fields has been left blank.")
            return redirect("/signup")
        if password != verify:
            flash("Passwords do not match")
            return redirect('/signup')
        if len(username) < 3 or len(password) < 3:
            flash("Please provide a username or password longer than 3 characters.")
            return redirect('/signup')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect("/newpost")
        else:
            flash("Username already taken, please provide a diffferent one.")
            return redirect('/signup')
    
    return render_template("signup.html")

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

     blogs = Blog.query.all()

     blog_id = request.args.get('id')
     owner = request.args.get('user')
     if blog_id != None:
        blog = Blog.query.get(blog_id)
      
        return render_template('case_one.html', 
        blog=blog)

     elif owner != None:
        user = User.query.filter_by(username=owner).first()
       
        user_blog = Blog.query.filter_by(owner_id=user.id)
        
        
        return render_template('singleUser.html', user=user, user_blog=user_blog)

     else:
        return render_template('blog.html',title="Build A Blog", 
        blogs=blogs)


     

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        
        blog_title = request.form['title']
        blog_body = request.form['body']
       
       
        if blog_title == "" or blog_body == "": 
            flash("Please provide a blog title and blog content.")
            return redirect('/newpost')
    
    
        else:
            new_blog = Blog(blog_title, blog_body, owner)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id 
            return render_template('case_two.html', new_blog=new_blog,
        blog_id=blog_id, owner=owner)



    return render_template('newpost.html')



@app.route('/', methods=['POST', 'GET'])
def index(): 

    users = User.query.all()

    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()