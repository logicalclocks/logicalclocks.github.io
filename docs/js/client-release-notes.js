// Python client release notes on the release pages. Each release ends with a
// `.hops-client-notes` block naming the hopsworks-api versions it ships and linking
// their GitHub releases (scripts/releases_hook.py). This fetches those releases from
// the GitHub API in the reader's browser and shows their notes as GitHub renders
// them, one collapsed block per version. When GitHub can't be reached or a version
// is missing, the links stay.
(function () {
  var REPO = "https://api.github.com/repos/logicalclocks/hopsworks-api/releases";
  var HTML = { Accept: "application/vnd.github.html+json" };
  var CACHE = "hops-client-releases";
  var TTL = 60 * 60 * 1000; // anonymous GitHub API calls are limited per reader

  function cached() {
    try {
      var entry = JSON.parse(sessionStorage.getItem(CACHE));
      if (entry && Date.now() - entry.at < TTL) return entry.releases;
    } catch (e) {}
    return null;
  }

  function store(releases) {
    try {
      sessionStorage.setItem(CACHE, JSON.stringify({ at: Date.now(), releases: releases }));
    } catch (e) {}
  }

  function json(url) {
    return fetch(url, { headers: HTML }).then(function (response) {
      if (!response.ok) throw new Error(response.status);
      return response.json();
    });
  }

  function add(releases, release) {
    releases[release.tag_name] = { html: release.body_html || "", url: release.html_url };
  }

  // One call lists the latest releases; a version older than those costs one more.
  function load(versions) {
    var releases = cached() || {};
    var missing = versions.filter(function (v) { return !releases[v]; });
    if (!missing.length) return Promise.resolve(releases);
    return json(REPO + "?per_page=100")
      .then(function (list) {
        list.forEach(function (release) { add(releases, release); });
        return Promise.all(
          missing
            .filter(function (v) { return !releases[v]; })
            .map(function (v) {
              return json(REPO + "/tags/" + encodeURIComponent(v))
                .then(function (release) { add(releases, release); })
                .catch(function () {});
            })
        );
      })
      .then(function () {
        // Keep only what this page shows: the notes of every release run to 1 MB.
        var kept = cached() || {};
        versions.forEach(function (v) { if (releases[v]) kept[v] = releases[v]; });
        store(kept);
        return releases;
      });
  }

  // GitHub sanitizes body_html; this also drops anything active, and turns headings
  // into bold paragraphs so the notes don't enter the page's own outline.
  function notes(html) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    doc.querySelectorAll("script, style, iframe, object, embed, form").forEach(function (el) {
      el.remove();
    });
    doc.querySelectorAll("*").forEach(function (el) {
      Array.prototype.slice.call(el.attributes).forEach(function (attr) {
        if (/^on/i.test(attr.name)) el.removeAttribute(attr.name);
      });
    });
    doc.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach(function (heading) {
      var p = doc.createElement("p");
      var strong = doc.createElement("strong");
      strong.textContent = heading.textContent;
      p.appendChild(strong);
      heading.replaceWith(p);
    });
    doc.querySelectorAll("a[href]").forEach(function (a) {
      a.target = "_blank";
      a.rel = "noopener";
    });
    var body = document.createElement("div");
    body.className = "hops-client-notes__body";
    Array.prototype.slice.call(doc.body.childNodes).forEach(function (node) {
      body.appendChild(document.importNode(node, true));
    });
    return body;
  }

  function render(block, releases) {
    var versions = block.dataset.versions.split(" ");
    if (!versions.every(function (v) { return releases[v]; })) return;
    var children = [];
    versions.slice().reverse().forEach(function (v) {
      var details = document.createElement("details");
      details.className = "note";
      var summary = document.createElement("summary");
      summary.textContent = "hopsworks-api " + v;
      var link = document.createElement("p");
      link.className = "hops-client-notes__title";
      var a = document.createElement("a");
      a.href = releases[v].url;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = "Release " + v + " on GitHub";
      link.appendChild(a);
      details.append(summary, link, notes(releases[v].html));
      children.push(details);
    });
    block.replaceChildren.apply(block, children);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var blocks = Array.prototype.slice.call(
      document.querySelectorAll(".hops-client-notes[data-versions]")
    );
    if (!blocks.length) return;
    var versions = [];
    blocks.forEach(function (block) {
      versions = versions.concat(block.dataset.versions.split(" "));
    });
    load(versions)
      .then(function (releases) {
        blocks.forEach(function (block) { render(block, releases); });
      })
      .catch(function () {});
  });
})();
