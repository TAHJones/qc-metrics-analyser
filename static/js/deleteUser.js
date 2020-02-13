const deleteUserForm = document.getElementById("deleteUserForm");
const deleteUserButton = document.getElementById("deleteUserButton");
const deleteUserList = document.getElementById("deleteUserList");

/**
* Function is called by "DOMContentLoaded" event. It hides or displays different sections of the page depending on whether the 'pageLocation' variable passed from the server contains the string 'runDeleted' or 'deleteRunForm'.
* @param {string} pageSection - pageLocation variable which can be string "usertDeleted" or "deleteUserForm".
*/
function hidePageSection(pageSection){
    if(pageSection == "userDeleted"){
        deleteUserForm.classList.add("hide");
        deleteUserButton.classList.add("hide");
        deleteUserList.classList.add("deleted");
    } else if(pageSection == "deleteUserForm") {
        deleteUserForm.classList.remove("hide");
        deleteUserButton.classList.remove("hide");
        deleteUserList.classList.remove("deleted");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hidePageSection(pageLocation);
});