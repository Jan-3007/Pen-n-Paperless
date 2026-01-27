// Editor page JavaScript: delegated handlers and avatar upload/delete
// Depends on fetchWithFlashes and showToast being available (toast.js)

// Dropdown helper exposed globally
window.onDropdownSelect = function(list_name){
    const el = document.getElementById("listDropdown-" + list_name);
    if(el) el.classList.toggle("show");
};

window.closeDropdown = function(){
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for(var i = 0; i < dropdowns.length; i++){
        var openDropdown = dropdowns[i];
        if(openDropdown.classList.contains('show')){
            openDropdown.classList.remove('show');
        }
    }
};

// Notes saving (keeps same contract as before)
async function saveNotes(){
    const content = document.getElementById('notes').value;
    console.debug('[editor] saveNotes', { len: content ? content.length : 0, content: content});
    try{
        const j = await fetchWithFlashes(
            document.body.dataset.updateUrl || '/update',
            {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({ notes: { value: content } })
            }
        );

        if(j && typeof j === 'object' && j.status === 'ok'){
            if(!(j.flashed && j.flashed.length)) showToast('Saved','success');
        }else{
            showToast('Save failed','error');
        }
    }catch(e){
        showToast('Network error', 'error');
    }
};


// add entry to hp history
async function addEntry(history_type){
    const description = document.getElementById('add-entry-desc-' + [history_type]).value;
    const value = document.getElementById('add-entry-value-' + [history_type]).value;
    console.debug('[editor] addEntry', { [history_type]: { description: description, value: value }});

    try{
        const j = await fetchWithFlashes(
            document.body.dataset.updateUrl || '/update',
            {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({ [history_type]: { value: value, description: description } })
            }
        );

        if(j && typeof j === 'object' && j.status === 'ok'){
            // if(!(j.flashed && j.flashed.length)) showToast('Saved','success');
        }else{
            showToast('Save failed','error');
        }

    }catch(e){
        showToast('Network error', 'error');
    }
};


document.addEventListener('click', async function(e){
    const btn = e.target.closest && e.target.closest('.remove-entry');
    if(!btn) return;
    e.preventDefault();

    const key = btn.getAttribute('data-key');
    const entry_nb = btn.getAttribute('data-value');

    if(!key) return;
    if(!entry_nb) return;

    console.debug('[editor] remove-entry click, removing: ', { key: key, dataset: entry_nb } );

    try{
        const body = {};
        const innerKey = "value";
        body[key] = {};
        body[key][innerKey] = entry_nb;
        const updateUrl = document.body.dataset.updateUrl || '/update';
        
        console.debug('[editor] sending update', { url: updateUrl, body: body });

        const j = await fetchWithFlashes(updateUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });

        console.debug('[editor] update response', j);

        if(j && j.status === 'ok'){
            // not much to do here, changing the hp or xp history always reloads the whole page
            closeDropdown();
            if(!(j.flashed && j.flashed.length)) showToast('Saved','success');
        }

    }catch(ex){
        showToast('Network error','error');
    }
}, false);



// Delegated handler for any element with class 'save-prop'
// Data attributes supported:
// - data-key: property key to send (required)
// - data-value: exact value to send (optional)
// - data-display: human-friendly label for UI (optional)
// - data-delta: integer, for numeric attribute adjustments (optional)
document.addEventListener('click', async function(e){
    const btn = e.target.closest && e.target.closest('.save-prop');
    if(!btn) return;
    e.preventDefault();

    const key = btn.getAttribute('data-key');
    if(!key) return;
    console.debug('[editor] save-prop click', { key: key, dataset: { value: btn.getAttribute('data-value'), delta: btn.getAttribute('data-delta'), display: btn.getAttribute('data-display') } });

    // build payload
    let payloadValue = null;
    let delta = null;
    if(btn.hasAttribute('data-value')){
        payloadValue = btn.getAttribute('data-value');
    }else if(btn.hasAttribute('data-delta')){
        // numeric update of an attribute: read current value from DOM and apply delta
        delta = parseInt(btn.getAttribute('data-delta')) || 0;

        let temp_span = null;
        temp_span = document.getElementById('prop-' + key);
        if(!temp_span){
            temp_span = document.getElementById('ability-' + key);
        }
        const span = temp_span;
        
        let cur = span ? parseInt(span.textContent) || 0 : 0;
        payloadValue = cur + delta;
    } else {
        // no value specified — nothing to do
        return;
    }
    console.debug('[editor] payloadValue computed', { key: key, payloadValue: payloadValue });

    try{
        const body = {};
        const innerKey = 'value';
        const innerKey2 = 'delta';
        body[key] = {};
        body[key][innerKey] = payloadValue;
        body[key][innerKey2] = delta;
        // body[key] = {innerKey: payloadValue, innerKey2: delta};

        const updateUrl = document.body.dataset.updateUrl || '/update';
        
        console.debug('[editor] sending update', { url: updateUrl, body: body });

        const j = await fetchWithFlashes(updateUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });

        console.debug('[editor] update response', j);

        if(j && j.status === 'ok'){
            // prefer server-canonical updated values when available
            const serverUpdated = (j.updated && j.updated.hasOwnProperty(key)) ? j.updated[key] : undefined;
            const effectiveValue = serverUpdated !== undefined ? serverUpdated : payloadValue;

            console.debug('Evaluating: ', {key});
            const test = 'prop-' + key;
            console.debug('Evaluating: ', {test});

            // partial UI updates depending on key
            if(key === 'tribe'){
                const display = btn.getAttribute('data-display') || effectiveValue;
                updateTribe(display);
                updateAttribute(j.updated);

            // } else if(key === 'profession'){
                // a change of the profession will trigger a full page reload
                // updateProfession(effectiveValue);

            } else if(key === 'specialization'){
                updateSpecialization(effectiveValue);

            } else if(document.getElementById('prop-' + key)){
                // if an element with id 'prop-' + key exists, for character attributes
                console.debug('found ', {key});
                updateAttribute(j.updated);

            } else if(key === 'armour'){
                updateArmour(j.updated)

            } else if(key === 'weapons'){
                updateWeapons(j.updated)

            } else if(document.getElementById('ability-' + key)){
                // if an element with id 'prop-' + key exists, for abilities
                console.debug('found ', {key});
                updateAbilities(j.updated);
                updateAbilityPoints(j.updated);
                updateAttribute(j.updated);
            }

            closeDropdown();
            if(!(j.flashed && j.flashed.length)) showToast('Saved','success');
        }
    }catch(ex){
        showToast('Network error','error');
    }
}, false);


// UI update helpers (separated for easier testing)
window.updateTribe = function(value){
    const dropbtn = document.querySelector('#tribe-list .dropbtn');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateProfession = function(value){
    const dropbtn = document.querySelector('#profession-list .dropbtn');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateSpecialization = function(value){
    const dropbtn = document.querySelector('#specialization-list .dropbtn');
    if(dropbtn) dropbtn.textContent = value;
};

window.updateAttribute = function(updated){
    // extract attributes dict
    attr_dict = updated['attributes'];
    console.debug('attribute dict', {updated});
    console.debug('attribute dict', {attr_dict});

    for(var key in attr_dict){
        // update attribute
        try{
            const span = document.getElementById('prop-' + key);
            if(span) span.textContent = attr_dict[key];
        }catch{
            continue;
        }
    }

    // extract attribute bonuses dict
    attr_bonus_dict = updated['attribute_bonuses'];
    console.debug('attribute dict', {attr_bonus_dict});

    for(var key in attr_bonus_dict){
        // update its corresponding bonus
        try{
            const span_bonus = document.getElementById('prop-' + key);
            if(span_bonus) span_bonus.textContent = attr_bonus_dict[key];
        }catch{
            continue;
        }
    }

    // TODO update of the endurance attribute needs to trigger refresh of the max_hp
    // extract max_hp and current_hp
    statistics_dict = updated['statistics'];
    console.debug('statistics dict', {statistics_dict});

    for(var key in statistics_dict){
        try{
            const span = document.getElementById('stat-' + key);
            if(span) span.textContent = statistics_dict[key];
        }catch{
            continue;
        }
    }

    updateAbilityPoints(updated);
};

window.updateArmour = function(value){
    const armour_list = value['armour'];
    for(var pos in armour_list){
        let dropbtn = document.querySelector('#armour-' + pos + ' .dropbtn');
        if(dropbtn) dropbtn.textContent = (+pos + 1) + ': ' + armour_list[+pos];
    }
};

window.updateWeapons = function(value){
    const weapon_list = value['weapons'];
    for(var pos in weapon_list){
        let dropbtn = document.querySelector('#weapon-' + pos + ' .dropbtn');
        if(dropbtn) dropbtn.textContent = (+pos + 1) + ': ' + weapon_list[+pos];
    }
};

window.updateAbilities = function(updated){
    const ability_dict = updated['abilities'];
    console.debug('ability dict', {ability_dict});

    for(var ability_key in ability_dict){
        console.debug('ability key', {ability_key});
        // update ability
        try{
            const span = document.getElementById('ability-' + ability_key);
            if(span) span.textContent = ability_dict[ability_key]['level'];
        }catch{
            continue;
        }
    }
};

window.updateAbilityPoints = function(updated){
    // extract ability points
    max_ability_points = updated['max_ability_points'];
    remaining_ability_points = updated['remaining_ability_points'];
    console.debug('max ability points', max_ability_points);
    console.debug('remaining ability points', remaining_ability_points);

    try{
        const span_max = document.getElementById('ability-max_points');
        const span_rem = document.getElementById('ability-remaining_points');

        if(span_max) span_max.textContent = max_ability_points;
        if(span_rem) span_rem.textContent = remaining_ability_points;
    }catch{
        return;
    }
};




// Avatar upload + delete handling (moved from template)
(function(){
    console.debug('[editor] init avatar IIFE');
    const form = document.getElementById('avatar-form');
    console.debug('[editor] avatar form element', { found: !!form });
    if(form){
        form.addEventListener('submit', async function(e){
            e.preventDefault();
            const fd = new FormData(form);
            console.debug('[editor] avatar upload submit', { action: form.action });
            try{
                const j = await fetchWithFlashes(form.action, {method:'POST', body: fd});
                console.debug('[editor] avatar upload response', j);
                if(j && (j.avatar_url_webp || j.avatar_url)){
                    const webp = j.avatar_url_webp ? (j.avatar_url_webp + '?t=' + Date.now()) : null;
                    const fallback = j.avatar_url ? (j.avatar_url + '?t=' + Date.now()) : (webp || null);
                    const wrapper = form.closest('.avatar-wrapper');
                    const container = wrapper ? wrapper.querySelector('.avatar-image') : document.querySelector('.avatar-image');
                    if(container){
                        let img = container.querySelector('img.avatar');
                        const placeholderSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><rect width="100%" height="100%" fill="#e5e7eb"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="#6b7280">No avatar</text></svg>';
                        const placeholder = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(placeholderSVG);
                        if(img){
                            img.style.opacity = '0';
                            const pic = img.closest('picture');
                            if(pic){
                                const srcEl = pic.querySelector('source[type="image/webp"]');
                                if(srcEl && webp){ srcEl.srcset = webp; }
                                img.src = fallback;
                            } else {
                                img.src = webp || fallback;
                            }
                            img.classList.remove('placeholder');
                            img.onload = () => { img.style.opacity = '1'; };
                        } else {
                            const pic = document.createElement('picture');
                            if(webp){
                                const src = document.createElement('source');
                                src.setAttribute('type', 'image/webp');
                                src.setAttribute('srcset', webp);
                                pic.appendChild(src);
                            }
                            img = document.createElement('img');
                            img.className = 'avatar avatar-image';
                            img.alt = 'avatar';
                            img.style.opacity = '0';
                            img.src = fallback || placeholder;
                            img.onload = () => { img.style.opacity = '1'; };
                            pic.appendChild(img);
                            container.innerHTML = '';
                            container.appendChild(pic);
                        }
                    }
                }
            }catch(e){
                showToast('Upload failed', 'error');
            }
        });
    }

    const del = document.getElementById('delete-avatar');
    if(del){
        console.debug('[editor] delete-avatar element', { found: !!del });
        del.addEventListener('click', async function(){
            console.debug('[editor] delete-avatar click');
            try{
                const j = await fetchWithFlashes(document.body.dataset.deleteAvatarUrl || '/me/delete_avatar', {method:'POST'});
                console.debug('[editor] delete-avatar response', j);
                if(j && !j.avatar_url && !j.avatar_url_webp){
                    const placeholderSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><rect width="100%" height="100%" fill="#e5e7eb"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="#6b7280">No avatar</text></svg>';
                    const placeholder = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(placeholderSVG);
                    document.querySelectorAll('img.avatar').forEach(img => {
                        const pic = img.closest('picture');
                        if(pic){
                            const srcEl = pic.querySelector('source[type="image/webp"]');
                            if(srcEl) srcEl.srcset = '';
                        }
                        img.style.opacity = '0';
                        img.onload = () => { img.classList.add('placeholder'); img.style.opacity = '1'; };
                        img.src = placeholder;
                    });
                    const preview = document.getElementById('avatar-preview');
                    if(preview) preview.innerHTML = '';
                }
            }catch(e){
                showToast('Remove failed', 'error');
            }
        });
    }

})();
