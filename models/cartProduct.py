# cartProduct.py
from database import db

# 定义 cart 和 product 之间的多对多关系表，并增加 quantity 字段
cart_product = db.Table(
    'cart_product',
    db.Column('cart_id', db.Integer, db.ForeignKey('carts.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)  # 增加 quantity 整数字段，默认为1
)
