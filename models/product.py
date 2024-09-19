# product.py
from database import db
from models.cartProduct import cart_product  # 确保中间表已被导入

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # 定义与 Cart 的多对多关系，使用中间表
    carts = db.relationship('Cart', secondary=cart_product, back_populates='products')
