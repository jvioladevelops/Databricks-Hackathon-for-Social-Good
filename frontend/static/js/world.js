function clickToShowStep2() {
  var x = document.getElementById("step2WholeSurvey");
  if (x.style.visibility === "hidden") {
    x.style.visibility = "visible";
    x.style.overflow = "auto";
    x.style.height = "100%";
  } else {
    x.style.visibility = "hidden";
    x.style.overflow = "hidden";
    x.style.height = "0";
  }
  //calling step2 anchor
  document.getElementById("anchorStep2").click();
}
function checkRegionCode(regionCode) {
  if (regionCode.localeCompare("US") == 0) {
    console.log("hello,it works");
  } else if (regionCode.localeCompare("CN") == 0) {
    console.log("hello,it works too");
  }
}
