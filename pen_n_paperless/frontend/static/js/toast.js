
// Shared toast helper
function showToast(message, kind=''){
    // create new toast object if it does not exist yet in the document
    let t = document.getElementById('toast');
    if(!t){
        t = document.createElement('div');
        t.id = 'toast';
        t.className = 'toast';
        t.setAttribute('role','status');
        t.setAttribute('aria-live','polite');
        document.body.appendChild(t);
    }
    // apply basic config to the toast
    t.textContent = message;
    for (let status in StatusCode) {
        t.classList.remove(status);
    }
    // t.classList.remove('success', 'warning', 'error');
    if(kind) t.classList.add(kind);
    t.classList.add('show');
    clearTimeout(t._hide);
    t._hide = setTimeout(()=>t.classList.remove('show'),2600);
};


// Small helper to perform fetch and display any flashed messages returned in JSON.
// Usage: const j = await fetchWithFlashes(url, options);
async function fetchWithFlashes(url, options){
    const res = await fetch(url, options);
    // only parse JSON when the server actually responded with JSON
    try{
        const ct = (res.headers && res.headers.get) ? (res.headers.get('content-type') || '') : '';
        if(ct.indexOf('application/json') !== -1){
            const j = await res.clone().json();
            
            if(j && j.flashed && Array.isArray(j.flashed)){
                j.flashed.forEach(function(pair){ 
                    showToast(pair[1], pair[0]); 
                });
            }
            
            // if server requested a reload, do it now
            if(j && j.reload){
                // small delay to allow toasts to display
                setTimeout(function(){ window.location.reload(); }, 500);
            }

            // remove 'flashed' and 'reload' properties
            const { flashed, reload, ...unprocessedData } = j;
            return unprocessedData;
        }
        // non-JSON response: return the Response object so callers can handle it
        return res;
    }catch(e){
        // parsing failed for some reason — return raw Response
        return res;
    }
};

// expose helper globally for templates to use
window.fetchWithFlashes = fetchWithFlashes;
