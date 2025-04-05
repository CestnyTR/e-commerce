# routes.py
from flask import render_template, request,  render_template, redirect, request, url_for, flash, session,  Blueprint, current_app
from Apps.Functions import save_pictures, save_file, delete_file
from flask import render_template
from Apps.Forms import ProductForm
from Apps.MySQL_connettions import save_product, update_product, get_product, delete_product, get_category, get_color, get_products, get_products_details

prodcuts_bp = Blueprint("prodcuts", __name__)


@prodcuts_bp.route("/product/products")
def products():
    category_title = request.args.get('category')  # Get category from query parameters
    products = get_products(category_title)
    return render_template("/product/products.html", products=products)


@prodcuts_bp.route("/product/products/<string:id>")
def products_details(id):
    result = get_products_details(id)
    if result:
        return render_template("/product/products_details.html", products=result)
    else:
        return render_template("/product/products_details.html")


@prodcuts_bp.route("/product/product_add", methods=["GET", "POST"])
def product_add():
    if session:
        form = ProductForm(request.form, request.files)
        form.category.choices = get_category()
        form.color.choices = get_color()
        if request.method == "POST" and form.validate():
            owner_id = session["id"]
            title = form.title.data
            category = form.category.data
            stock = form.stock.data
            active = form.active.data
            content = form.content.data
            price = form.price.data
            color = form.color.data

            # Gelen dosyaları al
            pictures = request.files.getlist("pictures")
            picture_orders = request.form.getlist("picture_order")

            picture_orders = list(map(int, picture_orders))

            # Resimleri sıralamak için bir boş liste oluştur
            sorted_pictures_list = [None] * len(pictures)

            # picture_orders'a göre resimleri sıralayın
            for i, order in enumerate(picture_orders):
                sorted_pictures_list[i] = pictures[order]

            saved_images = save_pictures(
                sorted_pictures_list, current_app.config['UPLOAD_FOLDER'], owner_id, category, title, color)

            if not saved_images:
                flash("Resim yükleme başarısız oldu!", "danger")
                return render_template("product/product_add.html", form=form)
            save_product(title, category, stock, active, owner_id,
                         content, color, price, saved_images)
            flash("Ürün başarıyla eklendi!", "success")
            return redirect(url_for("profiles.profile"))

        return render_template("product/product_add.html", form=form)

    flash("Sadece üyeler ürün ekleyebilir.", "danger")
    return redirect(url_for("profiles.login"))


@prodcuts_bp.route("/product/product_update/<int:id>", methods=["GET", "POST"])
def product_update(id):
    if session:
        form = ProductForm(request.form, request.files)
        form.category.choices = get_category()
        form.color.choices = get_color()
        owner_id = session["id"]
        result = get_product(session["id"], id)
        if result:
            product = result.fetchone()
            if request.method == "POST" and form.validate():
                title = form.title.data
                category = form.category.data
                stock = form.stock.data
                active = form.active.data
                content = form.content.data
                color = form.color.data
                price = form.price.data
                existing_pictures = [product[f"pic_{i+1}"]
                                     for i in range(6) if product[f"pic_{i+1}"]]
                remaining_pictures = request.form.getlist("old-image[]")
                deleted_pictures = set(existing_pictures) - \
                    set(remaining_pictures)
                updated_pictures = [
                    pic if pic in remaining_pictures else None for pic in existing_pictures]

                for filename in deleted_pictures:
                    delete_file(
                        current_app.config["UPLOAD_FOLDER"], owner_id, filename)

                new_files = request.files.getlist("new_pictures[]")
                new_pictures = []

                for file in new_files:
                    new_filename = save_file(
                        file, current_app.config["UPLOAD_FOLDER"], owner_id, category, title, color)
                    if new_filename:
                        new_pictures.append(new_filename)

                        # Kullanıcının gönderdiği resim sırasını al
                    ordered_pictures = []
                    image_order_list = request.form.getlist("picture_order")
                    ordered_pictures = list(map(int, image_order_list))

                    # Resimleri sıralamak için image_order_list'inin sırasına göre index'lere bakıyoruz
                    all_pictures = updated_pictures + new_pictures

                    # sorted_pictures_list oluşturuluyor
                    sorted_pictures_list = [None] * len(all_pictures)

                    used_orders = set()  # Kullanılmış sıraları takip etmek için set

                    # 'ordered_pictures' içinde geçerli indeksleri filtreleyelim
                    valid_orders = [
                        order for order in ordered_pictures if 0 <= order < len(all_pictures)]

                    for i, order in enumerate(valid_orders):
                        # Eğer sıra zaten kullanılmışsa veya None olan bir yer doldurulmuşsa atlıyoruz
                        if order not in used_orders:
                            sorted_pictures_list[i] = all_pictures[order]
                            used_orders.add(order)

                # Maksimum 6 resim
                pictures_to_save = sorted_pictures_list[:6] + \
                    [None] * (6 - len(all_pictures))
                update_product(id, title, category, stock, active,
                               content, color, price, *pictures_to_save)
                flash("Ürün başarıyla güncellendi!", "success")
                return redirect(url_for("profiles.profile"))
            else:
                form.title.data = product["title"]
                form.category.data = product["category_id"]
                form.stock.data = product["stock"]
                form.active.data = product["active"]
                form.content.data = product["content"]
                form.color.data = product["color_id"]
                form.price.data = product["price"]
                pictures = [product["pic_1"], product["pic_2"], product["pic_3"],
                            product["pic_4"], product["pic_5"], product["pic_6"]]

                return render_template("/product/product_update.html", form=form, pictures=pictures, owner_id=owner_id)
        else:
            flash("Yetkisiz işlem.", "danger")
            return redirect(url_for("profiles.profile"))
    else:
        flash("Sadece üyeler ürün güncelleyebilir.", "danger")
        return redirect(url_for("profiles.login"))


@prodcuts_bp.route("/product/product_delete/<string:id>")
def product_delete(id):
    if session:
        result = get_product(session["id"], id)
        if result:
            product = result.fetchone()
            pictures = [product["pic_1"], product["pic_2"], product["pic_3"],
                        product["pic_4"], product["pic_5"], product["pic_6"]]

            for picture in pictures:
                if picture == None:
                    pass
                delete_file(
                    current_app.config["UPLOAD_FOLDER"], session["id"], picture)

            delete_product(id)
            return redirect(url_for("profiles.profile"))
        else:
            flash("Yetkisiz işlem.", "danger")
            return redirect(url_for("profiles.profile"))
    else:
        flash("Yetkisiz işlem.", "danger")
        return redirect(url_for("main.index"))
