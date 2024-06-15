from applications.user_datastore import user_datastore
from flask_restful import Resource
from flask import make_response, jsonify, request



class Login(Resource):
    def post(self):
        recieved_data = request.get_json()

        email = recieved_data.get('email')
        password = recieved_data.get('password')

        print(email,password)  

        return make_response(jsonify({'message':'Login Successful'}),200) 

