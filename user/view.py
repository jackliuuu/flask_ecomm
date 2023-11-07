from user import user
from view import db
@user.route("/")
def index():
    return "Hello user"