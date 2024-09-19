from flask import Blueprint
from controllers.cartController import save, find_all

cart_blueprint = Blueprint("cart_bp", __name__)

cart_blueprint.route('/', methods=["POST"])(save)
cart_blueprint.route('/', methods=["GET"])(find_all)

