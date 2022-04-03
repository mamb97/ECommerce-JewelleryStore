from flask import Flask, render_template
import os
from product import product_api
from contact import contact_api
from backend.account import account_api


def create_app():

    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, '../frontend/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, '../frontend/templates')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('product.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.register_blueprint(product_api)
    app.register_blueprint(contact_api)
    app.register_blueprint(account_api)
    app.run()
