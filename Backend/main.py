from flask import Flask

from applications.model import User, Role
from applications.database import db
from applications.config import Config
from flask_restful import Api
from applications.user_datastore import user_datastore

from flask_security import Security, hash_password


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)

    api = Api(app, prefix='/api/v1')

    app.security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()

        admin = app.security.datastore.find_or_create_role(name='admin',description='Administrator')
        manager = app.security.datastore.find_or_create_role(name='manager',description='Manager')
        user = app.security.datastore.find_or_create_role(name='user',description = 'Customers')
        if not app.security.datastore.find_user(email="admin@gmail.com"):
            app.security.datastore.create_user(email="admin@gmail.com", username='admin', password=hash_password("password"),roles = [admin])
        db.session.commit()

    return app,  api


app, api = create_app() 


from applications.auth_api import Login, Register, Logout

api.add_resource(Login,'/login')
api.add_resource(Register,'/register')
api.add_resource(Logout,'/logout')

from applications.store_management_api import AllCategories, Category
api.add_resource(Category,'/category')
api.add_resource(AllCategories,'/get_all_categories')

if __name__ == '__main__':
    app.run(debug = True)
