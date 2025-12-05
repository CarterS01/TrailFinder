function fillMark(btn) {
    if (btn.src.endsWith("/static/images/bookmark.png")){
        btn.src = "/static/images/bookmark_filled.png";
        const id = btn.id;
        const data = { id: id, add: true }
        fetch('saveTrail', {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify(data)
        })
        alert('Trail saved')

    } else {
        btn.src = "/static/images/bookmark.png";
        const id = btn.id;
        const data = { id: id, add: false };
        fetch('saveTrail', {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify(data)
        })
        alert('Trail removed')
    }
}

function saveNotes(btn) {
    const trail = btn.id;
    const id = `${trail}_text`;
    const note = document.getElementById(id).value;
    const data = { id: trail, note: note }
    fetch('/saveNote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    alert('Note successfully saved!')
}

function deleteTrail(btn) {
    const id = btn.id
    const data = { id: id }
    fetch('/deleteSaved', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    alert('Trail removed from saved')
    location.reload()
}