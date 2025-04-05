# routes.py
from flask import render_template, redirect, request, url_for, flash, session, jsonify, Blueprint
from passlib.hash import sha256_crypt
from Apps.Functions import unauthorized_operation
from Apps.MySQL_connettions import delete_address, get_user_addres_name, update_user_address, update_user, check_usermane_id, get_user_address, get_user, get_seller_products, update_user_log, get_username, check_usermane, save_user, get_districts, get_streets, get_neighborhoods, get_cities, save_address, update_address
from Apps.Forms import LoginForm, RegisterForm, UpdateUserForm, AddressForm

profiles_bp = Blueprint("profiles", __name__)


@profiles_bp.route("/profile")
def profile():
    if session["member_type"] == "admin":
        ado = "admin yazır"
        return render_template("profile.html", ado=ado)
    elif session["member_type"] == "buyer":
        adwad = "buyer yazır"

        return render_template("profile.html", adwad=adwad)

    elif session["member_type"] == "seller":
        products = get_seller_products(session["id"]).fetchall()
        return render_template("profile.html", products=products)
    else:
        _else = "else yazır"
        return render_template("profile.html", awww=_else)


@profiles_bp.route("/logout")
def logout():
    # update last login
    update_user_log("0", session["id"])
    session.clear()
    flash("Çıkış yapıldı", "success")
    return redirect(url_for("main.index"))


@profiles_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    # Kullanıcı zaten giriş yaptıysa, login sayfasına erişemez
    if session.get("logged_in"):
        # Kullanıcıyı profil sayfasına yönlendir
        return redirect(url_for("profiles.profile"))

    if request.method == "POST" and form.validate():
        username = form.username.data
        password_entered = form.password.data
        result = get_username(username)
        if result:
            data = result.fetchone()
            password_real = data["password"]
            if sha256_crypt.verify(password_entered, password_real):
                session["member_type"] = data["member_type"]
                session["id"] = data["id"]
                session["username"] = username
                session["logged_in"] = True

                # Son giriş ve aktiflik güncelleme
                update_user_log("1", data["id"])

                flash("Giriş Başarılı", "success")
                return redirect(url_for("profiles.profile"))
            else:
                flash("Şifre yanlış", "danger")
                return redirect(url_for("profiles.login"))
        else:
            flash("Kullanıcı adı hatalı", "danger")
            return redirect(url_for("profiles.login"))
    else:
        return render_template("login.html", form=form)


@profiles_bp.route("/get_districts/<int:city_id>")
def get_districts_api(city_id):
    districts = get_districts(city_id)
    return jsonify(districts)


@profiles_bp.route("/get_streets/<int:district_id>")
def get_streets_api(district_id):
    streets = get_streets(district_id)
    return jsonify(streets)


@profiles_bp.route("/get_neighborhoods/<int:street_id>")
def get_neighborhoods_api(street_id):
    neighborhoods = get_neighborhoods(street_id)
    return jsonify(neighborhoods)


@profiles_bp.route("/register", methods=["GET", "POST"])
def register():
    # Kullanıcı zaten giriş yaptıysa, login sayfasına erişemez
    if session.get("logged_in"):
        # Kullanıcıyı profil sayfasına yönlendir
        return redirect(url_for("profiles.profile"))
    form = RegisterForm(request.form)
    # Seçeneklerin ilk değerlerini belirle
    form.city.choices = [(0, "Lütfen şehir seçin")] + get_cities()
    form.district.choices = [(0, "Önce şehir seçin")]
    form.street.choices = [(0, "Önce ilçe seçin")]
    form.neighborhood.choices = [(0, "Önce sokak seçin")]
    if request.method == "POST":
        # Eğer şehir seçildiyse, ilgili ilçeleri al ve forma ekle
        if form.city.data:
            form.district.choices = get_districts(form.city.data)
        if form.district.data:
            form.street.choices = get_streets(form.district.data)
        if form.street.data:
            form.neighborhood.choices = get_neighborhoods(form.street.data)
        if form.validate():
            name = form.name.data
            surname = form.surname.data
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(form.password.data)
            birth_date = form.birth_date.data
            member_type = form.member_type.data
            result = check_usermane(username)
            if result > 0:
                flash(
                    "Kullanıcı adı mevcut lütfen farklı bir kullanıcı adı tercih ediniz.", "danger")
                return render_template("register.html", form=form)
            address_title = form.address_title.data
            # Adres verileri
            city_id = int(form.city.data) if isinstance(form.city.data, str) and form.city.data.isdigit(
            ) else int(form.city.data) if isinstance(form.city.data, int) else 0
            district_id = int(form.district.data) if isinstance(form.district.data, str) and form.district.data.isdigit(
            ) else int(form.district.data) if isinstance(form.district.data, int) else 0
            street_id = int(form.street.data) if isinstance(form.street.data, str) and form.street.data.isdigit(
            ) else int(form.street.data) if isinstance(form.street.data, int) else 0
            neighborhood_id = int(form.neighborhood.data) if isinstance(form.neighborhood.data, str) and form.neighborhood.data.isdigit(
            ) else int(form.neighborhood.data) if isinstance(form.neighborhood.data, int) else 0
            open_address = form.address.data
            if city_id == 0 or district_id == 0 or street_id == 0 or neighborhood_id == 0:
                flash("Lütfen geçerli bir adres seçin.", "danger")
                return render_template("register.html", form=form)

            # Adresi kaydet
            address_id = save_address(
                address_title, city_id, district_id, street_id, neighborhood_id, open_address)

            # Kullanıcıyı kaydet
            save_user(name, surname, username, email, password,
                      birth_date, member_type, str(address_id)+",")
            flash("Kayıt işlemi başarılı", "success")
            return redirect(url_for("profiles.login"))
        else:
            flash("Formda hatalar var, lütfen kontrol edin.", "danger")
            return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)


@profiles_bp.route("/user_update", methods=["GET", "POST"])
def user_update():
    if session:
        form = UpdateUserForm(request.form)

        # Seçeneklerin ilk değerlerini belirle
        form.city.choices = [(0, "Lütfen şehir seçin")] + get_cities()
        form.district.choices = [(0, "Önce şehir seçin")]
        form.street.choices = [(0, "Önce ilçe seçin")]
        form.neighborhood.choices = [(0, "Önce sokak seçin")]
        result = get_user(session["id"])
        if result:
            user_info = result.fetchone()
            if request.method == "POST":
                # Eğer şehir seçildiyse, ilgili ilçeleri al ve forma ekle
                if form.city.data:
                    form.district.choices = get_districts(form.city.data)
                if form.district.data:
                    form.street.choices = get_streets(form.district.data)
                if form.street.data:
                    form.neighborhood.choices = get_neighborhoods(
                        form.street.data)
                if form.validate():
                    name = form.name.data if form.name.data else user_info["name"]
                    surname = form.surname.data if form.surname.data else user_info["surname"]
                    username = form.username.data if form.username.data else user_info[
                        "username"]
                    email = form.email.data if form.email.data else user_info["email"]
                    # Kullanıcı adı değişikliği kontrolü
                    # Kullanıcı adı değişmiş mi?
                    if form.username.data != session["username"]:
                        result = check_usermane_id(username, session["id"])
                        if result:
                            flash(
                                "Kullanıcı adı mevcut lütfen farklı bir kullanıcı adı tercih ediniz.", "danger")
                            return render_template("profile/user_update.html", form=form)

                        # Şifre değişikliği kontrolü
                    if form.password.data:
                        if not sha256_crypt.verify(form.old_password.data, user_info["password"]):
                            flash("Eski şifreniz yanlış!", "danger")
                            return render_template("profile/user_update.html", form=form)
                        password = sha256_crypt.encrypt(form.password.data)
                    else:
                        # Eski şifre korunur
                        password = user_info["password"]
                    # Adres verileri
                    address_title = form.address_title.data if form.address_title.data else user_info[
                        "address_title"]

                    city_id = int(
                        form.city.data) if form.city.data else user_info["city_id"]
                    district_id = int(
                        form.district.data) if form.district.data else user_info["district_id"]
                    street_id = int(
                        form.street.data) if form.street.data else user_info["street_id"]
                    neighborhood_id = int(
                        form.neighborhood.data) if form.neighborhood.data else user_info["neighborhood_id"]
                    open_address = form.address.data if form.address.data else user_info[
                        "open_address"]

                    # Adres güncellemesi
                    address_id = update_address(
                        user_info["address_id"], address_title, city_id, district_id, street_id, neighborhood_id, open_address)

                    # Kullanıcı bilgilerini güncelle
                    update_user(name, surname, username, email,
                                password, address_id, session["id"])
                    flash("Güncelleme başarılı", "success")
                    return redirect(url_for("main.index"))

                else:
                    flash("Formda hatalar var, lütfen kontrol edin.", "danger")
                    return render_template("profile/user_update.html", form=form)
            else:
                form.name.data = user_info["name"]
                form.surname.data = user_info["surname"]
                form.username.data = user_info["username"]
                form.email.data = user_info["email"]
                form.password.data = user_info["password"]
                address = get_user_address(user_info["address_id"])
                if address:
                    address_info = address.fetchone()
                    form.address_title.data = address_info["title"]
                    form.city.data = address_info["city_id"]
                    form.district.data = address_info["district_id"]
                    form.street.data = address_info["street_id"]
                    form.neighborhood.data = address_info["neighborhood_id"]
                    form.address.data = address_info["open_address"]

                    # İlçe, sokak ve mahalle seçeneklerini güncelle
                    form.district.choices = [
                        (0, "Lütfen ilçe seçin")] + get_districts(address_info["city_id"])
                    form.street.choices = [
                        (0, "Lütfen sokak seçin")] + get_streets(address_info["district_id"])
                    form.neighborhood.choices = [
                        (0, "Lütfen mahalle seçin")] + get_neighborhoods(address_info["street_id"])

                return render_template("profile/user_update.html", form=form)
        else:
            flash("Yetkisiz işlem.", "danger")
            session.clear()
            return redirect(url_for("profiles.login"))
    else:
        return redirect(url_for("profiles.login"))


@profiles_bp.route("/user_address", methods=["GET"])
def user_address():
    if not session:
        return redirect(url_for("profiles.login"))

    result = get_user(session["id"])
    if not result:
        flash("Yetkisiz işlem.", "danger")
        session.clear()
        return redirect(url_for("profiles.login"))
    user_info = result.fetchone()
    address_lists = get_user_addres_name(user_info["address_id"])
    return render_template("profile/user_address.html", address_lists=address_lists)


@profiles_bp.route("/address_update/<string:address_id>", methods=["GET", "POST"])
def address_update(address_id):
    if not session:
        return unauthorized_operation()
    form = AddressForm(request.form)
    # Seçeneklerin ilk değerlerini belirle
    form.city.choices = [(0, "Lütfen şehir seçin")] + get_cities()
    form.district.choices = [(0, "Önce şehir seçin")]
    form.street.choices = [(0, "Önce ilçe seçin")]
    form.neighborhood.choices = [(0, "Önce sokak seçin")]
    result = get_user(session["id"])
    if not result:
        return unauthorized_operation()
    user_info = result.fetchone()
    if request.method == "POST":
        # Eğer şehir seçildiyse, ilgili ilçeleri al ve forma ekle
        if form.city.data:
            form.district.choices = get_districts(form.city.data)
        if form.district.data:
            form.street.choices = get_streets(form.district.data)
        if form.street.data:
            form.neighborhood.choices = get_neighborhoods(
                form.street.data)
        if not form.validate():
            flash("Formda hatalar var, lütfen kontrol edin.", "danger")
            return render_template("profile/address_update.html", form=form)
         # Adres verileri
        address_title = form.address_title.data if form.address_title.data else user_info[
            "address_title"]
        city_id = int(
            form.city.data) if form.city.data else user_info["city_id"]
        district_id = int(
            form.district.data) if form.district.data else user_info["district_id"]
        street_id = int(
            form.street.data) if form.street.data else user_info["street_id"]
        neighborhood_id = int(
            form.neighborhood.data) if form.neighborhood.data else user_info["neighborhood_id"]
        open_address = form.address.data if form.address.data else user_info[
            "open_address"]

        # Adres güncellemesi
        address_id = update_address(
            user_info["address_id"], address_title, city_id, district_id, street_id, neighborhood_id, open_address)

        # Kullanıcı bilgilerini güncelle
        update_user_address(str(address_id)+",", session["id"])
        flash("Güncelleme başarılı", "success")
        return redirect(url_for("profiles.user_address"))
    else:
        is_owner = False
        address_ids = user_info["address_id"]
        address_id_lists = address_ids.split(",")
        for address_id_list in address_id_lists:
            address_id_list = address_id_list.strip()  # Boşlukları temizle
            if address_id_list == address_id:
                is_owner = True
        if not is_owner:
            return unauthorized_operation()
        address = get_user_address(address_id)
        if not address:
            flash("Adrese erişim sağlanamadı.", "danger")
            return redirect(url_for("profiles.user_address"))
        address_info = address.fetchone()
        form.address_title.data = address_info["title"]
        form.city.data = address_info["city_id"]
        form.district.data = address_info["district_id"]
        form.street.data = address_info["street_id"]
        form.neighborhood.data = address_info["neighborhood_id"]
        form.address.data = address_info["open_address"]

        # İlçe, sokak ve mahalle seçeneklerini güncelle
        form.district.choices = [
            (0, "Lütfen ilçe seçin")] + get_districts(address_info["city_id"])
        form.street.choices = [
            (0, "Lütfen sokak seçin")] + get_streets(address_info["district_id"])
        form.neighborhood.choices = [
            (0, "Lütfen mahalle seçin")] + get_neighborhoods(address_info["street_id"])
        return render_template("profile/address_update.html", form=form)


@profiles_bp.route("/address_delete/<string:address_id>", methods=["GET", "POST"])
def address_delete(address_id):
    delete_address(address_id, session["id"])
    flash("silme işlemi başarılı", "success")

    return redirect(url_for("profiles.user_address"))


@profiles_bp.route("/profile/address_add", methods=["GET", "POST"])
def address_add():
    if not session:
        return unauthorized_operation()
    form = AddressForm(request.form)
    form.city.choices = [(0, "Lütfen şehir seçin")] + get_cities()
    form.district.choices = [(0, "Önce şehir seçin")]
    form.street.choices = [(0, "Önce ilçe seçin")]
    form.neighborhood.choices = [(0, "Önce sokak seçin")]
    if request.method == "POST":
        # Adres verileri
        title = form.address_title.data
        city_id = int(form.city.data) if isinstance(form.city.data, str) and form.city.data.isdigit(
        ) else int(form.city.data) if isinstance(form.city.data, int) else 0
        district_id = int(form.district.data) if isinstance(form.district.data, str) and form.district.data.isdigit(
        ) else int(form.district.data) if isinstance(form.district.data, int) else 0
        street_id = int(form.street.data) if isinstance(form.street.data, str) and form.street.data.isdigit(
        ) else int(form.street.data) if isinstance(form.street.data, int) else 0
        neighborhood_id = int(form.neighborhood.data) if isinstance(form.neighborhood.data, str) and form.neighborhood.data.isdigit(
        ) else int(form.neighborhood.data) if isinstance(form.neighborhood.data, int) else 0
        open_address = form.address.data
        if city_id == 0 or district_id == 0 or street_id == 0 or neighborhood_id == 0 or title == "" or open_address == "":
            flash("Lütfen geçerli bir adres seçin.", "danger")
            return render_template("profile/address_add.html", form=form)
            # Adresi kaydet
        address_id = save_address(
            title, city_id, district_id, street_id, neighborhood_id, open_address)
        # Kullanıcıyı kaydet
        update_user_address(address_id, session["id"])
        flash("Kayıt işlemi başarılı", "success")
        return redirect(url_for("profiles.user_address"))
    else:
        return render_template("profile/address_add.html", form=form)
