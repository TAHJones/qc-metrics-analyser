const userForm = document.getElementById("userFormBg");
const userRuns = document.getElementById("userRunsBg");
const returnToForm = document.getElementById("returnToForm");
const deleteRun = document.getElementById("deleteRun");
const updateRun = document.getElementById("updateRun");
const selectFilteredRunForm = document.getElementById("selectFilteredRunForm");

function hidePageSection(pageSection){
    if(pageSection=="userRun"){
        userRuns.classList.remove("hide");
        userForm.classList.add("hide");
        selectFilteredRunForm.classList.add("hide")
        deleteRun.classList.remove("invisible");
        updateRun.classList.remove("invisible");            
    } else if(pageSection=="userRuns") {
        userRuns.classList.remove("hide");
        userForm.classList.add("hide");
        selectFilteredRunForm.classList.remove("hide")
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hidePageSection(pageLocation);
});

returnToForm.addEventListener("click", function(){
    userRuns.classList.add("hide");
    userForm.classList.remove("hide");
    deleteRun.classList.add("invisible");
    updateRun.classList.add("invisible");
});