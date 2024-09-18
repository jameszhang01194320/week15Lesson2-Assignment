from flask import Blueprint
from controllers.orderController import find_by_id, save, find_all, place_order_route

order_blueprint = Blueprint("order_bp", __name__)

order_blueprint.route('/', methods=["POST"])(save)
order_blueprint.route('/', methods=["GET"])(find_all)
order_blueprint.route('/<int:order_id>', methods=['GET'])(find_by_id)

order_blueprint.route('/place_order', methods=["POST"])(place_order_route)