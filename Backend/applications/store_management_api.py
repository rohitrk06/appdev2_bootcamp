from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request
from flask_security import auth_token_required, roles_required, roles_accepted, current_user
from applications.model import *
from applications.marshal_fields import *
from datetime import datetime

class AllCategories(Resource):  
    @marshal_with(category)
    def get(self):
        categories = Categories.query.all()
        return categories


class Category(Resource):
    @marshal_with(category)
    def get(self,category_id):
        category = Categories.query.get(category_id)
        if not category:
            return make_response(jsonify({'message':'Category does not exist'}),404)
        return category


    @auth_token_required
    @roles_accepted('admin','manager')
    def post(self):
        data = request.get_json()


        name = data.get('name')
        description = data.get('description')

        # Data Validation
        if not name:
            return make_response(jsonify({'message':'Category Name is required'}),400)
        
        if Categories.query.filter_by(name=name).first():
            return make_response(jsonify({'message':'Category already exists'}),400)

        if current_user.has_role('admin'):
            try:
                category = Categories(name=name,description=description)
                db.session.add(category)
                db.session.commit()
                response = {
                    'message':'Category added successfully',
                    'category':{
                        'category_id':category.category_id,
                        'name':category.name,
                        'description':category.description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
        else:

            requests = Requests.query.filter_by(request_type='add_category',status='pending',new_category_name=name).all()
            if requests:
                return make_response(jsonify({'message':'Request already sent to admin for approval'}),400)

            try:
                request = Requests(username=current_user.username, 
                                   request_type='add_category',
                                   request_date = datetime.now(),
                                   status= 'pending', 
                                   new_category_name=name,
                                   new_category_description=description)
                db.session.add(request)
                db.session.commit()
                response = {
                    'message':'Request sent to admin for approval',
                    'request':{
                        'request_id':request.request_id,
                        'username':request.username,
                        'request_type':request.request_type,
                        'request_date':request.request_date,
                        'status':request.status,
                        'new_category_name':request.new_category_name,
                        'new_category_description':request.new_category_description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
    @auth_token_required
    @roles_accepted('admin','manager')
    def put(self,category_id):
        data = request.get_json()

        category = Categories.query.get(category_id)

        if not category:
            return make_response(jsonify({'message':'Category does not exist'}),404)

        name = data.get('name')
        description = data.get('description')

        # Data Validation
        if not name and not description:  
            return make_response(jsonify({'message':'Edit request is empty with any data'}),400)
        
        if name and Categories.query.filter_by(name=name).first():
            return make_response(jsonify({'message':'Category already exists'}),400)

        if current_user.has_role('admin'):
            try:
                if name:
                    category.name = name
                if description:
                    category.description = description
                db.session.commit()
                response = {
                    'message':'Category updated successfully',
                    'category':{
                        'category_id':category.category_id,
                        'name':category.name,
                        'description':category.description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
        else:

            requests = Requests.query.filter_by(request_type='update_category',status='pending',category_id=category_id).all()
            if requests:
                return make_response(jsonify({'message':'Request already sent to admin for approval'}),400)

            try:
                request = Requests(username=current_user.username, 
                                   request_type='update_category',
                                   request_date = datetime.now(),
                                   status= 'pending', 
                                   category_id=category_id,
                                   new_category_name=name,
                                   new_category_description=description)
                db.session.add(request)
                db.session.commit()
                response = {
                    'message':'Request sent to admin for approval',
                    'request':{
                        'request_id':request.request_id,
                        'username':request.username,
                        'request_type':request.request_type,
                        'request_date':request.request_date,
                        'status':request.status,
                        'category_id':request.category_id,
                        'new_category_name':request.new_category_name,
                        'new_category_description':request.new_category_description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)

    @auth_token_required
    @roles_accepted('admin','manager')
    def delete(self, category_id):
        category = Categories.query.get(category_id)

        if not category:
            return make_response(jsonify({'message':'Category does not exist'}),404)
        
        if current_user.has_role('admin'):
            try:
                db.session.delete(category)
                db.session.commit()
                return make_response(jsonify({'message':'Category deleted successfully'}),200)
            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
        else:
            requests = Requests.query.filter_by(request_type='delete_category',status='pending',category_id=category_id).all()
            if requests:
                return make_response(jsonify({'message':'Request already sent to admin for approval'}),400)

            try:
                request = Requests(username=current_user.username, 
                                   request_type='delete_category',
                                   request_date = datetime.now(),
                                   status= 'pending', 
                                   category_id=category_id)
                db.session.add(request)
                db.session.commit()
                response = {
                    'message':'Request sent to admin for approval',
                    'request':{
                        'request_id':request.request_id,
                        'username':request.username,
                        'request_type':request.request_type,
                        'request_date':request.request_date,
                        'status':request.status,
                        'category_id':request.category_id
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)

class ViewRequests(Resource):
    @auth_token_required
    @roles_accepted('admin','manager')
    @marshal_with(requests)
    def get(self):
        try:
            requests = Requests.query.all()
            return requests
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
    
    @auth_token_required
    @roles_accepted('admin','manager')
    @marshal_with(requests)
    def get(self,request_id):
        try:
            request = Requests.query.get(request_id)
            if not request:
                return make_response(jsonify({'message':'Request does not exist'}),404)
            return request
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

class ApproveRequest(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self,request_id):
        request = Requests.query.get(request_id)

        if not request:
            return make_response(jsonify({'message':'Request does not exist'}),404)

        if request.status == 'approved':
            return make_response(jsonify({'message':'Request already approved'}),400)

        if request.status == 'rejected':
            return make_response(jsonify({'message':'Request already rejected'}),400)

        if request.request_type == 'add_category':
            try:
                category = Categories.query.filter_by(name=request.new_category_name).first()
                if category:
                    request.status = 'rejected'
                    db.session.commit()
                    response = {
                        'message':'Request Rejected - Category already exists',
                    }
                    return make_response(jsonify(response),400)

                category = Categories(name=request.new_category_name,description=request.new_category_description)
                db.session.add(category)
                request.status = 'approved'
                db.session.commit()
                response = {
                    'message':'Category added successfully',
                    'category':{
                        'category_id':category.category_id,
                        'name':category.name,
                        'description':category.description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)

        if request.request_type == 'update_category':
            try:
                category = Categories.query.filter_by(name=request.new_category_name).first()
                if category:
                    request.status = 'rejected'
                    db.session.commit()
                    response = {
                        'message':'Request Rejected - Category already exists',
                    }
                    return make_response(jsonify(response),400)

                category = Categories.query.get(request.category_id)
                ###
                if request.new_category_name:
                    category.name = request.new_category_name
                if request.new_category_description:
                    category.description = request.new_category_description

                request.status = 'approved'

                db.session.commit()
                response = {
                    'message':'Category updated successfully',
                    'category':{
                        'category_id':category.category_id,
                        'name':category.name,
                        'description':category.description
                    }
                }
                return make_response(jsonify(response),201)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)

        if request.request_type == 'delete_category':
            try:
                category = Categories.query.get(request.category_id)
                if not category:
                    request.status = 'rejected'
                    db.session.commit()
                    response = {
                        'message':'Request Rejected - Category does not exist',
                    }
                    return make_response(jsonify(response),400)

                db.session.delete(category)
                request.status = 'approved'
                db.session.commit()                
                return make_response(jsonify({'message':'Category deleted successfully'}),200)

            except Exception as e:
                return make_response(jsonify({'message':str(e)}),400)
            
class RejectRequest(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self,request_id):
        request = Requests.query.get(request_id)

        if not request:
            return make_response(jsonify({'message':'Request does not exist'}),404)

        if request.status == 'approved':
            return make_response(jsonify({'message':'Request already approved'}),400)

        if request.status == 'rejected':
            return make_response(jsonify({'message':'Request already rejected'}),400)
        try:
            request.status = 'rejected'
            db.session.commit()
            response = {
                'message':'Request Rejected',
            }
            return make_response(jsonify(response),200)
        
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)


    


        

    
