from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services.orderService import OrderService
from marshmallow import ValidationError
from utils.util import token_required

def save():
    try:
        # 从请求中获取 cart_id
        cart_id = request.json.get('cart_id')

        if not cart_id:
            raise ValueError("Cart ID is required.")

        # 调用服务层，从购物车中生成订单
        new_order = OrderService.save({"cart_id": cart_id})

        # 返回新创建的订单信息
        return jsonify({"message": "订单创建成功", "order_id": new_order.id}), 201
    except ValueError as e:
        # 处理购物车为空或未找到的错误
        return jsonify({"error": str(e)}), 400
    except ValidationError as e:
        # 处理数据验证错误
        return jsonify(e.messages), 400

@token_required
def find_all():
    # 获取分页参数
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 10)

    try:
        # 调用服务层获取所有订单
        all_orders = OrderService.find_all(page, per_page)
        return orders_schema.jsonify(all_orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
