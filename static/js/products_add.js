window.onload = function () {
    document.getElementById("pictures").value = "";
};
document.addEventListener("DOMContentLoaded", function () {
    const picturesInput = document.getElementById("pictures");
    const preview = document.getElementById("image-preview");
    let selectedFiles = [];


    picturesInput.addEventListener("change", function (event) {
        const files = event.target.files;
        selectedFiles = []; // Seçilen dosyaları da sıfırla
        preview.innerText = "";

        for (let i = 0; i < files.length; i++) {
            selectedFiles.push(files[i]);
        }
        updatePreview();
    });

    function updatePreview() {
        preview.innerHTML = "";
        selectedFiles.forEach(function (file, index) {
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
                label.textContent = `Resim ${index + 1}`;
                label.classList.add("image-label");
                const orderInput = document.createElement("input"); // Gizli input
                orderInput.type = "hidden";
                orderInput.name = "picture_order"; // Input adı
                orderInput.value = index; // Sıra numarası
                imageContainer.appendChild(img);
                imageContainer.appendChild(label);
                imageContainer.appendChild(orderInput); // Gizli input ekle
                imageContainer.appendChild(deleteButton);
                preview.appendChild(imageContainer);
            };
            reader.readAsDataURL(file);
        });

        Sortable.create(preview, {
            animation: 150,
            onUpdate: function (evt) {
                updateLabels();
            },
        });
    }

    function updateLabels() {
        const labels = document.querySelectorAll(".image-label");
        labels.forEach((label, index) => {
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

    // Form gönderilmeden önce dosyaları FormData'ya ekle
    document.querySelector("form").addEventListener("submit", function (event) {
        const formData = new FormData(this);
        selectedFiles.forEach((file, index) => {
            const ext = file.name.split(".").pop(); // Dosya uzantısı
            const newFilename = `picture_${index + 1}.${ext}`; // Yeni dosya adı
            formData.append("pictures", new File([file], newFilename));
        });


        // FormData'yı backend'e gönder
        fetch(this.action, {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                if (response.ok) {
                    window.location.href = "/profile"; // Başarılıysa profile yönlendir
                } else {
                    alert("Ürün ekleme başarısız oldu.");
                }
            })
            .catch((error) => {
                console.error("Hata:", error);
            });
        event.preventDefault(); // Formun normal gönderimini engelle
    });
});