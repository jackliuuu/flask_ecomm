from flask import current_app,request
from app.models import User
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import functools
from app.utils import message

def generate_auth_token(uid,expiration):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'id':uid,'exp': expiration})

def verify_auth_token(token):
    
    s = Serializer(current_app.config['SECRET_KEY'])
    
    try:
        data=s.loads(token)
        print(data)
    except Exception:
        return None
    
    usr =User.query.get(data['id']).first()
    return usr

def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            token=request.headers['token']
        except Exception:
            return message.to_dict_msg(10016)
        
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            s.loads(token)
        except Exception:
            return message.to_dict_msg(10017)
        
        return view_func(*args,**kwargs)
    return verify_token