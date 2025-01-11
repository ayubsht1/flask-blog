from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from blog import db
from blog.models import Post


class PostResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post or post.user_id != current_user.id:
                return {'message': 'Post not found or unauthorized'}, 404
            return {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
                'user_id': post.user_id
            }, 200
        else:
            posts = Post.query.all()  # Fetch all posts
            if not posts:
                return {'message': 'No posts found'}, 404
            return [
                {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'date_posted': post.date_posted.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
                    'user_id': post.user_id
                } for post in posts
            ], 200

    @login_required
    def post(self):
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('title') or not data.get('content'):
            return {'message': 'Title and content are required'}, 400
        
        # Create a new post
        new_post = Post(
            title=data['title'],
            content=data['content'],
            user_id=current_user.id
        )
        
        # Add the post to the database
        db.session.add(new_post)
        db.session.commit()
        
        return {'message': 'Post created successfully', 'post_id': new_post.id}, 201

    @login_required
    def put(self, post_id):
        # Fetch post by ID
        post = Post.query.get(post_id)
        
        if not post or post.user_id != current_user.id:
            return {'message': 'Post not found or unauthorized'}, 404
        
        # Update post fields
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        
        # Commit changes to the database
        db.session.commit()
        
        return {'message': 'Post updated successfully'}, 200

    @login_required
    def delete(self, post_id):
        # Fetch post by ID
        post = Post.query.get(post_id)
        
        if not post or post.user_id != current_user.id:
            return {'message': 'Post not found or unauthorized'}, 404
        
        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()
        
        return {'message': 'Post deleted successfully'}, 200
