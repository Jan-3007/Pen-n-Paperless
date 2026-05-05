



// Delegated handler for saving properties
// any element with class 'save-prop'
// supported data attributes 
// - data-category: defines the category of properties
// - data-key: defines the specific property in the category
// - data-value: defines the value to be set
async function editProperty(event){

    const btn = event.target.closest && event.target.closest('.save-prop');
    if(!btn) return;
    event.preventDefault();

    // retrieve data attributes
    const category = btn.getAttribute('data-category');
    const key = btn.getAttribute('data-key');
    const valueStr = btn.getAttribute('data-value');
    if(!category || !key || !valueStr) return;

    const value = parseInt(valueStr)

    const characterName = document.getElementById('character_name').innerHTML;

    console.debug(
        '[editor.js] editProperty -> Server',
        {
            "character_name": characterName,
            "category": category,
            "key": key,
            "value": value
        }
    );

    let dataBody = {};
    dataBody[category] = {};
    dataBody[category][key] = value;

    await requestEdit(dataBody);
};

// register the edit function to be called whenever the user performs a click
document.addEventListener('DOMContentLoaded', function() {
    const collection = document.getElementsByClassName('save-prop');
    for (let i = 0; i < collection.length; i++) {
        collection[i].addEventListener('click', editProperty, false);
    }
});


async function addHistoryEntry(event){

    const btn = event.target.closest && event.target.closest('.history');
    if(!btn) return;
    event.preventDefault();

    const category = btn.getAttribute('data-category');
    const description = document.getElementById('add-entry-desc-' + [category]).value;
    const valueStr = document.getElementById('add-entry-value-' + [category]).value;

    if(valueStr === '' || description === '') {
        showToast('Incomplete input','warning');
        return;
    }

    const value = parseInt(valueStr)

    const characterName = document.getElementById('character_name').innerHTML;

    console.debug(
        '[editor.js] addHistoryEntry -> Server',
        {
            "character_name": characterName,
            "category": category,
            "description": description,
            "value": value
        }
    );

    let dataBody = {};
    dataBody[category] = {};
    dataBody[category][Generic.DESCRIPTION] = description;
    dataBody[category][Generic.VALUE] = value;

    await requestEdit(dataBody);
}

async function removeHistoryEntry(event){

    const btn = event.target.closest && event.target.closest('.history');
    if(!btn) return;
    event.preventDefault();

    const category = btn.getAttribute('data-category');
    const idStr = btn.getAttribute('data-value');

    if(idStr === '') {
        showToast('Internal error','error');
        console.error(
            '[editor.js] removeHistoryEntry: Fetching the entry ID resulted in empty string.'
        )
        return;
    }

    const id = parseInt(idStr)

    const characterName = document.getElementById('character_name').innerHTML;

    console.debug(
        '[editor.js] removeHistoryEntry -> Server',
        {
            "character_name": characterName,
            "category": category,
            "entry id": id
        }
    );

    let dataBody = {};
    dataBody[category] = {};
    dataBody[category][History.ENTRY_NUMBER] = id;

    await requestEdit(dataBody);
}

// register the history edit functions to be called whenever the user performs a click
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-hp-history-entry').addEventListener('click', addHistoryEntry, false);
    document.getElementById('add-xp-history-entry').addEventListener('click', addHistoryEntry, false);

    const collection = document.getElementsByClassName('remove-entry');
    for (let i = 0; i < collection.length; i++) {
        collection[i].addEventListener('click', removeHistoryEntry, false);
    }

});

// ---
// for armour and weapons

async function selectEquipment(event){

    const btn = event.target.closest && event.target.closest('.dropdown-element');
    if(!btn) return;
    event.preventDefault();

    const category = btn.getAttribute('data-category');
    const key = btn.getAttribute('data-key');
    const value = btn.getAttribute('data-value');
    const idx = event.target.parentNode.parentNode.getAttribute('id').split('-')[1];

    const characterName = document.getElementById('character_name').innerHTML;

        console.debug(
        '[editor.js] removeHistoryEntry -> Server',
        {
            "character_name": characterName,
            "category": category,
            "key": key,
            "value": value,
            "index": idx
        }
    );

    let dataBody = {};
    dataBody[category] = {};
    dataBody[category][key] = value;
    dataBody[category][Generic.ID] = idx;

    await requestEdit(dataBody);
}

// register the equipment select function to be called whenever the user performs a click
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('equipment-dropdown-element').addEventListener('click', selectEquipment, false);
});




// ---
// send edit request and process response

async function requestEdit(dataBody){
    // send the data
    try{
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
            // remove 'status' property
            const { status, ...newData } = dataUpdate

            for (const [categ, data] of Object.entries(newData)) {
                
                if(categ === Tribes.TRIBE) {
                    updateTribe(data);

                } else if(categ === Professions.PROFESSION) {
                    updateProfession(data);

                } else if(categ === Specializations.SPECIALIZATION) {
                    updateSpecialization(data);

                } else if(categ === Attributes.ATTRIBUTE) {
                    updateAttribute(data); 

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
        } else if(dataUpdate && typeof dataUpdate === 'object' && dataUpdate.status === 'warning'){
            console.debug(
                '[editor.js] received warning',
                {
                    "data": dataUpdate
                }
            );

        }else{
            console.debug(
                '[editor.js] received error',
                {
                    "data": dataUpdate
                }
            );

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

// UI update helpers
window.updateTribe = function(data) {
    const value = Object.values(data)[0];

    const dropbtn = document.getElementById('dropbtn-tribe');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateProfession = function(data) {
    const value = data[Professions.PROFESSION]

    const dropbtn = document.getElementById('dropbtn-profession');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateSpecialization = function(data)  {
    const value = data[Specializations.SPECIALIZATION]

    const dropbtn = document.getElementById('dropbtn-specialization');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateAttribute = function(data) {
    // one attribute, one attribute bonus and the remaining points
    for (const [key, value] of Object.entries(data)) {
        const el = document.getElementById('attr-' + key);
        if(el) el.textContent = value;
    }
}

