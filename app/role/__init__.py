from flask import Blueprint

from flask_restful import Api

role = Blueprint('role',__name__)

role_api= Api(role)

from app.role import views