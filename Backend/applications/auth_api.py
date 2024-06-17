from applications.user_datastore import user_datastore
from flask_restful import Resource
from flask import make_response, jsonify, request
from flask_security import utils, auth_token_required



class Login(Resource):
    def post(self):
        recieved_data = request.get_json()

        email = recieved_data.get('email')
        password = recieved_data.get('password')

        if not email or not password:
            return make_response(jsonify({'message':'Email and Password are required'}),400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({'message':'Invalid Credentials - User doesn\'t exists '}),401)
        
        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message':'Invalid Credentials - Invalid Password'}),401)

        utils.login_user(user)
        auth_token = user.get_auth_token()

        response = {
            'message':'Login Successful',
            'user':{
                'username':user.username,
                'email':user.email,
                'address' : user.address,
                'roles': [role.name for role in user.roles],
                'auth_token':auth_token
            }
        } 
        return make_response(jsonify(response),200) 
    

class Register(Resource):
    def post(self):
        recieved_data = request.get_json()

        email = recieved_data.get('email')
        password = recieved_data.get('password')
        username = recieved_data.get('username')
        address = recieved_data.get('address')
        role   = recieved_data.get('role')

        if not email or not password or not username:
            return make_response(jsonify({'message':'Email, Username and Password are required'}),400)
        
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({'message':'User with provided email id already exists'}),400)
        
        user = user_datastore.find_user(username=username)
        if user:
            return make_response(jsonify({'message':'User with provided username already exists'}),400)
        
        # Input validations at Backend

        if '@' not in email or '.' not in email:
            return make_response(jsonify({'message':'Invalid Email'}),400)
        
        if len(password) < 8:
            return make_response(jsonify({'message':'Password must be atleast 8 characters long'}),400)
        
        if len(username) < 3 or not username.isalnum():
            return make_response(jsonify({'message':'Username must be atleast 3 characters long and alphanumeric characters'}),400)

        if role not in ['admin','manager','user']:
            return make_response(jsonify({'message':'Invalid Role'}),400)
        
        try:
            role = user_datastore.find_role(role)
            user = user_datastore.create_user(email=email, username=username, password=utils.hash_password(password), address=address,roles=[role])
            user_datastore.commit()
            # auth_token = user.get_auth_token()

            response = {
                'message':'User Registered Successfully',
                'user':{
                    'username':user.username,
                    'roles': [role.name for role in user.roles],
                }
            } 
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),500)
        

class Logout(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        return make_response(jsonify({'message':'Logout Successful'}),200)

