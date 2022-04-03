from flask import render_template
from flask import Blueprint
from database import get_db
from bson.objectid import ObjectId

product_api = Blueprint('product_api', __name__)
product_db = get_db().products


@product_api.route("/products")
def product_list():
    records = [_get_reconstructed_product_dict(r) for r in product_db.find()]
    return render_template('product.html', data=records)


def _get_reconstructed_product_dict(r):
    return {"product_name": r["name"], "product_price": r["price"], "product_image": "/static/img/" + r['img'],
            "product_id": str(r["_id"]), "product_description": r["desc"], "product_description_url": r["_id"]}


@product_api.route("/product/<product_id>")
def product_description(product_id):
    record = _get_reconstructed_product_dict(product_db.find_one({"_id": ObjectId(product_id)}))
    return render_template("product_detail.html", product=record)

# @product_api.route("/product/purchase/<product_id>")
# def purchase(product_id):
#
