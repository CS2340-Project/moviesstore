const search = document.getElementById("search");
const movieNodes = document.querySelectorAll(".movie-node");
const movies = Array.from(movieNodes).map((node, index) => {
    return { name: node.dataset.name.toLowerCase(), element: node };
});
search.addEventListener("input", () => {
   searching = search.value.toLowerCase().trim()
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
