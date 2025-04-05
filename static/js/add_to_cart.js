function addToCart(productId, quantity) {
    fetch(`/add_to_cart/${productId}?quantity=${quantity}`)
        .then(response => {
            if (response.ok) {
                console.log("Ürün sepete eklendi!"); // Kullanıcıya bildirim gösterilir
            } else {
                console.error("Hata oluştu");
            }
        })
        .catch(error => console.error("İstek hatası:", error));
}