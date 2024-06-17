from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request
from flask_security import auth_token_required, roles_required, roles_accepted
from applications.model import *
from applications.marshal_fields import *

class AllCategories(Resource):  
    @marshal_with(category)
    def get(self):
        categories = Categories.query.all()
        return categories


class Category(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')

        # Data Validation
        if not name:
            return make_response(jsonify({'message':'Category Name is required'}),400)
        
        if Categories.query.filter_by(name=name).first():
            return make_response(jsonify({'message':'Category already exists'}),400)
        
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
        

    
