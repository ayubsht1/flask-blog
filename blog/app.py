from flask import Blueprint, render_template, redirect, url_for, request, flash
from blog.models import  Post, User
from flask_login import login_user, login_required, logout_user, current_user
from blog import bcrypt, db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)  # Get the current page from the query string (defaults to page 1)
    per_page = 5  # Set how many posts per page
    
    # Query the posts and paginate them
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Pagination data (total pages, current page, next page, etc.)
    next_url = url_for('main.home', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.home', page=posts.prev_num) if posts.has_prev else None
    
    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url)

@main.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title or not content:
            flash('Title and Content are required!', 'danger')
            return redirect(url_for('main.create_post'))
        
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html')

@main.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@main.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure that the post belongs to the logged-in user
    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        if not post.title or not post.content:
            flash('Title and Content are required!', 'danger')
            return redirect(url_for('main.update_post', post_id=post.id))

        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.post_detail', post_id=post.id))  # Redirect to the post detail page

    return render_template('update_post.html', post=post)


@main.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main.home'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))

        flash('Login failed. Check your email and password', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))