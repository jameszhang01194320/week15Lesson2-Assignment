from database import db
from models.order import Order
from sqlalchemy import select
from datetime import date
from models.cart import Cart

class OrderService:

    @staticmethod
    def save(order_data):
        # 从 order_data 中获取 cart_id
        cart_id = order_data.get('cart_id')
        
        # 从数据库中获取购物车数据
        cart = db.session.query(Cart).filter_by(id=cart_id).first()
        if not cart:
            raise ValueError("购物车未找到。")
        
        # 创建新的订单
        new_order = Order(customer_id=cart.customer_id, date=date.today())
        db.session.add(new_order)
        db.session.commit()

        # 更新订单后进行刷新，确保拿到订单ID
        db.session.refresh(new_order)

        # 清空购物车或做标记
        db.session.delete(cart)  # 也可以标记为已处理，例如 cart.is_processed = True

        # 提交删除或标记操作
        db.session.commit()

        return new_order

    @staticmethod
    def find_all(page=1, per_page=10):
        query = select(Order)
        # 使用分页功能
        all_orders = db.paginate(query, page=int(page), per_page=int(per_page))
        return all_orders
