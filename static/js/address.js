document.addEventListener("DOMContentLoaded", function () {
    let citySelect = document.getElementById("city");
    let districtSelect = document.getElementById("district");
    let streetSelect = document.getElementById("street");
    let neighborhoodSelect = document.getElementById("neighborhood");

    function updateOptions(selectElement, data) {
        selectElement.innerHTML = '<option value="">Seçiniz</option>';
        data.forEach(item => {
            let option = document.createElement("option");
            option.value = item[0];
            option.textContent = item[1];
            selectElement.appendChild(option);
        });
    }

    citySelect.addEventListener("change", function () {
        let city_id = this.value;
        fetch(`/get_districts/${city_id}`)
            .then(response => response.json())
            .then(data => {
                updateOptions(districtSelect, data);
                updateOptions(streetSelect, []);
                updateOptions(neighborhoodSelect, []);
            });
    });

    districtSelect.addEventListener("change", function () {
        let district_id = this.value;
        fetch(`/get_streets/${district_id}`)
            .then(response => response.json())
            .then(data => {
                updateOptions(streetSelect, data);
                updateOptions(neighborhoodSelect, []);
            });
    });

    streetSelect.addEventListener("change", function () {
        let street_id = this.value;
        fetch(`/get_neighborhoods/${street_id}`)
            .then(response => response.json())
            .then(data => {
                updateOptions(neighborhoodSelect, data);
            });
    });
});