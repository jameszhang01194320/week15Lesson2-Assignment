from flask import request, jsonify
from models.schemas.orderSchema import order_schema, orders_schema
from services import orderService
from marshmallow import ValidationError
# from utils.util import admin_required, user_validation
from database import db 


def save():
    try:
        order_data = order_schema.load(request.json)
        new_order = orderService.save(order_data)
        return order_schema.jsonify(new_order), 201
    except ValidationError as e:
        return jsonify(e.messages), 400


def find_all():
    page = request.args.get("page")
    per_page = request.args.get("per_page")
    page = 1 if not page else page
    per_page = 10 if not per_page else per_page
    all_orders = orderService.find_all_orders(page, per_page)
    
    return orders_schema.jsonify(all_orders), 200

def find_by_id(order_id): #dynamic route takes in parameters
    order = orderService.find_by_id(order_id)

    return order_schema.jsonify(order), 200

def place_order_route():
    customer_id = request.json.get('customer_id')

    try:
        new_order = orderService.place_order(customer_id, db)
        return jsonify({"message": "place order success:", "order_id": new_order.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
