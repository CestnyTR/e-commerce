document.addEventListener("DOMContentLoaded", function () {
    const oldPasswordInput = document.getElementById("old_password");
    const newPasswordContainer = document.getElementById("new-password-container");

    oldPasswordInput.addEventListener("input", function () {
        if (oldPasswordInput.value.trim() !== "") {
            newPasswordContainer.style.display = "block";
        } else {
            newPasswordContainer.style.display = "none";
        }
    });
});