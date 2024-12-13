import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, PostForm
from models import db, User, Post

# Initialize the Flask application
app = Flask(__name__)

# Load configurations from environment variables
app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Use a secure key loaded from the .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Use the database URL from the .env file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for better performance

# Initialize the database
db.init_app(app)

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Route: Homepage
@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)

# Route: User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Route: User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

# Route: User logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Route: Create a new post
@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if 'user_id' not in session:
        flash('You need to log in to create a post.', 'danger')
        return redirect(url_for('login'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=session['user_id'])
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('new_post.html', form=form)

# Entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
