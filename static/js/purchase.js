document.addEventListener("DOMContentLoaded", function () {
  const steps = document.querySelectorAll(".step-horizontal");
  const contents = document.querySelectorAll(".step-content");
  let currentStep = 1;

  function updateSteps() {
    steps.forEach((step, index) => {
      if (index < currentStep - 1) {
        step.classList.add("complete");
        step.classList.remove("active");
      } else if (index === currentStep - 1) {
        step.classList.add("active");
        step.classList.remove("complete");
      } else {
        step.classList.remove("active", "complete");
      }
    });

    contents.forEach(content => {
      content.style.display = content.getAttribute("data-step") == currentStep ? "block" : "none";
    });

    if (currentStep === 4) {
      const selectedRadio = document.querySelector('input[name="selected_address"]:checked');
      const summary = document.getElementById("selected-address-summary");
      if (selectedRadio && summary) {
        summary.textContent = selectedRadio.value;
      } else {
        summary.textContent = "Herhangi bir adres seçilmedi.";
      }
    }
  }

  document.getElementById("prevBtn").addEventListener("click", function () {
    if (currentStep > 1) {
      currentStep--;
      updateSteps();
    }
  });

  document.getElementById("nextBtn").addEventListener("click", function () {
    // 2. adımda adres seçilmemişse geçişi engelle
    if (currentStep === 2) {
      const selected = document.querySelector("input[name='selected_address']:checked");
      if (!selected) {
        alert("Lütfen bir adres seçin.");
        return; // geçişi engelle
      }}
    
    if (currentStep < steps.length) {
      currentStep++;
      updateSteps();
    }
  });

  updateSteps();
});
