# cart.py
from database import db
from models.cartProduct import cart_product  # 导入中间表

class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    date = db.Column(db.Date, nullable=False)

    # 定义与 Product 的多对多关系，使用中间表
    products = db.relationship('Product', secondary=cart_product, back_populates='carts')

    # 定义与 Customer 的一对多关系
    customer = db.relationship('Customer', back_populates='carts')
