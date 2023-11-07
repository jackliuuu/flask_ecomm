from init import db



class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True,nullable=False)
    pwd = db.Column(db.String(128))
    nick_name = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))
