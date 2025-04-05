from extensions import mysql
from flask import flash
from datetime import datetime
# CREATE


def save_address(address_title, city_id, district_id, street_id, neighborhood_id, open_address):
    cursor = mysql.connection.cursor()
    query = """
            INSERT INTO address (title,city_id, district_id, street_id, neighborhood_id, open_address)
            VALUES (%s, %s,%s, %s, %s, %s)
        """
    cursor.execute(query, (address_title, city_id, district_id, street_id,
                           neighborhood_id, open_address))
    mysql.connection.commit()

    # Eklenen adresin ID'sini al
    address_id = cursor.lastrowid
    cursor.close()
    return address_id


def save_product(title, category, stock, active, owner_id, content, color, price, saved_images):
    cursor = mysql.connection.cursor()
    insert_products = """
                INSERT INTO products(title, category_id, stock, active, owner_id, content, color_id, price, pic_1, pic_2, pic_3, pic_4, pic_5, pic_6)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

    picture_paths = [saved_images[i] if i < len(
        saved_images) else None for i in range(6)]

    cursor.execute(insert_products, (title, category, stock,
                                     active, owner_id, content, color, price, *picture_paths))
    mysql.connection.commit()
    cursor.close()


def save_user(name, surname, username, email, password, birth_date, member_type, address_id):
    cursor = mysql.connection.cursor()
    query = """
                    INSERT INTO users (name, surname, username, email, password, birth_date, member_type, address_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
    cursor.execute(query, (name, surname, username,
                           email, password, birth_date, member_type, address_id))
    mysql.connection.commit()
    cursor.close()


def add_to_cart(user_id, product_id, quantity, status):
    cursor = mysql.connection.cursor()
    query = "SELECT id, user_id, product_id, quantity, date_added, status FROM shopping_carts WHERE user_id=%s AND product_id=%s"
    result = cursor.execute(query, (user_id, product_id))
    if result:
        update_shopping_carts(user_id, product_id, quantity)
        cursor.close()
        return
    add_query = "INSERT INTO shopping_carts( user_id, product_id, quantity, date_added, status) VALUES (%s,%s,%s,%s,%s)"
    date_added = datetime.now()

    cursor.execute(
        add_query, (user_id, product_id, quantity, date_added, status))
    mysql.connection.commit()
    cursor.close()
# UPDATE


def update_product(id, title, category, stock, active, content, color, price, *pictures_to_save):
    cursor = mysql.connection.cursor()
    update_query = """
        UPDATE products SET title=%s, category_id=%s, stock=%s, active=%s, content=%s, color_id=%s, price=%s,
        pic_1=%s, pic_2=%s, pic_3=%s, pic_4=%s, pic_5=%s, pic_6=%s WHERE id=%s
    """
    # pictures_to_save'i tuple'dan ayrı parametrelere açıyoruz
    pictures_list = list(pictures_to_save)

    # pictures_list'in uzunluğunu 6'ya tamamlamak için None ekle
    while len(pictures_list) < 6:
        pictures_list.append(None)

    cursor.execute(update_query, (title, category, stock, active, content, color, price,
                                  pictures_list[0], pictures_list[1], pictures_list[2],
                                  pictures_list[3], pictures_list[4], pictures_list[5], id))
    mysql.connection.commit()
    cursor.close()


def update_address(address_id, address_title, city_id, district_id, street_id, neighborhood_id, open_address):
    cursor = mysql.connection.cursor()
    query = """
            UPDATE address SET title=%s,city_id=%s, district_id=%s, street_id=%s, neighborhood_id=%s, open_address=%s WHERE id=%s
        """
    cursor.execute(query, (address_title, city_id, district_id, street_id,
                           neighborhood_id, open_address, address_id))
    mysql.connection.commit()
    cursor.close()
    return address_id


def update_user(name, surname, username, email, password, address_id, id):
    cursor = mysql.connection.cursor()
    query = """
                            UPDATE users
                            SET name=%s, surname=%s, username=%s, email=%s, password=%s, address_id=%s
                            WHERE id=%s
                        """
    cursor.execute(query, (name, surname, username,
                   email, password, address_id, id))
    mysql.connection.commit()
    cursor.close()


def update_user_address(address_id, id):
    cursor = mysql.connection.cursor()
    user_query = "SELECT address_id FROM users WHERE id = %s"
    cursor.execute(user_query, (id,))
    user_addres_list = cursor.fetchone()
    user_addres_list = user_addres_list["address_id"]+","+str(address_id)
    query = """
                            UPDATE users
                            SET address_id=%s
                            WHERE id=%s
                        """
    cursor.execute(query, (user_addres_list, id))
    mysql.connection.commit()
    cursor.close()


def update_user_log(status, id):
    cursor = mysql.connection.cursor()
    if status == 0:
        logout = "UPDATE users SET  status=%s WHERE id=%s"
        cursor.execute(logout, (status, id))
        mysql.connection.commit()
    else:
        # Son giriş ve aktiflik güncelleme
        now = datetime.now()
        update_query = "UPDATE users SET last_login=%s, status=%s WHERE id=%s"
        cursor.execute(update_query, (now, status, id))
        mysql.connection.commit()
    cursor.close()


def update_shopping_carts(id, product_id, count):
    """
    Updates the quantity of a product in the shopping cart.
    """
    cursor = mysql.connection.cursor()
    query = "SELECT id, user_id, product_id, quantity, date_added, status FROM shopping_carts WHERE user_id=%s AND product_id=%s"
    result = cursor.execute(query, (id, product_id))

    if result == 0:
        flash("Product not found in shopping cart for this user.", "danger")
        cursor.close()
        return
    products = cursor.fetchall()
    if not products:
        flash("No products found for this user and product ID.", "danger")
        cursor.close()
        return
    product = products[0]
    quantity_change = int(product["quantity"]) + count  # Corrected line
    if quantity_change > 0:
        update_query = """
            UPDATE shopping_carts SET quantity=%s WHERE user_id=%s AND product_id=%s
        """
        cursor.execute(update_query, (quantity_change, id, product_id))
        mysql.connection.commit()
    else:
        delete_shopping_cart(id, product_id)
    cursor.close()
# DELETE


def delete_product(id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM products WHERE id= %s"
    cursor.execute(query, (id,))
    mysql.connection.commit()
    cursor.close()


def delete_shopping_cart(id, product_id):
    cursor = mysql.connection.cursor()
    delete_query = "DELETE FROM shopping_carts WHERE user_id=%s AND product_id=%s"
    cursor.execute(delete_query, (id, product_id))
    mysql.connection.commit()
    cursor.close()


def delete_address(address_id, id):
    cursor = mysql.connection.cursor()
    user_query = "SELECT address_id FROM users WHERE id = %s"
    cursor.execute(user_query, (id,))
    user_address_list = cursor.fetchone()
    if user_address_list and user_address_list["address_id"]:
        address_ids = user_address_list["address_id"].split(",")
        updated_address_ids = [
            addr_id for addr_id in address_ids if addr_id != str(address_id) and addr_id]
        updated_address_string = ",".join(updated_address_ids)

        query = "UPDATE users SET address_id=%s WHERE id=%s"
        cursor.execute(query, (updated_address_string, id))
        mysql.connection.commit()

        query = "DELETE FROM address WHERE id=%s"
        cursor.execute(query, (address_id,))
        mysql.connection.commit()
    cursor.close()
# READ

def get_products(category_title=None, min_price=10, max_price=1000000, color=None):
    cursor = mysql.connection.cursor()
    query = """
        SELECT
            p.id,
            p.title,
            c.title AS category_title,
            p.stock,
            p.active,
            p.owner_id,
            p.content,
            cl.title AS color_title,
            p.price,
            p.pic_1,
            p.pic_2,
            p.pic_3,
            p.pic_4,
            p.pic_5,
            p.pic_6
        FROM
            products p
        LEFT JOIN
            category c ON p.category_id = c.id
        LEFT JOIN
            colors cl ON p.color_id = cl.id
        WHERE
            p.price BETWEEN %s AND %s
    """
    params = [min_price, max_price]

    if category_title:
        # Dynamically create the placeholders for each category in the list
        placeholders = ', '.join(['%s'] * len(category_title))
        query += f" AND c.title IN ({placeholders})"
        params.extend(category_title)  # Add the list of categories to the params

    if color:
        query += " AND cl.title = %s"
        params.append(color)

    cursor.execute(query, params)
    return cursor.fetchall()


def get_product(owner_id, id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM products WHERE owner_id = %s AND id = %s"
    result = cursor.execute(query, (owner_id, id))
    if result:
        return cursor
    else:
        return False


def get_products_details(id):
    cursor = mysql.connection.cursor()
    query = """SELECT
                p.id,
                p.title,
                c.title AS category_title,
                p.stock,
                p.active,
                p.owner_id,
                u.username AS owner,
                p.content,
                cl.title AS color_title,
                p.price,
                p.pic_1,
                p.pic_2,
                p.pic_3,
                p.pic_4,
                p.pic_5,
                p.pic_6
            FROM
                products p
            LEFT JOIN
                category c ON p.category_id = c.id
            LEFT JOIN
                colors cl ON p.color_id = cl.id
            LEFT JOIN
                users u ON p.owner_id = u.id
            WHERE
                p.id = %s;
                """
    result = cursor.execute(query, (id,))
    if result:
        products = cursor.fetchall()
        return products
    else:
        return False


def get_seller_products(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM products WHERE owner_id=%s"
    cursor.execute(query, (id,))
    return cursor


def get_cities():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id,name FROM cities")
    cities = cursor.fetchall()
    cities_choices = [(city['id'], city['name'])
                      for city in cities]
    cursor.close()
    return cities_choices


def get_districts(city_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, name FROM districts WHERE city_id = %s", (city_id,))
    districts = cursor.fetchall()
    districts_choices = [(district['id'], district['name'])
                         for district in districts]
    cursor.close()
    return districts_choices


def get_streets(district_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, name FROM streets WHERE district_id = %s", (district_id,))
    streets = cursor.fetchall()
    streets_choices = [(street['id'], street['name'])
                       for street in streets]
    cursor.close()
    return streets_choices


def get_neighborhoods(street_id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, name FROM neighborhoods WHERE street_id = %s", (street_id,))
    neighborhoods = cursor.fetchall()
    neighborhoods_choices = [(neighborhood['id'], neighborhood['name'])
                             for neighborhood in neighborhoods]
    cursor.close()
    return neighborhoods_choices


def get_color():
    cursor = mysql.connection.cursor()
    query = "SELECT id, title FROM colors"
    cursor.execute(query)
    colors = cursor.fetchall()
    colors_choices = [(color['id'], color['title'])
                      for color in colors]
    cursor.close()
    return colors_choices


def get_category():
    cursor = mysql.connection.cursor()
    query = "SELECT id, title FROM category"
    cursor.execute(query)
    categories = cursor.fetchall()
    category_choices = [(category['id'], category['title'])
                        for category in categories]
    cursor.close()
    return category_choices


def get_user(owner_id):
    cursor = mysql.connection.cursor()

    query = "SELECT id, name, surname, username, email, password, address_id, membership_date, status, last_login FROM users WHERE id = %s"
    result = cursor.execute(query, (owner_id,))
    if result:
        return cursor
    else:
        return False


def get_user_address(user_info):
    cursor = mysql.connection.cursor()
    query = "SELECT id, title,city_id, district_id, street_id, neighborhood_id, open_address FROM address WHERE id=%s"
    result = cursor.execute(query, (user_info,))
    if result:
        return cursor
    else:
        return False


def get_user_addres_name(address_ids):
    address_lists = []
    if address_ids:  # address_id boş değilse işlem yap
        address_id_list = address_ids.split(",")
        for address_id in address_id_list:
            address_id = address_id.strip()  # Boşlukları temizle
            # adres id'yi integer'a çevir
            cursor = mysql.connection.cursor()
            query = "SELECT id, title,city_id, district_id, street_id, neighborhood_id, open_address FROM address WHERE id=%s"
            result = cursor.execute(query, (address_id,))
            if result:
                address_info = cursor.fetchone()
                city = "SELECT id,name FROM cities WHERE id=%s"
                city_name = cursor.execute(city, (address_info["city_id"],))
                city_name = cursor.fetchone()
                city_name = city_name["name"]
                district = "SELECT id,name FROM districts WHERE id=%s"
                district_name = cursor.execute(
                    district, (address_info["district_id"],))
                district_name = cursor.fetchone()
                district_name = district_name["name"]
                street = "SELECT id,name FROM streets WHERE id=%s"
                street_name = cursor.execute(
                    street, (address_info["street_id"],))
                street_name = cursor.fetchone()
                street_name = street_name["name"]
                neighborhood = "SELECT id,name FROM neighborhoods WHERE id=%s"
                neighborhood_name = cursor.execute(
                    neighborhood, (address_info["neighborhood_id"],))
                neighborhood_name = cursor.fetchone()
                neighborhood_name = neighborhood_name["name"]
                addres_name = " "+city_name+" "+district_name+" "+street_name + \
                    " "+neighborhood_name
                address = {"id": address_id, "title":  address_info["title"],
                           "name": addres_name, "open_address": address_info["open_address"]}
                if address:
                    address_lists.append(address)
        return address_lists


def get_shopping_carts(user_id):
    cursor = mysql.connection.cursor()
    query = """SELECT
    u.name AS user_name,
    p.*,
    c.title AS category_title,
    sc.quantity,
    sc.date_added,
    sc.status
FROM
    shopping_carts sc
LEFT JOIN
    users u ON sc.user_id = u.id
LEFT JOIN
    products p ON sc.product_id = p.id
LEFT JOIN
    category c ON p.category_id = c.id
WHERE
    sc.user_id = %s;
    """
    result = cursor.execute(
        query, (user_id,))
    if result:
        return cursor.fetchall()
    else:
        return False


# login


def get_username(username):
    cursor = mysql.connection.cursor()
    query = "SELECT id,username,password,member_type FROM users WHERE  username = %s"
    result = cursor.execute(query, (username,))
    if result:
        return cursor
    else:
        return False


def check_usermane(username):
    check_usermane_query = "SELECT username FROM users WHERE username = %s"
    cursor = mysql.connection.cursor()
    result = cursor.execute(check_usermane_query, (username,))
    return result


def check_usermane_id(username, id):
    check_usermane_query = "SELECT username FROM users WHERE username = %s AND id != %s"
    cursor = mysql.connection.cursor()
    result = cursor.execute(check_usermane_query,
                            (username, id))
    if result > 0:
        return True
