document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".dropdown-toggle");
    const dropdown = document.querySelector(".dropdown");

    menuToggle.addEventListener("click", function (event) {
        event.stopPropagation();
        dropdown.classList.toggle("active");
    });

    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove("active");
        }
    });
});