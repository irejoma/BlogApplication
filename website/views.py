# Import necessary modules
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user  # Import login-related functions
from .models import Post, User, Comment, Like  # Import models for post, user, comment, like
from . import db  # Import the database instance

# Create a Blueprint for the views/routes
views = Blueprint("views", __name__)

# Home route: Displays posts on the home page with pagination and search functionality
@views.route("/", methods=['GET', 'POST'])
@views.route("/home", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def home():
    # Get the current page number and search query from the URL parameters
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')  # If provided, filter posts by username

    # If a search query exists, filter posts based on the username, otherwise show all posts
    if search_query:
        posts = Post.query.join(User).filter(User.username.like(f'%{search_query}%')).order_by(Post.date_created.desc()).paginate(page=page, per_page=5, error_out=False)
    else:
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5, error_out=False)

    return render_template("home.html", posts=posts, user=current_user)  # Render the home page with posts

# Create Post route: Allows users to create a new post
@views.route("/create-post", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def create_post():
    if request.method == "POST":
        text = request.form.get('text')  # Get the text content for the post

        if not text:
            flash('Post cannot be empty', category='error')  # Flash error if the post is empty
        else:
            post = Post(text=text, author=current_user.id)  # Create a new post
            db.session.add(post)  # Add the post to the session
            db.session.commit()  # Commit the transaction to save the post
            flash('Post created!', category='success')  # Flash success message
            return redirect(url_for('views.home'))  # Redirect to the home page

    return render_template('create_post.html', user=current_user)  # Render the create post form

# Delete Post route: Allows users to delete their posts
@views.route("/delete-post/<id>")
@login_required  # Ensure the user is logged in to access this route
def delete_post(id):
    post = Post.query.filter_by(id=id).first()  # Get the post by ID

    if not post:
        flash("Post does not exist.", category='error')  # Flash error if the post is not found
    elif current_user.id != post.author:  # Ensure the user is the post's author
        flash('You do not have permission to delete this post.', category='error')  # Flash error if not authorized
    else:
        db.session.delete(post)  # Delete the post from the database
        db.session.commit()  # Commit the transaction
        flash('Post deleted.', category='success')  # Flash success message

    return redirect(url_for('views.home'))  # Redirect to home page after deletion

# User's posts route: Displays all posts by a specific user
@views.route("/posts/<username>")
@login_required  # Ensure the user is logged in to access this route
def posts(username):
    user = User.query.filter_by(username=username).first()  # Get the user by username

    if not user:
        flash('No user with that username exists.', category='error')  # Flash error if user not found
        return redirect(url_for('views.home'))  # Redirect to home page

    posts = Post.query.filter_by(author=user.id).all()  # Get all posts by the user

    return render_template("posts.html", user=current_user, posts=posts, username=username)  # Render the user's posts page

# Create Comment route: Allows users to comment on posts
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required  # Ensure the user is logged in to access this route
def create_comment(post_id):
    text = request.form.get('text')  # Get the comment text

    if not text:
        flash('Comment cannot be empty.', category='error')  # Flash error if the comment is empty
    else:
        post = Post.query.filter_by(id=post_id).first()  # Get the post by ID
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)  # Create a new comment
            db.session.add(comment)  # Add the comment to the session
            db.session.commit()  # Commit the transaction to save the comment
        else:
            flash('Post does not exist.', category='error')  # Flash error if the post doesn't exist

    return redirect(url_for('views.home'))  # Redirect to home page after creating comment

# Delete Comment route: Allows users to delete their comments
@views.route("/delete-comment/<comment_id>")
@login_required  # Ensure the user is logged in to access this route
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()  # Get the comment by ID

    if not comment:
        flash('Comment does not exist.', category='error')  # Flash error if comment not found
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')  # Flash error if not authorized
    else:
        db.session.delete(comment)  # Delete the comment from the database
        db.session.commit()  # Commit the transaction to delete the comment

    return redirect(url_for('views.home'))  # Redirect to home page after deletion

# Like Post route: Allows users to like or unlike posts
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required  # Ensure the user is logged in to access this route
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()  # Get the post by ID
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()  # Check if the user has already liked the post

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)  # Return error if the post doesn't exist
    elif like:
        db.session.delete(like)  # Unlike the post (delete like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)  # Like the post (create like)
        db.session.add(like)  # Add the like to the session
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})  # Return updated like count and like status

# Edit Post route: Allows users to edit their posts
@views.route("/edit-post/<id>", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def edit_post(id):
    post = Post.query.filter_by(id=id).first()  # Get the post by ID

    if not post:
        flash("Post does not exist.", category='error')  # Flash error if the post doesn't exist
        return redirect(url_for('views.home'))  # Redirect to home page if post not found

    if post.author != current_user.id:
        flash('You do not have permission to edit this post.', category='error')  # Flash error if the user isn't the post's author
        return redirect(url_for('views.home'))  # Redirect to home page if not authorized

    if request.method == 'POST':
        text = request.form.get('text')  # Get the new text for the post

        if not text:
            flash('Post cannot be empty.', category='error')  # Flash error if the post text is empty
        else:
            post.text = text  # Update the post text
            db.session.commit()  # Commit the transaction to save changes
            flash('Post updated!', category='success')  # Flash success message
            return redirect(url_for('views.home'))  # Redirect to home page after updating post

    return render_template('edit_post.html', post=post)  # Render the edit post form with the existing post data
