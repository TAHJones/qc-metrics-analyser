/**
 *  CREDIT: code for scrolling button taken from
 *  https://www.w3schools.com/howto/howto_js_scroll_to_top.asp 
 */

const backToTop = document.getElementById("backToTop");


/**
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
 * triggers scrollingButton function on scroll event
 */ 
window.addEventListener("scroll", scrollingButton, false);


/**
 * Calls topFunction function to scroll back to the
 * top of the page when floating button is clicked
 */
backToTop.addEventListener("click", topFunction, false);


/**
 * call floatButton function when page is fully loaded or when window size changes
 */
document.addEventListener("DOMContentLoaded", floatButton, false);
window.addEventListener("resize", floatButton, false);