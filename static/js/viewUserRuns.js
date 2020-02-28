const userForm = document.getElementById("userFormBg");
const userRuns = document.getElementById("userRunsBg");
const userRun = document.getElementById("userRunBg");

function hidePageSection(pageSection){
    if(pageSection=="userRun"){
        userRun.classList.remove("hide");
        userRuns.classList.add("hide");
        userForm.classList.add("hide");
    } else if(pageSection=="userRuns") {
        userRun.classList.add("hide");
        userRuns.classList.remove("hide");
        userForm.classList.add("hide");
    } else if(pageSection=="userForm"){
        userRun.classList.add("hide");
        userRuns.classList.add("hide");
        userForm.classList.remove("hide");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hidePageSection(pageLocation);
});