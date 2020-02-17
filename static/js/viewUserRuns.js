const userForm = document.getElementById("userFormBg");
const userRuns = document.getElementById("userRunsBg");
const userRun = document.getElementById("userRunBg");
// const returnToForm = document.getElementById("returnToForm");
// const deleteRun = document.getElementById("deleteRun");
// const updateRun = document.getElementById("updateRun");
// const selectFilteredRunForm = document.getElementById("selectFilteredRunForm");

function hidePageSection(pageSection){
    if(pageSection=="userRun"){
        userRun.classList.remove("hide");
        userRuns.classList.add("hide");
        userForm.classList.add("hide");
        // selectFilteredRunForm.classList.add("hide")
        // deleteRun.classList.remove("invisible");
        // updateRun.classList.remove("invisible");            
    } else if(pageSection=="userRuns") {
        userRun.classList.add("hide");
        userRuns.classList.remove("hide");
        userForm.classList.add("hide");
        // selectFilteredRunForm.classList.remove("hide")
    } else if(pageSection=="userForm"){
        userRun.classList.add("hide");
        userRuns.classList.add("hide");
        userForm.classList.remove("hide");
        // selectFilteredRunForm.classList.remove("hide")
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hidePageSection(pageLocation);
});