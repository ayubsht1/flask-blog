from flask_restful import Api
from blog.api.post_resources import PostListResource, PostCreateResource
from blog.api.user_resources import UserRegisterResource, UserLoginResource

def init_api(app):
    api = Api(app)
    
    api.add_resource(PostListResource, '/api/posts')  # List of posts
    api.add_resource(PostCreateResource, '/api/posts/create')  # Create a new post
    api.add_resource(UserRegisterResource, '/api/register')  # User registration
    api.add_resource(UserLoginResource, '/api/login')  # User login
