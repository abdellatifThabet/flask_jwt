from flask import Flask, jsonify
from flask_migrate import Migrate
from config import config
from extensions import db, jwt

from auth import auth_bp
from users import user_blueprint

from db_models import User, TokenBlockList

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

     
     
    db.init_app(app)
    migrate = Migrate(app, db)

    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix = '/auth')
    app.register_blueprint(user_blueprint, url_prefix = '/users')

    # load user
    @jwt.user_lookup_loader 
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username = identity).one_or_none()

    # additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):

        if identity== "test2":
            return {"is_staff": True}
        return {"is_staff": False} 

    # jwt error handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "token has expired",
                        "error": "token expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "signature verification failed",
                        "error": "invalid check"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "request does not contain a valid token",
                        "error": "auth header"}), 401
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()

        return token is not None

    return app



if __name__== "__main__":
    app = create_app()
    app.run()