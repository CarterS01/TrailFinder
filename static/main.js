function fillMark() {
    if (document.getElementById("bookmark").src.endsWith("/static/images/bookmark.png")){
        document.getElementById("bookmark").src = "/static/images/bookmark_filled.png";
    } else {
        document.getElementById("bookmark").src = "/static/images/bookmark.png";
    }
}

function saveNotes(btn) {
    const trail = btn.id;
    const id = `${trail}_text`;
    const note = document.getElementById(id).value;
    const data = { id: trail, note: note }
    fetch('/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    alert('Note successfully saved!')
}