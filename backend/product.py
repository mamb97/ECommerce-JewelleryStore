from flask import render_template, session, Blueprint, redirect, url_for
from database import get_db
from bson.objectid import ObjectId
from datetime import datetime

product_api = Blueprint('product_api', __name__)
product_db = get_db().products
account_db = get_db().accounts


@product_api.route("/products")
def product_list():
    records = [_get_reconstructed_product_dict(r) for r in product_db.find()]
    return render_template('product.html', data=records, username=session.get("username"))


def _get_reconstructed_product_dict(r):
    return {"product_name": r["name"], "product_price": r["price"], "product_image": "/static/img/" + r['img'],
            "product_id": str(r["_id"]), "product_description": r["desc"], "product_description_url": r["_id"]}

def generate_unique_receipt_id():
    return datetime.today().strftime("%Y%m%d%H%M%S%f")

@product_api.route("/product/<product_id>")
def product_description(product_id):
    product_record = _get_reconstructed_product_dict(product_db.find_one({"_id": ObjectId(product_id)}))
    return render_template("product_detail.html", product=product_record, username=session.get("username"))


@product_api.route("/product/purchase/<product_id>")
def purchase(product_id):
    if "username" not in session:
        return "500"
    product_id = product_id.strip()
    product_record = _get_reconstructed_product_dict(product_db.find_one({"_id": ObjectId(product_id)}))
    username = session["username"]
    user_record = account_db.find_one({'email': username})
    order_id = generate_unique_receipt_id()
    receipt_id = (order_id, product_id)
    current_order = {'receipt_id': receipt_id, 'order_id': order_id, 'product': product_record,
                     'address': {'address_line_1': user_record["address"], 'city': user_record["city"],
                                 'state': user_record["state"], 'country': user_record["country"]},
                     'status': [(order_id, 'ordered')]  # (datetime of the order placement, Order state )

                     }
    orders = user_record.get('orders') or []
    orders.append(current_order)
    account_db.update_one({'email': username}, {"$set": {'orders': orders}})
    return "200"
