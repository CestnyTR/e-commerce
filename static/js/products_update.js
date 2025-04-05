window.onload = function () {
    document.getElementById("pictures").value = "";
};
document.addEventListener("DOMContentLoaded", function () {
    const picturesInput = document.getElementById("pictures");
    const preview = document.getElementById("image-preview");
    const fileInput = document.getElementById("pictures");
    const form = document.querySelector("form");


    var oldImageCount = 0
    let selectedFiles = [];
    preview.innerHTML = "";
    loadOldImage()
    picturesInput.addEventListener("change", function (event) {
        const files = event.target.files;
        for (let i = 0; i < files.length; i++) {
            selectedFiles.push(files[i]);
        }
        updatePreview();
    });

    function loadOldImage() {
        const picturesData = document.getElementById('pictures-data').textContent;
        const ownerIdData = document.getElementById('owner_id-data').textContent;

        if (!picturesData || !ownerIdData) {
            console.error("Resim verileri eksik.");
            return;
        }

        let products = JSON.parse(picturesData); // Eski resimler
        const owner_id = JSON.parse(ownerIdData); // Sahip ID

        products.forEach(function (product, index) {
            updateLabels()
            if (product != null) {
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("image-container");
                imageContainer.classList.add("old-image");

                const img = document.createElement("img");
                img.src = `/static/uploads/${owner_id}/${product}`;
                img.classList.add("preview-image");

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "X";
                deleteButton.classList.add("delete-button");
                deleteButton.addEventListener("click", function () {
                    products = products.filter((item, idx) => idx !== index && item !== null);
                    imageContainer.remove();
                });

                const label = document.createElement("span");
                const productName = product.split("_");
                label.textContent = `${productName[0]} ${productName[1]}`;
                label.classList.add("image-label");

                const oldImageInput = document.createElement("input");
                oldImageInput.type = "hidden";
                oldImageInput.name = "old-image[]";
                oldImageInput.value = product;

                const orderInput = document.createElement("input"); // Gizli input
                orderInput.type = "hidden";
                orderInput.name = "picture_order"; // Input adı
                orderInput.value = index; // Sıra numarası
                imageContainer.appendChild(img);
                imageContainer.appendChild(label);
                imageContainer.appendChild(oldImageInput);
                imageContainer.appendChild(orderInput);
                imageContainer.appendChild(deleteButton);
                preview.appendChild(imageContainer);
                oldImageCount += 1
            }
        });
        updatePreview();
    }
    function updatePreview() {
        document.querySelectorAll(".image-container:not(.old-image)").forEach((img) => img.remove());
        selectedFiles.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imageContainer = document.createElement("div");
                imageContainer.classList.add("image-container");

                const img = document.createElement("img");
                img.src = e.target.result;
                img.classList.add("preview-image");

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "X";
                deleteButton.classList.add("delete-button");
                deleteButton.addEventListener("click", function () {
                    selectedFiles.splice(index, 1);
                    updatePreview();
                    updateFileInput();
                });

                const label = document.createElement("span");
                label.textContent = `Yeni Resim ${index + 1}`;
                label.classList.add("image-label");

                const newImageInput = document.createElement("input");
                newImageInput.type = "hidden";
                newImageInput.name = "new_pictures_order[]";
                newImageInput.value = file;
                const orderInput = document.createElement("input"); // Gizli input
                orderInput.type = "hidden";
                orderInput.name = "picture_order"; // Input adı
                orderInput.value = index + oldImageCount; // Sıra numarası
                imageContainer.appendChild(img);
                imageContainer.appendChild(label);
                imageContainer.appendChild(newImageInput);
                imageContainer.appendChild(orderInput);
                imageContainer.appendChild(deleteButton);
                preview.appendChild(imageContainer);
            };
            reader.readAsDataURL(file);
        });

        Sortable.create(preview, {
            animation: 150,
            onUpdate: updateLabels,
        });
    }

    function updateLabels() {
        document.querySelectorAll(".image-label").forEach((label, index) => {
            label.textContent = `Resim ${index + 1}`;
        });
    }

    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        selectedFiles.forEach((file) => dataTransfer.items.add(file));
        picturesInput.files = dataTransfer.files;
    }
    picturesInput.addEventListener("change", function (event) {
        selectedFiles = [...event.target.files];
    });
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(form);

        selectedFiles.forEach((file) => {
            formData.append("new_pictures[]", file);
        });

        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        fetch(form.action, {
            method: "POST",
            body: formData,
        })
            .then((response) => response.text())
            .then((data) => {
                console.log("Server yanıtı:", data);
                if (response.ok) {
                    window.location.href = "/profile";
                } else {
                    alert("Ürün güncelleme başarısız oldu.");
                }
            })
            .catch((error) => console.error("Hata:", error));
    });
});