function setQuotes(data) {
    if (data) {
        document.getElementById("quotes-text").innerHTML = data.content;
        document.getElementById("author-name").innerHTML = data.author;
    } else {
        document.getElementById("quotes-text").innerHTML = "Our greatest glory is not in never falling, but in rising every time we fall.";
        document.getElementById("author-name").innerHTML = "Confucius";
    }
};
setQuotes();

setInterval(() => {
    fetch('https://api.quotable.io/random')
        .then((res) => {
            res.json()
                .then(data => {
                    setQuotes(data);
                });
        })
}, 10000)

