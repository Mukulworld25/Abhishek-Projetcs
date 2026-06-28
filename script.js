
function toggleMenu() {
    const menu = document.getElementById("mobileMenu");
    const hamburger = document.getElementById("hamburger");
    if(menu) menu.classList.toggle("open");
}

window.addEventListener("scroll", () => {
    const nav = document.getElementById("mainNav");
    if (nav) {
        if (window.scrollY > 10) {
            nav.classList.add("scrolled");
        } else {
            nav.classList.remove("scrolled");
        }
    }
});
