from flask_restful import Resource, marshal_with
from flask import make_response, jsonify, request as req
from flask_security import auth_token_required, roles_required, roles_accepted, current_user
from applications.model import *
from applications.model import Product as prd
from applications.marshal_fields import *
from datetime import datetime

class AllCategories(Resource):  
    @marshal_with(category)
    def get(self):
        categories = Categories.query.all()
        return categories
    

class ProductsAPI(Resource):
    def get(self, category_id):
        category = Categories.query.get(category_id)
        if not category:
            return make_response(jsonify({'message':'Category does not exist'}),404)
        
        products = prd.query.filter_by(category_id=category_id).all()
        response = []
        for product in products:
            response.append({
                'product_id':product.product_id,
                'name':product.name,
                'description':product.description,
                'selling_price':product.selling_price,
                'stock':product.stock,
                'manufacture_date':product.manufacture_date,
                'expiry_date':product.expiry_date,
                'cost_price':product.cost_price,
                'category_id':product.category_id
            })
        return make_response(jsonify(response),200)
    

# class AllProducts(Resource):
#     def get(self, category_id):
#         products = Product.query.filter_by(category_id=category_id).all()
#         response = []
#         for product in products:
#             category = Categories.query.get(product.category_id)
#             response.append({
#                 'product_id':product.product_id,
#                 'name':product.name,
#                 'description':product.description,
#                 'selling_price':product.selling_price,
#                 'stock':product.stock,
#                 'manufacture_date':product.manufacture_date,
#                 'expiry_date':product.expiry_date,
#                 'cost_price':product.cost_price,
#                 'category':{
#                     'category_id':category.category_id,
#                     'name':category.name,
#                     'description':category.description
#                 }
#             })
#         return make_response(jsonify(response),200)

class Products(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({'message':'Product does not exist'}),404)
        
        category = Categories.query.get(product.category_id)
        response = {
            'product_id':product.product_id,
            'name':product.name,
            'description':product.description,
            'selling_price':product.selling_price,
            'stock':product.stock,
            'manufacture_date':product.manufacture_date,
            'expiry_date':product.expiry_date,
            'cost_price':product.cost_price,
            'category':{
                'category_id':category.category_id,
                'name':category.name,
                'description':category.description
            }
        }
        return make_response(jsonify(response),200)


    @auth_token_required
    @roles_required('manager')
    def post(self):
        data = req.get_json()

        name = data.get('name')
        description = data.get('description')
        selling_price = float(data.get('selling_price'))
        stock = int(data.get('stock'))
        manufacture_date = datetime.strptime(data.get('manufacture_date'),'%Y-%m-%d')
        expiry_date = datetime.strptime(data.get('expiry_date'),'%Y-%m-%d')
        cost_price = float(data.get('cost_price'))
        category_name = data.get('category_name')

        if not name or not selling_price or not stock or not manufacture_date or not cost_price or not category_name:
            return make_response(jsonify({'message':'All fields are required'}),400)
        
        category = Categories.query.filter_by(name=category_name).first()
        if not category:
            return make_response(jsonify({'message':'Category does not exist'}),404)
        
        try:
            product = Product(name=name,description=description,selling_price=selling_price,stock=stock,manufacture_date=manufacture_date,expiry_date=expiry_date,cost_price=cost_price,category_id=category.category_id)
            db.session.add(product)
            db.session.commit()
            response = {
                'message':'Product added successfully',
                'product':{
                    'product_id':product.product_id,
                    'name':product.name,
                    'description':product.description,
                    'selling_price':product.selling_price,
                    'stock':product.stock,
                    'manufacture_date':product.manufacture_date,
                    'expiry_date':product.expiry_date,
                    'cost_price':product.cost_price,
                    'category_id':product.category_id
                }
            }
            return make_response(jsonify(response),201)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('manager')
    def put(self,product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({'message':'Product does not exist'}),404)
        
        data = req.get_json()

        name = data.get('name')
        description = data.get('description')
        selling_price = data.get('selling_price')
        stock = data.get('stock')
        manufacture_date = data.get('manufacture_date')
        expiry_date = data.get('expiry_date')
        cost_price = data.get('cost_price')
        category_name = data.get('category_name')

        if not name and not description and not selling_price and not stock and not manufacture_date and not cost_price and not category_name and not expiry_date:
            return make_response(jsonify({'message':'Edit request is empty with any data'}),400)
        
        if name:
            product.name = name
        if description:
            product.description = description
        if selling_price:
            product.selling_price = selling_price
        if stock:
            product.stock = stock
        if manufacture_date:
            product.manufacture_date = manufacture_date
        if expiry_date:
            product.expiry_date = expiry_date
        if cost_price:
            product.cost_price = cost_price
        if category_name:
            category = Categories.query.filter_by(name=category_name).first()
            if not category:
                return make_response(jsonify({'message':'Category does not exist'}),404)
            product.category_id = category.category_id
        
        try:
            db.session.commit()
            return make_response(jsonify({'message':'Product updated successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
    @auth_token_required
    @roles_required('manager')
    def delete(self,product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({'message':'Product does not exist'}),404)
        
        try:
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message':'Product deleted successfully'}),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)






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
        data = req.get_json()


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
        data = req.get_json()

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
    # @marshal_with(requests)
    def get(self):
        try:
            requests = Requests.query.all()
            response = []
            for request in requests:
                response.append({
                    'request_id':request.request_id,
                    'username':request.username,
                    'category_id':request.category_id,
                    'request_type':request.request_type,
                    'request_date':request.request_date,
                    'status':request.status,
                    'new_category_name':request.new_category_name,
                    'new_category_description':request.new_category_description,
                })
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)
        
class ViewRequest(Resource):   
    @auth_token_required
    @roles_accepted('admin','manager')
    # @marshal_with(requests)
    def get(self,request_id):
        try:
            request = Requests.query.get(request_id)
            if not request:
                return make_response(jsonify({'message':'Request does not exist'}),404)
            response = {
                    'request_id':request.request_id,
                    'username':request.username,
                    'category_id':request.category_id,
                    'request_type':request.request_type,
                    'request_date':request.request_date,
                    'status':request.status,
                    'new_category_name':request.new_category_name,
                    'new_category_description':request.new_category_description,
            }
            return make_response(jsonify(response),200)
        except Exception as e:
            return make_response(jsonify({'message':str(e)}),400)

# class EditRequest(Resource):
#     @auth_token_required
#     @roles_required('manager')
#     def put(self, request_id):
#         data = req.get_json()

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


    


        

    
