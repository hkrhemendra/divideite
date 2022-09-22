from flask import Flask

from blog.models import mongo
from blog.api.users import users
from blog.config.flask_bcrypt import bcrypt
from blog.api.blogs import blog
from blog.config.flask_jwt_extended import jwt
from blog.config.flask_cors import cors
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    app.config['SECRET_KEY'] = "dGhpc2lzbXlzZWNyZXQK"
    app.config['JWT_SECRET_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    # app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config['MONGO_URI'] = "mongodb+srv://hemen123:hemendra@cluster0.rebp1if.mongodb.net/?retryWrites=true&w=majority"
    CORS(app)
    cors = CORS(app,support_credentials=True ,resources={
        r"/*":{
             "origins": "http://localhost:4200", "allow_headers": "*", "expose_headers": "*"
        }
    })
    app.register_blueprint(users)
    app.register_blueprint(blog)
    
    with app.app_context():
        bcrypt.init_app(app)
        jwt.init_app(app)
        cors.init_app(app)

    return app