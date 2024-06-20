from flask_restful import fields
from datetime import datetime

def format_date(date):
    return date.strftime("%Y-%m-%d") if date else None

category = {
    "category_id":fields.Integer,
    "name":fields.String,
    "description":fields.String
}

# requests = {
#                     'request_id':fields.Integer,
#                     'username':fields.String,
#                     'category_id':fields.Integer,
#                     'request_type':fields.String,
#                     'request_date':fields.Raw(attribute=lambda x: x.request_date),
#                     'status':fields.String,
#                     'new_category_name':fields.String,
#                     'new_category_description':fields.String,
#                 }