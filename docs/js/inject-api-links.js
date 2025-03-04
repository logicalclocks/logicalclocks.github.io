window.addEventListener("DOMContentLoaded", function () {
    var windowPathNameSplits = window.location.pathname.split("/");
    var majorVersionRegex = new RegExp("(\\d+[.]\\d+)");
    var latestRegex = new RegExp("latest");
    var majorVersion = "latest"; // Default version
    
    // Determine the current version from URL
    if (majorVersionRegex.test(windowPathNameSplits[1])) {
        // On landing page docs.hopsworks.api/4.0 - URL contains major version
        majorVersion = windowPathNameSplits[1];
    } else if (!latestRegex.test(windowPathNameSplits[2]) && !latestRegex.test(windowPathNameSplits[1])) {
        // If we're not on latest, try to parse version
        var apiVersion = windowPathNameSplits[2];
        if (apiVersion && majorVersionRegex.test(apiVersion)) {
            majorVersion = apiVersion.match(majorVersionRegex)[0];
        }
    }
    
    // Only update external API links, not navigation links for local development
    var hopsworksApiLink = document.getElementById("hopsworks_api_link");
    var hsfsJavadocLink = document.getElementById("hsfs_javadoc_link");
    
    if (hopsworksApiLink) {
        hopsworksApiLink.href = "https://docs.hopsworks.ai/hopsworks-api/" + majorVersion + "/generated/api/login/";
    }
    
    if (hsfsJavadocLink) {
        hsfsJavadocLink.href = "https://docs.hopsworks.ai/hopsworks-api/" + majorVersion + "/javadoc";
    }
    
    // Skip updating local navigation links when in development mode
    if (window.location.hostname === "docs.hopsworks.ai") {
        // Only update links when on the production site
        var navLinks = document.getElementsByClassName("md-tabs__link");
        if (navLinks.length >= 7) {
            navLinks[0].href = "https://docs.hopsworks.ai/" + majorVersion;
            navLinks[1].href = "https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb";
            navLinks[2].href = "https://docs.hopsworks.ai/" + majorVersion + "/tutorials/";
            navLinks[3].href = "https://docs.hopsworks.ai/" + majorVersion + "/concepts/hopsworks/";
            navLinks[4].href = "https://docs.hopsworks.ai/" + majorVersion + "/user_guides/";
            navLinks[5].href = "https://docs.hopsworks.ai/" + majorVersion + "/setup_installation/aws/getting_started/";
            // navLinks[6] is for API, which is handled by dropdown.js
        }
    }
});
