import wtforms
#! user class

class RegisterForm(wtforms.Form):
    name = wtforms.StringField("İsim", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=5, max=12, message="Girilen isim 5 ile 12 harf arasında olmalıdır.")])
    surname = wtforms.StringField("Soyad", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=5, max=12, message="Girilen soyisim 5 ile 12 harf arasında olmalıdır.")])
    username = wtforms.StringField("Kullanıcı adı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=5, max=12, message="Girilen kullanıcı adı 5 ile 12 harf arasında olmalıdır.")])
    email = wtforms.StringField("E-Mail", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Email(
            message="Lütfen geçerli bir E-Mail hesabı giriniz."),
        wtforms.validators.Length(min=5, max=30, message="Girilen mail 5 ile 30 harf arasında olmalıdır.")])
    password = wtforms.PasswordField("Kullanıcı Şifresi", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(
            min=8, max=15, message="Girilen şifre 8 ile 15 karakter arasında olmalıdır."),
        wtforms.validators.Regexp(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&-_])[A-Za-z\d@$!%*?&-_]+$',
            message="Şifre en az bir büyük harf, bir küçük harf, bir sayı ve bir özel karakter içermelidir.")])
    confirm = wtforms.PasswordField('Şifreyi Tekrar Girin', validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(
            min=8, max=15, message="Girilen şifre 8 ile 15 karakter arasında olmalıdır."),
        wtforms.validators.EqualTo('password', message='Şifreler eşleşmiyor!')])
    birth_date = wtforms.DateField("Doğum Tarihi", validators=[
        wtforms.validators.DataRequired()])
    member_type = wtforms.RadioField("Üyelik amacınız:", choices=[
        ("buyer", "Alıcı"), ("seller", "Satıcı")],
        default="buyer",
        render_kw={"class": "radio-field"},
        validators=[wtforms.validators.DataRequired()])
    address_title = wtforms.StringField("Adres Başlığı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=2, max=12, message="Girilen isim 2 ile 20 harf arasında olmalıdır.")])
    city = wtforms.SelectField(u"Şehir", coerce=int, choices=[])
    district = wtforms.SelectField(u"İlçe", coerce=int, choices=[])
    street = wtforms.SelectField(u"Sokak", coerce=int, choices=[])
    neighborhood = wtforms.SelectField(u"Mahalle", coerce=int, choices=[])
    address = wtforms.TextAreaField(
        "Adress", validators=[
            wtforms.validators.data_required(),
            wtforms.validators.Length(min=5, max=100, message="aderes en az 5 en fazla 100 karekter olabilir.")])


class UpdateUserForm(wtforms.Form):
    name = wtforms.StringField("İsim", validators=[
        wtforms.validators.Length(min=5, max=12, message="Girilen isim 5 ile 12 harf arasında olmalıdır.")])
    surname = wtforms.StringField("Soyad", validators=[
        wtforms.validators.Length(min=5, max=12, message="Girilen soyisim 5 ile 12 harf arasında olmalıdır.")])
    username = wtforms.StringField("Kullanıcı adı", validators=[
        wtforms.validators.Length(min=5, max=12, message="Girilen kullanıcı adı 5 ile 12 harf arasında olmalıdır.")])
    email = wtforms.StringField("E-Mail", validators=[
        wtforms.validators.Email(
            message="Lütfen geçerli bir E-Mail hesabı giriniz."),
        wtforms.validators.Length(min=5, max=30, message="Girilen mail 5 ile 30 harf arasında olmalıdır.")])
    old_password = wtforms.PasswordField('Eski şifrenizi giriniz', validators=[
        wtforms.validators.Optional()  # Opsiyonel hale getirir
    ])
    password = wtforms.PasswordField("Kullanıcı Şifresi", validators=[wtforms.validators.Optional(),
                                                                      wtforms.validators.Length(
        min=8, max=15, message="Girilen şifre 8 ile 15 karakter arasında olmalıdır."),
        wtforms.validators.Regexp(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&-_])[A-Za-z\d@$!%*?&-_]+$',
            message="Şifre en az bir büyük harf, bir küçük harf, bir sayı ve bir özel karakter içermelidir.")])
    confirm = wtforms.PasswordField('Şifreyi Tekrar Girin', validators=[wtforms.validators.Optional(),
                                                                        wtforms.validators.Length(
        min=8, max=15, message="Girilen şifre 8 ile 15 karakter arasında olmalıdır."),
        wtforms.validators.EqualTo('password', message='Şifreler eşleşmiyor!')])
    address_title = wtforms.StringField("Adres Başlığı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=2, max=12, message="Girilen isim 2 ile 20 harf arasında olmalıdır.")])
    city = wtforms.SelectField(u"Şehir", coerce=int, choices=[])
    district = wtforms.SelectField(u"İlçe", coerce=int, choices=[])
    street = wtforms.SelectField(u"Sokak", coerce=int, choices=[])
    neighborhood = wtforms.SelectField(u"Mahalle", coerce=int, choices=[])
    address = wtforms.TextAreaField(
        "Adress", validators=[
            wtforms.validators.data_required(),
            wtforms.validators.Length(min=5, max=100, message="aderes en az 5 en fazla 100 karekter olabilir.")])


class LoginForm(wtforms.Form):
    username = wtforms.StringField("Kullanıcı adı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=5, max=12, message="Girilen kullanıcı adı 5 ile 12 harf arasında olmalıdır.")])
    password = wtforms.PasswordField("Parola", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=8, max=15, message="Girilen şifre 8 ile 15 karakter arasında olmalıdır.")])


class ProductForm(wtforms.Form):
    title = wtforms.StringField(
        "Ürün adı", validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(max=50, min=5, message="Ürün adı 5 ile 50 karekter arasında olmalıdır.")])
    category = wtforms.SelectField(u"Ürün kateforisi", coerce=int)
    stock = wtforms.IntegerField(
        "Stok miktarı", validators=[
            wtforms.validators.DataRequired()])
    active = wtforms.BooleanField("Ürün satışa")
    content = wtforms.TextAreaField(
        "Ürün içeriği", validators=[
            wtforms.validators.data_required(),
            wtforms.validators.Length(min=8, max=10000, message="ürün içeriği 8 ile 10.000 karekter arasında olmalı")])
    color = wtforms.SelectField(u"Ürün Rengi", coerce=int)
    price = wtforms.DecimalField("Ürün Fiyatı")
    pictures = wtforms.MultipleFileField(
        'Image File', validators=[])


class AddressForm(wtforms.Form):
    address_title = wtforms.StringField("Adres Başlığı", validators=[
        wtforms.validators.DataRequired(),
        wtforms.validators.Length(min=2, max=12, message="Girilen isim 2 ile 20 harf arasında olmalıdır.")])
    city = wtforms.SelectField(u"Şehir", coerce=int, choices=[])
    district = wtforms.SelectField(u"İlçe", coerce=int, choices=[])
    street = wtforms.SelectField(u"Sokak", coerce=int, choices=[])
    neighborhood = wtforms.SelectField(u"Mahalle", coerce=int, choices=[])
    address = wtforms.TextAreaField(
        "Adress", validators=[
            wtforms.validators.data_required(),
            wtforms.validators.Length(min=5, max=100, message="aderes en az 5 en fazla 100 karekter olabilir.")])

