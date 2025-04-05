from flask import Flask, session, render_template
from extensions import mysql
from config import Config
from Apps.Product import prodcuts_bp
from Apps.Profiles import profiles_bp
from Apps.Main import main_bp
from Apps.Purchase import purchase_bp
from Apps.MySQL_connettions import get_shopping_carts


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Yapılandırmayı yükle

    # MySQL'i uygula bağla
    mysql.init_app(app)

    # Tüm route'ları kaydet
    app.register_blueprint(main_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(prodcuts_bp)
    app.register_blueprint(purchase_bp)
    # Bağlam işleyicisini ekle


    @app.context_processor
    def inject_shopping_carts():
        if session.get("id"):
            shopping_carts = get_shopping_carts(session["id"])
            return dict(navbar_shopping_carts=shopping_carts)
        else:
            return dict(shopping_carts=[])

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('not_found.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
