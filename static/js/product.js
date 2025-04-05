const priceRange = document.getElementById("price-range");
const minPrice = document.getElementById("min-price");
const maxPrice = document.getElementById("max-price");

// Fiyat aralığı değeri değiştiğinde, en düşük ve en yüksek fiyatı güncelle
priceRange.addEventListener("input", function () {
    const value = priceRange.value;
    minPrice.textContent = value < 0 ? "0" : value;
    maxPrice.textContent = value > 5000 ? "5000" : value;
});