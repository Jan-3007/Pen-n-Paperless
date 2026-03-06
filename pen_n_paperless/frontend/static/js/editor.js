



// Delegated handler for saving properties
// any element with class 'save-prop'
// supported data attributes 
// - data-category: defines the category of properties
// - data-key: defines the specific property in the category
// - data-value: defines the value to be set
async function requestEdit(event){

    const btn = event.target.closest && event.target.closest('.save-prop');
    if(!btn) return;
    event.preventDefault();

    // retrieve data attributes
    const category = btn.getAttribute('data-category');
    const key = btn.getAttribute('data-key');
    const value = btn.getAttribute('data-value');
    if(!category || !key || !value) return;

    const characterName = document.getElementById('character_name').value;

    console.debug(
        '[editor.js] requestEdit -> Server',
        {
            "character_name": characterName,
            "category": category,
            "key": key,
            "value": value
        }
    );

    // send the data
    try{
        let dataBody = {};
        dataBody[category] = {
            "key": key,
            "value": value,
        };

        const dataUpdate = await fetchWithFlashes(
            // use data-edit-character-url from the HTML template
            document.body.dataset.editCharacterUrl,
            {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify( dataBody )
            }
        );

        // process the returned data
        if(dataUpdate && typeof dataUpdate === 'object' && dataUpdate.status === 'success'){
            showToast('Saved','success');

            for (const [categ, data] of Object.entries(object)) {
                
                if(categ === Tribes.TRIBE) {
                    updateTribe(data['value']);

                } else if(categ === Professions.PROFESSION) {
                    updateProfession(data['value']);

                } else if(categ === Specializations.SPECIALIZATION) {
                    updateSpecialization(data['value']);

                } else {
                    console.debug(
                        '[editor.js] updating data on webpage failed',
                        {
                            "reason" : "unknown category key",
                            "category": categ,
                            "data": data
                        }
                    );
                }
            }

        }else{
            showToast('Save failed','error');
        }

    } catch(e){
        console.debug(
            '[editor.js] fetchWithFlashes failed',
            {
                "exception": e
            }
        );
        showToast('Network error', 'error')
    }

};

// register the edit function to be called whenever the user performs a click
document.addEventListener('click', requestEdit, false);


// UI update helpers
window.updateTribe = function(value) {
    const dropbtn = document.getElementById('dropbtn-tribe');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateProfession = function(value) {
    const dropbtn = document.getElementById('dropbtn-profession');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateSpecialization = function(value)  {
    const dropbtn = document.getElementById('dropbtn-specialization');
    if(dropbtn) dropbtn.textContent = value;
};



