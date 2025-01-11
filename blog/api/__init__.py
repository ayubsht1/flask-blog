from flask_restful import Api
from blog.api.post_resources import PostResource
from blog.api.user_resources import UserRegisterResource, UserLoginResource, LogoutResource

def init_api(app):
    api = Api(app)
    
    api.add_resource(UserRegisterResource, '/api/register')
    api.add_resource(UserLoginResource, '/api/login')
    api.add_resource(LogoutResource, '/api/logout')
    api.add_resource(PostResource, '/api/post', '/api/post/<int:post_id>')
