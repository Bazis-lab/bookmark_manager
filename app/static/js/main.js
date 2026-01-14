document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form[data-confirm]");

  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const msg = form.getAttribute("data-confirm") || "Подтвердить действие?";
      if (!confirm(msg)) e.preventDefault();
    });
  });
});