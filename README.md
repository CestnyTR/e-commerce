# cestnytr — Flask E-Ticaret Uygulaması

Flask, MariaDB/MySQL ve Bootstrap ile geliştirilmiş çok rollü (alıcı / satıcı / admin) bir e-ticaret uygulaması. Ürün listeleme ve filtreleme, sepet, satın alma, kullanıcı ve adres yönetimini içerir.

## Özellikler

- **Ürünler** — kategori, renk ve fiyat aralığına göre filtreleme, ürün detay sayfası
- **Satıcı işlemleri** — resim yüklemeli ürün ekleme, güncelleme ve silme
- **Sepet** — sepete ekleme, adet artırma/azaltma, çıkarma ve satın alma
- **Kullanıcılar** — kayıt, giriş/çıkış, profil güncelleme (`passlib` ile hash'li parolalar)
- **Adres yönetimi** — il → ilçe → mahalle bağımlı (cascading) seçim ile adres ekle/güncelle/sil
- **Roller** — `admin`, `buyer`, `seller` (satıcı) için ayrı profil görünümleri
- Blueprint'lerle modüler yapı: `Main`, `Product`, `Purchase`, `Profiles`

## Teknolojiler

- Python 3 + Flask
- flask_mysqldb (PyMySQL shim üzerinden — derleme gerektiren `mysqlclient` yerine)
- MariaDB / MySQL
- WTForms, passlib, Werkzeug, email_validator
- Bootstrap, vanilla JS (statik dosyalar)

## Proje Yapısı

```
app.py                    # Uygulama fabrikası (create_app) ve giriş noktası
config.py                 # Yapılandırma (DB, SECRET_KEY, upload klasörü)
extensions.py             # PyMySQL shim + MySQL nesnesi
Apps/
  Main.py                 # Ana sayfa, hakkımızda, SSS
  Product.py              # Ürün listeleme/ekleme/güncelleme/silme
  Purchase.py             # Sepet ve satın alma
  Profiles.py             # Kayıt, giriş, profil, adres
  Forms.py                # WTForms form tanımları
  Functions.py            # Resim/dosya kaydetme, yardımcılar
  MySQL_connettions.py    # Tüm veritabanı sorguları
templates/                # Jinja2 şablonları
static/                   # css, js, images, uploads
cestnytr_ecommerce.sql    # Veritabanı dump'ı
```

## Kurulum

### 1. Sanal ortam ve bağımlılıklar

```bash
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install flask wtforms passlib werkzeug email_validator pymysql
pip install --no-deps flask_mysqldb
```

> **Not:** `flask_mysqldb` normalde derleme gerektiren `mysqlclient`'a bağlıdır.
> Bunu atlamak için `--no-deps` ile kuruyoruz; `extensions.py` içindeki
> `pymysql.install_as_MySQLdb()` shim'i sayesinde PyMySQL sürücü olarak devreye
> girer. **Bu satırı silmeyin.**

### 2. Veritabanı

MariaDB/MySQL üzerinde `cestnytr_ecommerce` veritabanını oluşturup dump'ı içe aktarın:

```bash
mysql -u root -e "CREATE DATABASE cestnytr_ecommerce;"
mysql -u root cestnytr_ecommerce < cestnytr_ecommerce.sql
```

Bağlantı bilgileri [config.py](config.py) içindedir (varsayılan: `localhost`, kullanıcı `root`, boş parola). Ortamınıza göre düzenleyin.

### 3. Çalıştırma

```bash
python app.py
```

Ya da:

```bash
flask --app app.py --debug run
```

Uygulama http://127.0.0.1:5000 adresinde çalışır.

## Yapılandırma

`config.py` içindeki `Config` sınıfı:

| Anahtar | Açıklama |
|---|---|
| `SECRET_KEY` | Oturum imzalama anahtarı |
| `MYSQL_HOST` / `MYSQL_USER` / `MYSQL_PASSWORD` / `MYSQL_DB` | Veritabanı bağlantısı |
| `MYSQL_CURSORCLASS` | `DictCursor` (sorgular sözlük döndürür) |
| `UPLOAD_FOLDER` | Yüklenen ürün resimlerinin kaydedildiği klasör (`static/uploads`) |
