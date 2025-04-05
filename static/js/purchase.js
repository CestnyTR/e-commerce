document.addEventListener('DOMContentLoaded', function() {
    const addressItems = document.querySelectorAll('.address-item');

    addressItems.forEach(item => {
        item.addEventListener('click', function() {
            // Tüm adres öğelerinden seçili sınıfını kaldır
            addressItems.forEach(otherItem => {
                otherItem.classList.remove('selected');
            });
            // Tıklanan adres öğesine seçili sınıfını ekle
            this.classList.add('selected');
            // Seçilen adresin ID'sini al (isteğe bağlı)
            const selectedAddressId = this.dataset.addressId;
            console.log('Seçilen Adres ID:', selectedAddressId);
            // Seçilen adresle ilgili başka işlemler yapabilirsiniz
        });
    });
});