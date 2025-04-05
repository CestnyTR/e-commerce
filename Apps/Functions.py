import os
import time
import random
import re
from flask import flash, session, redirect, url_for
from werkzeug.utils import secure_filename


def unauthorized_operation():
    flash("Yetkisiz işlem.", "danger")
    session.clear()
    return redirect(url_for("profiles.login"))


def save_pictures(files, upload_folder, owner_id, category, title, color):
    """
    Resimleri belirtilen klasöre kaydeder ve yeniden adlandırır.

    Args:
        files: Yüklenecek dosyaların listesi.
        upload_folder: Ana yükleme klasörünün yolu.
        owner_id: Kullanıcı ID'si.

    Returns:
        Kaydedilen dosyaların listesi.
    """
    owner_folder = os.path.join(upload_folder, str(
        owner_id))  # Kullanıcı klasörünü oluştur

    if not os.path.exists(owner_folder):
        os.makedirs(owner_folder)  # Klasör yoksa oluştur

    saved_files = []
    max_files = 6  # Maksimum yükleme sınırı
    max_size = 3 * 1024 * 1024  # 3MB

    if len(files) > max_files:
        flash(f"En fazla {max_files} resim yükleyebilirsiniz!", "danger")
        return []
    new_title = clean_title(title)
    valid_file_count = 1  # Geçerli dosya sayısını takip et
    for file in files:
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[1].lower()  # Uzantıyı al

            # Dosya boyut kontrolü
            file.seek(0, os.SEEK_END)  # Dosyanın sonuna git
            file_size = file.tell()  # Dosya boyutunu öğren
            file.seek(0)  # Tekrar başa al

            if file_size > max_size:
                flash(
                    f"{filename} dosyası 3MB'den büyük, lütfen küçültün!", "danger")
                continue  # Büyük dosyayı geç
            # Yeni isimlendirme
            else:
                timestamp = int(time.time())
                random_number = random.randint(1000, 9999)
                new_filename = f"pictures_{valid_file_count}_{category}_{new_title}_{color}_{timestamp}_{random_number}.{ext}"
                filepath = os.path.join(owner_folder, new_filename)
                file.save(filepath)
                saved_files.append(new_filename)
                valid_file_count += 1

    return saved_files


def clean_title(title):
    """Başlıktaki özel karakterleri temizler ve güvenli hale getirir."""
    # Sadece harf, rakam, alt çizgi, tire ve boşluklara izin ver
    title = re.sub(r"[^\w\s-]", "", title)
    # Boşlukları alt çizgiyle değiştir
    title = title.replace(" ", "_")
    # Güvenli dosya adı oluştur
    title = secure_filename(title)
    return title


def sanitize_filename(filename):
    """Dosya adını güvenli hale getirir."""
    filename = re.sub(r"[^\w\s-]", "", filename)
    filename = filename.replace(" ", "_")
    return secure_filename(filename)


def generate_unique_filename(category, title, color, ext):
    """Benzersiz bir dosya adı oluşturur."""
    timestamp = int(time.time())
    random_number = random.randint(1000, 9999)
    return f"pictures_{category}_{title}_{color}_{timestamp}_{random_number}.{ext}"


def save_file(file, upload_folder, owner_id, category, title, color):
    """Tek bir dosyayı kaydeder ve yeni dosya adını döndürür."""
    if not file or file.filename == "":
        return None

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()
    file_size = len(file.read())  # Dosya boyutunu al
    file.seek(0)  # Dosya işaretçisini sıfırla

    if file_size > 3 * 1024 * 1024:
        flash(f"{filename} dosyası 3MB'den büyük, lütfen küçültün!", "danger")
        return None

    owner_folder = os.path.join(upload_folder, str(owner_id))
    # Klasörü oluştur veya varsa kullan
    os.makedirs(owner_folder, exist_ok=True)

    new_filename = generate_unique_filename(
        category, sanitize_filename(title), color, ext)

    filepath = os.path.join(owner_folder, new_filename)
    file.save(filepath)
    return new_filename


def delete_file(upload_folder, owner_id, filename):
    """Dosyayı siler."""
    try:
        file_path = os.path.join(upload_folder, str(owner_id), filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        pass


def shopping_cart_price(shopping_carts):
    total_price = 0
    if shopping_carts:
        for cart_item in shopping_carts:
            item_total = cart_item["price"] * cart_item["quantity"]
            cart_item["item_total"] = item_total
            total_price += item_total
        return total_price
    else:
        return total_price
