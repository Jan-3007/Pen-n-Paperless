
// Notes to self on JavaScript
// - use async functions to communicate with Python backend
// - use window functions (global functions) for updating data on the webpage


// Notes
async function saveNotes(){
    const key = Generic.NOTES;
    const content = document.getElementById('notes').value;
    const characterName = document.getElementById('character_name').value;

    console.debug(
        '[character.js] saveNotes -> Server', 
        { 
            "character_name": characterName,
            "key": key,
            "notes length": content ? content.length : 0, 
            "notes content": content ? content : ""
        }
    );

    try{
        let dataBody = {};
        dataBody[key] = content;

        const dataUpdate = await fetchWithFlashes(
            // use data-edit-character-url from the HTML template
            document.body.dataset.editCharacterUrl,
            {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify( dataBody )
            }
        );

        console.debug(
            '[character.js] Server -> saveNotes', 
            { 
                "data": dataUpdate
            }
        );

        if(dataUpdate && typeof dataUpdate === 'object' && dataUpdate.status === 'success'){
            showToast('Saved','success');
            // no need to update the webpage, input field stores latest data
        }else{
            showToast('Save failed','error');
        }
    }catch(e){
        console.debug(
            '[character.js] fetchWithFlashes failed', 
            { 
                "exception": e
            }
        );
        showToast('Network error', 'error');
    }
};











