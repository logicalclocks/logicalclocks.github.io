/*
    This script removes the sidebar from the Getting Started page for the example to expand whole page on non-mobile devices.
*/

//https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent for recommended approach to test if device is mobile
if(window.location.pathname.endsWith('hopsworks-tutorials/quickstart/') && !/Mobi|Android/i.test(navigator.userAgent)) {
    document.getElementsByClassName("md-sidebar--primary")[0].remove()
}