/*
    This script removes the sidebar from the Getting Started page for the example to expand whole page.
*/

if(window.location.pathname.endsWith('getting_started/quickstart/')) {
    document.getElementsByClassName("md-sidebar--primary")[0].remove()
}