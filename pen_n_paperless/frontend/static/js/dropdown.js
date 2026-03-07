

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



