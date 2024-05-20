from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token,\
      jwt_required, get_jwt, current_user, get_jwt_identity
from db_models import User, TokenBlockList

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register_user():

    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))
    if user:
        return jsonify({"error": "user already exists"})
    
    new_user = User(
        username= data.get("username"),
        email= data.get("email")
    )
    new_user.set_password(password= data.get("password"))
    new_user.save()

    return jsonify({"message": "user created"})

@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user and (user.check_password(data.get("password"))):
        access_token = create_access_token(identity = user.username)
        refresh_token = create_refresh_token(identity = user.username)
        return jsonify({"message": "user logged in",
                        "tokens": {
                            "access_token": access_token,
                            "refresh_token": refresh_token
                        } }), 200
    return jsonify({"error": "invalid username or password"}), 400

@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({"message": "message",
                    "user details": {"username": current_user.username,
                                     "email": current_user.email}}), 200

@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_acces_token = create_access_token(identity = identity)
    new_refresh_token =     create_refresh_token(identity = identity)
    return jsonify({"access_token": new_acces_token,
                    "refresh_token": new_refresh_token})


@auth_bp.get('/logout')
@jwt_required()
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']

    token_blockist = TokenBlockList(jti = jti)

    token_blockist.save()

    return jsonify({"message": "logged out"}), 200