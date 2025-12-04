function fillMark() {
    if (document.getElementById("bookmark").src.endsWith("/static/images/bookmark.png")){
        document.getElementById("bookmark").src = "/static/images/bookmark_filled.png";
    } else {
        document.getElementById("bookmark").src = "/static/images/bookmark.png";
    }
}

function test(btn) {
    alert(document.getElementById('test').class);
}