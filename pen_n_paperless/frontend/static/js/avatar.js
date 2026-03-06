
function getPlaceholder(){
    const placeholderSVG = '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><rect width="100%" height="100%" fill="#e5e7eb"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="#6b7280">No avatar</text></svg>';
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(placeholderSVG);
}



async function setOptPlaceholder(){

    const form = document.getElementById('avatar-form');
    const wrapper = form ? form.closest('.avatar-wrapper') : null;
    const container = wrapper ? wrapper.querySelector('.avatar-image') : document.querySelector('.avatar-image');
    if(container){
        // get current image
        let img = container.querySelector('img.avatar');

        // Use the raw attribute value (what was set in HTML or by scripts) to detect
        // placeholder markers like '#', the absolute path of the page may be prepended
        const rawSrc = img ? img.getAttribute('src') : null;
        const avatarURL = img ? img.src : '';

        // determine if the current src is a valid absolute URL to an avatar
        let hasValidUrl = true;
        try{
            new URL(avatarURL);
        }catch(e){
            hasValidUrl = false;
        }

        // treat missing/empty attribute, '#' or about:blank as invalid
        const rawMissing = !rawSrc || rawSrc === '#' || rawSrc === 'about:blank';

        if(rawMissing || !hasValidUrl){
            // avatar url is invalid, no avatar available yet, add placeholder

            if(img){
                img.style.opacity = '0';
                img.src = getPlaceholder();
                img.classList.add('placeholder');
                img.style.opacity = '1';
            }

            console.debug(
                '[avatar.js] setOptPlaceholder, setting placeholder', 
                { 
                    'url': getPlaceholder()
                }
            );

        } else{
            // an avatar is already set, remove placeholder css class

            if(img){
                img.classList.remove('placeholder');
            }

            console.debug(
                '[avatar.js] setOptPlaceholder, avatar active', 
                { 
                    'url': avatarURL
                }
            );

        }
    }else{
        console.error(
            '[avatar.js] setOptPlaceholder failed', 
            { 
                "reason" : "failed to retrieve container of the avatar",
                "container": container
            }
        );
    }

}




// https://www.infoworld.com/article/2169473/using-javascript-and-forms.html
// Note to self:
// var is not scoped, can be redeclared
// let is scoped, cannot be redeclared, can be reassigned
// const is scoped, cannot be redeclared, cannot be reassigned

async function uploadAvatar(form) {

    const key = Avatars.AVATAR;
    const formData = new FormData(form);
    const characterName = document.getElementById('character_name').innerHTML;
    
    console.debug(
        '[avatar.js] uploadAvatar -> Server', 
        { 
            "character_name": characterName,
            "key": key,
            "form data": formData
        }
    );

    try{
        const dataUpdate = await fetchWithFlashes(
            // use data-upload-avatar-url from the HTML template
            document.body.dataset.uploadAvatarUrl, 
            {
                method:'POST', 
                body: formData
            }
        );

        console.debug(
            '[avatar.js] Server -> uploadAvatar', 
            { 
                "data": dataUpdate
            }
        );

        if(dataUpdate && typeof dataUpdate === 'object' && dataUpdate.status === 'success' && dataUpdate.avatarURL){
            showToast('Saved','success');

            // fetch all needed elements
            const avatarURL = dataUpdate.avatarURL;
            const wrapper = form.closest('.avatar-wrapper');
            const container = wrapper ? wrapper.querySelector('.avatar-image') : document.querySelector('.avatar-image');
            if(container){
                // get current image
                let img = container.querySelector('img.avatar');
                img.style.opacity = '0';
                img.src = avatarURL;
                img.style.opacity = '1';

                setOptPlaceholder();

            }else{
                console.error(
                    '[avatar.js] updating avatar url failed', 
                    { 
                        "reason" : "failed to retrieve container of the avatar",
                        "container": container
                    }
                );
            }

        }else{
            showToast('Save failed','error');
        }

    }catch(e){
        console.error(
            '[avatar.js] fetchWithFlashes failed', 
            { 
                "exception": e
            }
        );
        showToast('Network error', 'error');
    }
}


async function deleteAvatar(form){

    const key = Avatars.AVATAR;
    const characterName = document.getElementById('character_name').innerHTML;

    console.debug(
        '[avatar.js] deleteAvatar -> Server', 
        { 
            "character_name": characterName,
            "key": key,
        }
    );

    try{
        const dataUpdate = await fetchWithFlashes(
            // use data-delete-avatar-url from the HTML template
            document.body.dataset.deleteAvatarUrl,
            {
                method:'POST',
                headers:{'Content-Type':'application/json'},
            }
        );

        console.debug(
            '[avatar.js] Server -> deleteAvatar', 
            { 
                "data": dataUpdate
            }
        );

        if(dataUpdate && typeof dataUpdate === 'object' && dataUpdate.status === 'success' && dataUpdate.avatarURL === "#"){
            showToast('Deleted','success');

            const wrapper = form.closest('.avatar-wrapper');
            const container = wrapper ? wrapper.querySelector('.avatar-image') : document.querySelector('.avatar-image');
            if(container){
                // get current image
                let img = container.querySelector('img.avatar');

                if(img){
                    img.style.opacity = '0';
                    // clear the src so setOptPlaceholder can detect missing avatar
                    img.src = '#';
                }

                setOptPlaceholder();
            
            } else{
                console.error(
                    '[avatar.js] replacing avatar url failed', 
                    { 
                        "reason" : "failed to retrieve container of the avatar",
                        "container": container
                    }
                );
            }

        } else{
            showToast('Delete failed','error');
        }

    } catch(e){
        console.error(
            '[avatar.js] fetchWithFlashes failed', 
            { 
                "exception": e
            }
        );
        showToast('Network error', 'error');
    }
}
