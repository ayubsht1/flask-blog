from flask_restful import Resource
from flask import request, jsonify, url_for
from blog.models import db, Post
from flask_login import current_user

class PostListResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = 5
        
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        next_url = url_for('postlistresource', page=posts.next_num) if posts.has_next else None
        prev_url = url_for('postlistresource', page=posts.prev_num) if posts.has_prev else None

        return jsonify({
            'posts': [{
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'date_posted': post.date_posted
            } for post in posts.items],
            'next_url': next_url,
            'prev_url': prev_url
        })

class PostCreateResource(Resource):
    def post(self):
        data = request.get_json()

        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'message': 'Title and content are required!'}, 400
        
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({
            'message': 'Post created successfully!',
            'post': {
                'id': new_post.id,
                'title': new_post.title,
                'content': new_post.content,
                'date_posted': new_post.date_posted
            }
        }), 201
