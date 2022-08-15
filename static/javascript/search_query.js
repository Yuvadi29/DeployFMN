function searchQuery(search_query_value) {
    
    let search_query = document.getElementById(search_query_value).value;
    

    if(search_query != '') {
        window.open("/searchPage/1/"+search_query, "_self")
    }
}
function triggerEnter(search_query_value){
    if (event.keyCode == 13) {
        searchQuery(search_query_value)
    }
}