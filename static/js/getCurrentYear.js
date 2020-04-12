/**
 * Function that uses js date method to get current year and add it to copyright statements then inserts them into page footer and marvel api modal.
 * @param {string} location - either "footer" or "marvelApiModal"
 */

const copyRight = document.getElementById("copyRight");
// const startGuide = document.getElementById("startGuide");

function getCurrentYear(){
  let copyRightText;
//   let marvelCopyRightText
  let currentTime = new Date();
  let year = currentTime.getFullYear();
//   if(location === "footer") {
    copyRightText = "2019 - " + year + " © Thomas Jones - All Rights Reserved";
    return copyRightText;
//   } else if(location === "marvelApiModal") {
//     marvelCopyRightText = year + " © Marvel - All Rights Reserved";
//     return marvelCopyRightText;
//   }
}

// call getCurrentYear function and insert copyright statement into footer
copyRight.innerHTML = getCurrentYear();
