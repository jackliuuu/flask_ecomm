from flask import current_app
from app.models import User
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

def generate_auth_token(uid,expiration):
    s = Serializer(current_app.config['SECRET_KEY'],expire_in=expiration)
    return s.dumps({'id':uid}).decode('utf-8')

def verify_auth_token(token):
    
    s = Serializer(current_app.config['SECRET_KEY'])
    
    try:
        data=s.loads(token)
        print(data)
    except Exception:
        return None
    
    usr =User.query.get(data['id']).first()
    return usr