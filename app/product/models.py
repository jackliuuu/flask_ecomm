from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(disable_autonaming=True)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    def __init__(self, name, description, price,image_url):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url

    def __str__(self):
        return self.name