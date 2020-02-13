//let pageLocation = JSON.parse({{ pageLocation|tojson }});
const userForm = document.getElementById("userFormBg");
const userRuns = document.getElementById("userRunsBg");
const userRun = document.getElementById("userRunBg");

/**
* Function is called by "DOMContentLoaded" event. It hides or displays different sections of the page depending on whether the 'pageLocation' variable passed from the server contains the string 'runDeleted' or 'deleteRunForm'.
* @param {string} pageSection - pageLocation variable which can be string "userRuns", "userRun" or "userForm".
*/
function hidePageSection(pageSection){
    if(pageSection=="userRuns"){
        userRuns.classList.remove("hide");
        userRun.classList.add("hide");
        userForm.classList.add("hide");
    } else if(pageSection=="userRun") {
        userRuns.classList.add("hide");
        userRun.classList.remove("hide");
        userForm.classList.add("hide");
    } else if(pageSection=="userForm") {
        userRuns.classList.add("hide");
        userRun.classList.add("hide");
        userForm.classList.remove("hide");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hidePageSection(pageLocation);
});