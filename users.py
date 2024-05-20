from flask import Blueprint, request, jsonify
from db_models import User
from serializers import UserSchema
from flask_jwt_extended import jwt_required

user_blueprint = Blueprint("users", __name__)




@user_blueprint.get('/all')
@jwt_required()
def get_all_users():
    page = request.args.get("page", default = 1, type = int)
    per_page = request.args.get("per_page", default = 3, type = int)
    users = User.query.paginate(
        page = page,
        per_page = per_page
    )

    results = UserSchema().dump(users, many=True)

    return jsonify({"results": results}), 200