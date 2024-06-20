from flask_restful import fields

category = {
    "category_id":fields.Integer,
    "name":fields.String,
    "description":fields.String
}

requests = {
                    'request_id':fields.Integer,
                    'username':fields.String,
                    'category_id':fields.Integer,
                    'request_type':fields.String,
                    'request_date':fields.DateTime,
                    'status':fields.String,
                    'new_category_name':fields.String,
                    'new_category_description':fields.String,
                }