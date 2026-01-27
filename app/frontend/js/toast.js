// Shared toast helper
function showToast(message, kind=''){
  let t = document.getElementById('toast');
  if(!t){
    t = document.createElement('div');
    t.id = 'toast';
    t.className = 'toast';
    t.setAttribute('role','status');
    t.setAttribute('aria-live','polite');
    document.body.appendChild(t);
  }
  t.textContent = message;
  t.classList.remove('success','error');
  if(kind) t.classList.add(kind);
  t.classList.add('show');
  clearTimeout(t._hide);
  t._hide = setTimeout(()=>t.classList.remove('show'),2600);
}

// Utility to read flashed messages from a <script type="application/json" id="flashed-data"> element
(function(){
  try{
    const el = document.getElementById('flashed-data');
    if(el){
      const flashed = JSON.parse(el.textContent || '[]');
      if(Array.isArray(flashed)){
        flashed.forEach(function(pair){ showToast(pair[1], pair[0]); });
      }
    }
  }catch(e){/* ignore parsing issues */}
})();

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
        j.flashed.forEach(function(pair){ showToast(pair[1], pair[0]); });
      }
      
      // if server requested a reload (for changes that affect derived UI), do it now
      if(j && j.reload){
        // small delay to allow toasts to display
        setTimeout(function(){ window.location.reload(); }, 500);
      }
      return j;
    }
    // non-JSON response: return the Response object so callers can handle it
    return res;
  }catch(e){
    // parsing failed for some reason — return raw Response
    return res;
  }
}

// expose helper globally for templates to use
window.fetchWithFlashes = fetchWithFlashes;
