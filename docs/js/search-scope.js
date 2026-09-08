// Search scope: an "All | API" switch above the search results, so a reader
// after a function or class can drop the prose hits. Material's own result
// list renders page hits lazily on scroll and cannot be filtered without
// losing hits, so the API scope runs Material's search worker a second time
// (same script, same index, created on first use) and renders a flat list of
// symbols in the same result markup while Material's list is hidden. The
// choice persists in localStorage.
document.addEventListener("DOMContentLoaded", function () {
  var result = document.querySelector(".md-search-result");
  var input = document.querySelector(".md-search__input");
  var meta = result && result.querySelector(".md-search-result__meta");
  var configEl = document.getElementById("__config");
  if (!result || !input || !meta || !configEl) return;
  var config = JSON.parse(configEl.textContent);

  var KEY = "hops-search-scope";
  var LIMIT = 60;
  var scope = "all";
  try { scope = localStorage.getItem(KEY) === "api" ? "api" : "all"; } catch (e) { /* storage blocked */ }

  // Switch, above Material's count line.
  var bar = document.createElement("div");
  bar.className = "hops-search-scope";
  bar.setAttribute("role", "tablist");
  var buttons = {};
  [["all", "All"], ["api", "API"]].forEach(function (pair) {
    var b = document.createElement("button");
    b.type = "button";
    b.setAttribute("role", "tab");
    b.dataset.scope = pair[0];
    b.textContent = pair[1];
    b.addEventListener("click", function () { setScope(pair[0]); });
    bar.appendChild(b);
    buttons[pair[0]] = b;
  });
  result.insertBefore(bar, meta);

  // API list and its count line, siblings of Material's own.
  var apiMeta = document.createElement("div");
  apiMeta.className = "md-search-result__meta hops-api-meta";
  var apiList = document.createElement("ol");
  apiList.className = "md-search-result__list hops-api-list";
  result.appendChild(apiMeta);
  result.appendChild(apiList);

  var worker = null;
  var ready = false;
  var queued = null;
  var timer = null;

  function setScope(next) {
    scope = next;
    try { localStorage.setItem(KEY, scope); } catch (e) { /* storage blocked */ }
    render();
    if (scope === "api") query(input.value);
  }

  function render() {
    result.dataset.scope = scope;
    Object.keys(buttons).forEach(function (k) {
      buttons[k].setAttribute("aria-selected", k === scope ? "true" : "false");
    });
  }

  function ensureWorker() {
    if (worker) return;
    worker = new Worker(config.search);
    worker.addEventListener("message", function (ev) {
      var msg = ev.data;
      if (msg.type === 1) {
        ready = true;
        if (queued !== null) { worker.postMessage({ type: 2, data: queued }); queued = null; }
      } else if (msg.type === 3) {
        show(msg.data.items || []);
      }
    });
    fetch(config.base + "/search/search_index.json")
      .then(function (r) { return r.json(); })
      .then(function (index) {
        // Same shape Material posts: the index plus the feature options.
        index.options = { suggest: false };
        worker.postMessage({ type: 0, data: index });
      });
  }

  // Material's own query transform, reduced: a trailing wildcard on plain terms.
  function transform(value) {
    return value.trim().split(/\s+/).filter(Boolean).map(function (term) {
      return /^[\w.-]+$/.test(term) ? term + "*" : term;
    }).join(" ");
  }

  function query(value) {
    ensureWorker();
    var q = transform(value);
    if (!q) { show([]); return; }
    if (!ready) { queued = q; return; }
    worker.postMessage({ type: 2, data: q });
  }

  function show(groups) {
    var hits = [];
    groups.forEach(function (group) {
      group.forEach(function (item) {
        var i = item.location.indexOf("#");
        if (item.location.indexOf("python-api/") === 0 && i > 0) hits.push(item);
      });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    hits = hits.slice(0, LIMIT);
    apiList.textContent = "";
    hits.forEach(function (item) {
      var path = item.location.slice(item.location.indexOf("#") + 1);
      var li = document.createElement("li");
      li.className = "md-search-result__item";
      var a = document.createElement("a");
      a.className = "md-search-result__link";
      a.href = config.base + "/" + item.location;
      a.tabIndex = -1;
      var article = document.createElement("article");
      article.className = "md-search-result__article md-typeset";
      var h1 = document.createElement("h1");
      // Title as the worker returns it: our own index text with <mark> on
      // the matched terms and the symbol-kind badge, like Material's list.
      h1.innerHTML = item.title;
      var p = document.createElement("p");
      p.className = "md-search-result__teaser";
      p.textContent = path;
      article.appendChild(h1);
      article.appendChild(p);
      a.appendChild(article);
      li.appendChild(a);
      apiList.appendChild(li);
    });
    apiMeta.textContent = input.value.trim()
      ? (hits.length ? hits.length + " API symbols" : "No API symbol matches")
      : "Type to search the Python API";
  }

  input.addEventListener("input", function () {
    if (scope !== "api") return;
    clearTimeout(timer);
    timer = setTimeout(function () { query(input.value); }, 120);
  });

  render();
  if (scope === "api") query(input.value);
});
