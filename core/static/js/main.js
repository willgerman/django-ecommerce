// #region mobile_header_nav
const nav_toggles = document.querySelectorAll("[aria-controls='#primary-nav']");
console.log(nav_toggles);

nav_toggles.forEach(toggle => {
    toggle.addEventListener("click", (e) => {
        menu = document.querySelector(toggle.getAttribute('aria-controls'));

        nav_status = menu.getAttribute("aria-expanded");

        if (nav_status == "false") {
            menu.setAttribute("aria-expanded", "true");
        } else (
            menu.setAttribute("aria-expanded", "false")
        )
    });
});
// #endregion

// #region dropdowns
document.addEventListener("DOMContentLoaded", () => {

    const dropdownToggles = document.querySelectorAll(".dropdown_toggle");

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener("click", (event) => {
            console.log("Dropdown toggle clicked");
            event.preventDefault();
            event.stopPropagation();

            const dropdownMenu = toggle.nextElementSibling;

            dropdownMenu.classList.toggle("open");

            document.querySelectorAll(".dropdown_menu").forEach(menu => {
                if (menu !== dropdownMenu) {
                    menu.classList.remove("open");
                }
            });
        });
    });

    document.addEventListener("click", () => {
        document.querySelectorAll(".dropdown_menu").forEach(menu => {
            menu.classList.remove("open");
        });
    });
});
// #endregion