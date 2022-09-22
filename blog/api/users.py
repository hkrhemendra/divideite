from crypt import methods
import json
from blog.utils.utils import parse_json

from urllib import request

from flask import Blueprint
from flask import jsonify
from flask import request

from blog.models import mongo
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from blog.config.flask_bcrypt import bcrypt

users = Blueprint('users',__name__)


database = mongo.dividiete.users

@users.route('/')
def index():
    try: 
        db = database.find_one_or_404({"name": "test"})
        print("type ------------------------->",parse_json(db))
        return jsonify({"status": 200, "data": parse_json(db)}),400
    except Exception as error:
        print(error)
        return jsonify({"status": 0, "message":"name not found"}),409

@users.route('/sign-up', methods = ["POST"])
def signUp():
    try: 
        if request.method == "POST":
            data = request.json
            name = data["name"]
            username = data["username"]
            phone = data["phone"]
            email = data["email"]
            role = data["role"]
            password = data["password"]

            pw_hash = bcrypt.generate_password_hash(password)

            if not database.find_one({"username":username}):
                database.insert_one({
                    "name": name,
                    "username": username,
                    "phone": phone,
                    "email": email,
                    "role": role,
                    "password": pw_hash
                })
                return jsonify({"status": 200,"message": "user added successfully"}),200
            else: 
                return jsonify({"status": 400, "message": "username already in use, please try with other username"}),400
    except Exception as error:
            print(error)
            return jsonify({"message": "some error occured"}),500



    

@users.route('/login', methods=["POST"])
def login():
    try:
        if request.method == "POST":
            data = request.json
            print("data =======>", data)
            username = data['username']
            password = data['password']
            
            user = database.find_one({"username": username})
            if not user:
                return jsonify({"message": "Username not exist. Try again"}),400
            else:
                if bcrypt.check_password_hash(user["password"], password):
                    additional_claims = {"role": user['role']}
                    access_token = create_access_token(identity=username,additional_claims=additional_claims)
                    return jsonify({"status": 200, "accessToken": access_token})
                else:
                    return jsonify({"message": "Wrong password", "status": 401})
    except Exception as error:
        print("Error ---------------->",error)
        return jsonify({"status": 0, "message":"unable to login user" }),409

@users.route('/get-user-role', methods=['GET'])
@jwt_required()
def get_role():
    role = get_jwt()
    return jsonify({"status": 200, "role": role['role']})



