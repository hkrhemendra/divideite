from ast import parse
from crypt import methods
from email import header
import json
from operator import imod
from urllib import request

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response

from blog.models import mongo
from blog.utils.utils import parse_json, data_length

from datetime import datetime

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

from flask_cors import cross_origin

blog = Blueprint('blog',__name__, url_prefix='/blog')

blog_data = mongo.dividiete.blog

# @blog.after_request
# def after_request_func(response):
#     origin = request.headers.get('Origin')
#     if request.method == 'OPTIONS':
#         response = make_response()
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
#         response.headers.add('Access-Control-Allow-Methods',
#                             'GET, POST, OPTIONS, PUT, PATCH, DELETE')
#         if origin:
#             response.headers.add('Access-Control-Allow-Origin', origin)
#     else:
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         if origin:
#             response.headers.add('Access-Control-Allow-Origin', origin)

#     return response
    ### end CORS section

@blog.route('/', methods = ['GET'], strict_slashes = False)
@cross_origin(supports_credentials=True)
def list_blog():
    if request.method == 'GET':
        try:
            blogs = []
            for single_blog in blog_data.find().sort("date", -1):
                single_blog["_id"] = str(single_blog["_id"])
                blogs.append(single_blog)
            len(blogs)
            print("count ----------------> ", len(blogs))
            return jsonify({'status': 200, "data":blogs})
        except Exception as error:
            print(error)
            return jsonify({'status': 400, "message": "Something went wrong"})


@blog.route('/upload',methods = ["POST"])
@jwt_required()
def upload_blog():
    if request.method == "POST":
        try:
            data = request.json
            date = datetime.now()
            title = data['title']
            intro = data['intro']
            banner = data['banner']
            image1 = data['image1']
            image2 = data['image2']
            subheading1 = data['subheading1']
            para1 = data['para1']
            subheading2 = data['subheading2']
            para2 = data['para2']
            conclusion = data['conclusion']
            status = 0
            created_by = get_jwt_identity()

            if not blog_data.find_one({'title':title}):

                new_id = data_length(blog_data.find().sort("id",-1)) + 1
                

                blog_data.insert_one({
                    'id': new_id,
                    'date': date,
                    'title': title,
                    'intro': intro,
                    'banner': banner,
                    'image1': image1,
                    'image2': image2,
                    'subheading1': subheading1,
                    'para1': para1,
                    'para2': para2,
                    'subheading2': subheading2,
                    'conclusion': conclusion,
                    "status": status,
                    "created_by": created_by
                })

                return jsonify({'status': 200, 'message': 'Blog has been uploaded successfully'})
            else:
                return jsonify({'status': 400, 'message': 'Title already in user, please use differnt title'})
        
        except Exception as error:
            print("Error --------------------->",error)
            return jsonify({'status': 500, 'message': 'Something went wrong'})


@blog.route('/single-blog/<id>',methods=['GET'], strict_slashes = False)
def single_blog(id):
    if request.method == 'GET':
        try:
            data = blog_data.find_one_or_404({
                'id': int(id)
            })
            print("single data ==========> ", data)
            return jsonify({"status": 200, "data": parse_json(data)})
        except Exception as error:
            print(error)
            return jsonify({'status': 500, 'message': 'something went wrong'})
    else:
        return jsonify({"status": 404, "message": "No POST method."})

@blog.route('/update-blog/<id>', methods=['PATCH'])
@jwt_required()
def update_form(id):
    if request.method == 'PATCH':
        try:
            data = request.json
            title = data['title']
            intro = data['intro']
            subheading1 = data['subheading1']
            para1 = data['para1']
            subheading2 = data['subheading2']
            para2 = data['para2']
            conclusion = data['conclusion']
            print("ID -------> ", title)

            new_values =  {"$set": { 'title': title } }

            print(type(new_values))

            data = blog_data.update_one({ 'id': int(id)}, {"$set": { 'title': title, 'intro': intro, 'subheading1': subheading1, 'subheading2': subheading2, 'para1': para1, 'para2': para2, 'conclusion': conclusion } })

            return jsonify({'status': 200, "message": "data updated successfully ", "updateData":"success"})
        except Exception as error: 
            print(error)
            return jsonify({"status": 500, "message": "Something wend wrong"})

@blog.route('/delete/<id>', methods = ['DELETE'])
@jwt_required()
def delete_blog(id):
    if request.method == 'DELETE':
        try:
            role = get_jwt()
            if role["role"] == "super_admin":
                data = blog_data.find_one_and_delete({
                    'id': int(id)
                })
                print("deleted result ========> ", data)
                return jsonify({'status': 200, "message": "data deleted successfully ", "deletedData":data})
            else:
                return jsonify({'status': 401,"message": "admin access required to delete data"})
        
        except Exception as error:
            print(error)
            return jsonify({"status": 500, "message": "Something wend wrong"})
        


@blog.route('/activate/<id>', methods = ['GET'])
@jwt_required()
def activate_blog(id):
    if request.method == 'GET':
        try:
            
            role = get_jwt()
            if role['role'] == "admin" or role['role'] == "super_admin":
                blog_data.update_one(
                    {'id':int(id)},
                    {"$set": {"status":1}}
                )
                data = blog_data.find_one({
                    "id": int(id)
                })
                return jsonify({"status":200,"message": "data updated successfully" ,"data": parse_json(data)})
            else:
                return jsonify({"status": 401,"message": "Admin Access Required"})
        except Exception as error:
            print(error)
            return jsonify({"status": 500, "message": "Something went wrong"})