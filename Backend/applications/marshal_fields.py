from flask_restful import fields

category = {
    "category_id":fields.Integer,
    "name":fields.String,
    "description":fields.String

}

categories = {
    "categories":fields.List(fields.Nested(category))
}