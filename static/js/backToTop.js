/**
 *  CREDIT: code for scrolling button taken from
 *  https://www.w3schools.com/howto/howto_js_scroll_to_top.asp 
 */

const backToTop = document.getElementById("backToTop");

/**
 * triggers scrollingButton function on scroll event
 */ 
window.addEventListener("scroll", scrollingButton, false);


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
 * Calls topFunction function to scroll back to the
 * top of the page when floating button is clicked
 */
backToTop.addEventListener("click", topFunction, false);


/**
 * topFunction function scrolls back to the top of the page
 */
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
