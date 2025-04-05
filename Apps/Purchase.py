# routes.py
from flask import render_template, redirect,  url_for, flash, session,  Blueprint, jsonify, request
from Apps.MySQL_connettions import add_to_cart, update_shopping_carts, delete_shopping_cart, get_shopping_carts, get_user_addres_name, get_user
from Apps.Functions import shopping_cart_price
purchase_bp = Blueprint("purchase", __name__)


@purchase_bp.route("/add_to_cart/<string:product_id>")
def shopping_carts_save(product_id):
    count = request.args.get('quantity', default=1, type=int)
    add_to_cart(session['id'], product_id, count, "1")
    return jsonify({"status": "success", "message": "Ürün sepete eklendi"})


@purchase_bp.route("/shopping_carts/shopping_cart_add/<string:product_id>")
def shopping_carts_update_add(product_id):
    count = 1
    update_shopping_carts(session['id'], product_id, count)
    return redirect(url_for('purchase.shopping_carts'))


@purchase_bp.route("/shopping_carts/shopping_cart_remove/<string:product_id>")
def shopping_carts_update_remove(product_id):
    count = -1
    update_shopping_carts(session['id'], product_id, count)
    return redirect(url_for('purchase.shopping_carts'))


@purchase_bp.route("/shopping_carts/shopping_cart_delete/<string:product_id>")
def shopping_carts_delete(product_id):
    delete_shopping_cart(session['id'], product_id)
    return redirect(url_for('purchase.shopping_carts'))


@purchase_bp.route("/shopping_carts")
def shopping_carts():
    shopping_carts = get_shopping_carts(session["id"])
    if shopping_carts:
        total_price = shopping_cart_price(shopping_carts)
        print("total_price")

        print(shopping_carts)
        cargo_price = 50
        return render_template("shopping_carts.html", shopping_carts=shopping_carts, user=session["username"], total_price=total_price, cargo_price=cargo_price)
    else:
        return render_template("shopping_carts.html")


@purchase_bp.route("/shopping_carts/purchase")
def shopping_carts_purchase():
    if not session:
        return redirect(url_for("profiles.login"))
    result = get_user(session["id"])
    if not result:
        flash("Yetkisiz işlem.", "danger")
        session.clear()
        return redirect(url_for("profiles.login"))
    shopping_carts = get_shopping_carts(session["id"])
    if not shopping_carts:
        flash("sepete ürün ekleyin lütfen", "danger")
        return redirect(url_for("purchase.shopping_carts"))

    total_price = shopping_cart_price(shopping_carts)

    user_info = result.fetchone()
    address_list = get_user_addres_name(user_info["address_id"])
    if not address_list:
        return redirect(url_for("profiles.address_add"))
    return render_template("purchase.html", shopping_carts=shopping_carts, total_price=total_price, address_lists=address_list)
