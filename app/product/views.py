from flask.views import MethodView
from flask import render_template, request, redirect, url_for,abort
from .models import Product
from flask import Blueprint
from .models import db


class ProductView(MethodView):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if product:
            product_info = {
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image_url
            }
            return render_template('product.html', product_info=product_info)
        else:
            return abort(404)
     
        
class AddProductView(MethodView):
    def get(self):
        return render_template('add_product.html')
    
    def post(self):
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('product.product_view', product_id=1))
        

product_bp = Blueprint('product', __name__)


product_view = ProductView.as_view('product_view')
addproduct_view = AddProductView.as_view('addproduct_view')
product_bp.add_url_rule('/product/<int:product_id>/', view_func=product_view)
product_bp.add_url_rule('/product/addproduct/',view_func=addproduct_view)

