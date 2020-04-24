const backToTop = document.getElementById("backToTop");
const copyRight = document.getElementById("copyRight");


/**
 *  CREDIT: code for scrolling button taken from
 *  https://www.w3schools.com/howto/howto_js_scroll_to_top.asp 
 * makes floating button visible once user starts scrolling.
 */
function scrollingButton() {
    if (document.body.scrollTop > 40 || document.documentElement.scrollTop > 40) {
        backToTop.classList.add("active");
    } else {
        backToTop.classList.remove("active");
    }
}


/**
 * topFunction function scrolls back to the top of the page
 */
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


/**
 * floatButton function fixes floating button in place on screens larger than 1200px
 * It also unfixes floating button on screens smaller than 1200px
 */
function floatButton() {
    if (window.innerWidth >= 1200) {
        backToTop.classList.replace("btn-float", "btn-fixed");
        backToTop.classList.add("active");

    } else {
        backToTop.classList.replace("btn-fixed", "btn-float");
    }
}


/**
 * Function that uses js date method to get current year and add it to copyright statements then inserts them into page footer and marvel api modal.
 * @param {string} location - either "footer" or "marvelApiModal"
 */
function getCurrentYear() {
  let copyRightText;
  let currentTime = new Date();
  let year = currentTime.getFullYear();
    copyRightText = "2019 - " + year + " © Thomas Jones - All Rights Reserved";
    return copyRightText;
}

// eventlisteners 
window.addEventListener("scroll", scrollingButton, false);
backToTop.addEventListener("click", topFunction, false);
document.addEventListener("DOMContentLoaded", floatButton, false);
window.addEventListener("resize", floatButton, false);

// function calls
copyRight.innerHTML = getCurrentYear();

// enable bootstrap popover component
$(function(){
    $("[data-toggle=popover]").popover();
});