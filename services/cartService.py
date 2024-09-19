# cartService.py
from database import db
from models.cart import Cart
from models.product import Product
from models.cartProduct import cart_product
from sqlalchemy import select
from datetime import date  # need to get today's date for the cart

# def save(cart_data):

#     new_cart = Cart(customer_id=cart_data['customer_id'], date=date.today()) # date.today() will generate today's date and store it in the date category

#     for item_id in cart_data['product_ids']:
#         query = select(Product).where(Product.id==item_id)  # search the product table for a product whose id matches the item_id we're looping over
#         item = db.session.execute(query).scalar()
#         new_cart.products.append(item)  # creates the connection from Cart to the associate id, and populates our cart_product table

#     db.session.add(new_cart)
#     db.session.commit()

#     db.session.refresh(new_cart)
#     return new_cart

def save(cart_data):

    new_cart = Cart(customer_id=cart_data['customer_id'], date=date.today())  # Create a new cart instance

    # Commit the cart to generate cart_id
    db.session.add(new_cart)
    db.session.commit()  # Ensure that the cart_id is generated after commit
    print(f"Cart ID after commit: {new_cart.id}")  # Confirm the generated cart ID

    # Loop to handle product additions and quantity settings
    for index, item_id in enumerate(cart_data['product_ids']):
        # Find the product
        query = select(Product).where(Product.id == item_id)
        item = db.session.execute(query).scalar()

        if item:
            # Add product to the cart
            new_cart.products.append(item)
            db.session.add(new_cart)  # Add to session to ensure the association table record is created

            # Commit to ensure cart-product association record creation
            db.session.commit()

            # Now we can update the quantity in the association table
            quantity = cart_data['quantities'][index]  # Get the corresponding product quantity
            cart_product_entry = db.session.query(cart_product).filter_by(cart_id=new_cart.id, product_id=item_id).first()

            if cart_product_entry:
                cart_product_entry.quantity = quantity  # Set the quantity
                db.session.commit()  # Commit changes promptly

    db.session.refresh(new_cart)  # Refresh the cart instance to get the latest data
    return new_cart


def find_all_carts(page=1, per_page=10):
    query = select(Cart)
    all_carts = db.paginate(query, page=int(page), per_page=int(per_page))
    return all_carts


# Function to update an existing cart
def update_cart(cart_id, cart_data):
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return None

    # Update cart details (e.g., cart_date, products)
    cart.cart_date = cart_data.get('cart_date', cart.cart_date)

    # Update products if provided
    if 'product_ids' in cart_data:
        cart.products.clear()  # Clear existing products
        products = db.session.execute(select(Product).filter(Product.id.in_(cart_data['product_ids']))).scalars().all()
        cart.products.extend(products)

    db.session.commit()
    db.session.refresh(cart)
    return cart

# Function to delete a cart by its ID
def delete_cart(cart_id):
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return None

    db.session.delete(cart)
    db.session.commit()
    return cart
