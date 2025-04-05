document.addEventListener('DOMContentLoaded', function () {
    const products = JSON.parse(document.getElementById('products-data').textContent);
    const imageContainer = document.getElementById('image-container');
    const mainImage = document.getElementById('main-product-image');

    products.forEach(product => {
        const ownerId = product.owner_id;
        const images = [];
        for (let i = 1; i <= 6; i++) {
            const picName = `pic_${i}`;
            if (product[picName]) {
                images.push(`uploads/${ownerId}/${product[picName]}`);
            }
        }
        if (images.length > 0) {
            let imageHtml = '';
            let i = 0;
            images.forEach(imageSrc => {
                imageHtml += `<div class="col-3"><img src="/static/${imageSrc}" class="img-thumbnail" alt="Thumbnail ${i++}" onerror="this.onerror=null;this.src='/static/images/not_found.png';"/></div>`;
            });
            imageContainer.innerHTML = imageHtml;

            // Mouse imleci üzerine gelince ana resmi değiştir
            imageContainer.querySelectorAll('img').forEach(img => {
                img.addEventListener('mouseover', function () {
                    mainImage.src = this.src.replace('/static/', '/static/');
                });
            });
        } else {
            imageContainer.innerHTML = '<p>Bu ürüne ait resim bulunmamaktadır.</p>';
        }
    });
  });