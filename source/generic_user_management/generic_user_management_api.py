from flask_restful import Api
from generic_user_management.api_management import ApiManagement
from generic_user_management.user_management import Users


def create_api(app):
    api = Api(app)
    api.add_resource(ApiManagement, '/')
    api.add_resource(Users, '/<tenant_key>/users')
    return api
