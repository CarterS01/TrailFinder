function fillMark() {
    console.log('linked')
    if (document.getElementById("bookmark").src == "/static/images/bookmark.png"){
        console.log('True')
        document.getElementById("bookmark").src = "/static/images/bookmark_filled.png";
    } 
    else {
        document.getElementById("bookmark").src = "/static/images/bookmark.png";
        console.log('False')
    }
}