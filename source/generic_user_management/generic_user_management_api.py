from flask_restful import Api
from generic_user_management.api_management import ApiManagement
from generic_user_management.user_management import Users, UserManagement


def create_api(app):
    api = Api(app)
    api.add_resource(ApiManagement, '/api/v1')
    api.add_resource(Users, '/api/v1/<tenant_key>/users')
    api.add_resource(
        UserManagement, '/api/v1/<tenant_key>/users/<int:user_id>')
    return api
