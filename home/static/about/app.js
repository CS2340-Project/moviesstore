const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        } else {
            entry.target.classList.remove("show");
        }
    });
});
const hidden = document.querySelectorAll(".hidden");
hidden.forEach((element) => observer.observe(element));
const loginContainer = document.getElementById("login-container");
function popUp() {
    loginContainer.style.display = "grid";
}
loginContainer.addEventListener("click", popUp);
function closeLogin() {
    loginContainer.style.display = "none";
}