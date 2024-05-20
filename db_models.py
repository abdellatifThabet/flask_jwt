
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

class User(db.Model):
    """
    User model containing user data. Password field contains hashed passwords
    """

    __tablename__ = "user"
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(255), nullable=False)
    email: str = db.Column(db.String(255), nullable=False)
    password: str = db.Column(db.String(255))


    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
            
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlockList(db.Model):
    __tablename__ = "token_block_list"
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return f"<Token  {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()