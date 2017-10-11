from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def blog():

     blogs = Blog.query.all()

     blog_id = request.args.get('id')
     if blog_id != None:
        blog = Blog.query.get(blog_id)
        return render_template('case_one.html', 
        blog=blog)
     else:
        return render_template('blog.html',title="Build A Blog", 
        blogs=blogs)


     

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        
        blog_title = request.form['title']
        blog_body = request.form['body']

      
        
        if blog_title == "" or blog_body == "": 
            return redirect('/newpost?blog_error=Please provide a blog title and blog content.')
    
    
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id 
            return render_template('case_two.html', new_blog=new_blog,
        blog_id=blog_id)


    error = {'blog_error': ""}

    blog_error = request.args.get("blog_error")
    if blog_error:
        error_esc = cgi.escape(blog_error, quote=True)
        error['blog_error'] =  error_esc 



   


    return render_template('newpost.html', error=error)

   






if __name__ == '__main__':
    app.run()