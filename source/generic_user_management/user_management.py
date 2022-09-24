from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash


class Users(Resource):
    def get(self, tenant_key):
        from .models.generic_user_management_models import User
        users = User.query.filter_by(tenant_key=tenant_key)
        result = [u.as_json() for u in users]
        print(tenant_key)
        return jsonify(result)

    def post(self, tenant_key):
        from . import db
        from .models.generic_user_management_models import User

        new_user_json = request.get_json()
        user = User.query.filter_by(
            email=new_user_json['email'], tenant_key=tenant_key).first()
        if user:
            return {'result': 'User already exists', 'JSON received': new_user_json}, 409
        else:
            new_user = User()
            new_user.first_name = new_user_json['first_name']
            new_user.last_name = new_user_json['last_name']
            new_user.email = new_user_json['email']
            new_user.mobile = new_user_json['mobile']
            new_user.tenant_key = tenant_key
            new_user.password = generate_password_hash(
                new_user_json['plain_text_password'], method='sha256')
            db.session.add(new_user)
            db.session.commit()
            return {'result': 'User created', 'JSON received': new_user_json}


class UserManagement(Resource):
    def get(self, tenant_key, user_id):
        from .models.generic_user_management_models import User
        user = User.query.filter_by(tenant_key=tenant_key, id=user_id).first()

        if not user:
            return {'result': 'No user by that id', 'Id received': user_id}, 404

        return jsonify(user.as_json())

    def put(self, tenant_key, user_id):
        from . import db
        from .models.generic_user_management_models import User
        user = User.query.filter_by(tenant_key=tenant_key, id=user_id).first()

        if not user:
            return {'result': 'No user by that id', 'Id received': user_id}, 404

        user_json = request.get_json()
        user.first_name = user_json['first_name']
        user.last_name = user_json['last_name']
        user.email = user_json['email']
        user.mobile = user_json['mobile']

        db.session.commit()
        return {'result': 'User updated', 'JSON received': user_json}

    def delete(self, tenant_key, user_id):
        from . import db
        from .models.generic_user_management_models import User
        user = User.query.filter_by(tenant_key=tenant_key, id=user_id).first()

        if not user:
            return {'result': 'No user by that id', 'Id received': user_id}, 404
        db.session.delete(user)
        db.session.commit()
        return {'result': 'User deleted', 'Id received': user_id}
