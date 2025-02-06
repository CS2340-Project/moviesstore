const search = document.querySelector(".search");
const movieNodes = document.querySelectorAll(".movie-node");
const movies = Array.from(movieNodes).map((node, index) => {
    return { name: node.dataset.name.toLowerCase(), element: node };
});
const popular = document.querySelector(".popular");

search.addEventListener("input", () => {
    popular.style.animation = "fade .2s ease-out forwards"
     setTimeout(() => {
        popular.style.display = "none";
    }, 200)
    let searching = search.value.toLowerCase().trim()
    const rankedMovies = movies.map(movie => {
        let score = 0;
        if (movie.name.startsWith(searching)) {
            score += 1;
        }
        if (movie.name.includes(searching)) {
            score += .5;
        }
        return {...movie,score};
    }).sort((a,b) => b.score - a.score);
   const child = document.querySelector(".child");
   child.innerHTML = "";
   rankedMovies.forEach((movie, i) => {
       movie.element.classList.add("added")
       child.appendChild(movie.element);
   });
});
const branches = document.querySelectorAll(".branch")
if (movies.length === 0) {
    for (let branch of branches) {
        branch.style.display = "none"
    }
}
search.addEventListener("blur", () =>{
    search.classList.add("unfocused");
    popular.style.animation = "fade .2s ease-out forwards"
    popular.style.animation = "smooth-compress .2s ease-out forwards"
     setTimeout(() => {
        popular.style.display = "none";
    }, 200)
    popular.style.right = "0"
});
search.addEventListener("focus", () =>{
    search.classList.remove("unfocused");
     setTimeout(() => {
        popular.style.display = "grid";
    }, 5);
    popular.style.animation = "materialize .2s ease-in forwards"
    popular.style.animation = "smooth-widen forwards .2s ease-in"
    popular.style.right = "4vh"


});