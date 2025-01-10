from blog import create_app
from blog.api import init_api

app = create_app()
init_api(app)

if __name__ == '__main__':
    app.run(debug=True)