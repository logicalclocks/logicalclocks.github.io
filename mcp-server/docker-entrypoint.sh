#!/usr/bin/env bash
# Keep one shallow checkout of the docs repo per published docs version, then
# serve the MCP over HTTP. The version list comes from the site's own mike
# versions.json, so a new release branch (and the `latest` alias moving to it)
# is picked up with no config change. `dev` maps to main, every other version
# to branch-<version>. The server rereads versions.json and reindexes changed
# versions on its own (MCP_REINDEX_INTERVAL), so no restart is needed. Run with
# `init: true` in compose so the background sync loop is reaped cleanly.
set -euo pipefail

DOCS_REPO="${DOCS_REPO:?DOCS_REPO is required}"
DOCS_VERSIONS_URL="${DOCS_VERSIONS_URL:-https://docs.hopsworks.ai/versions.json}"
DOCS_ROOT="${DOCS_ROOT:-/docs-repo}"
SYNC_INTERVAL="${SYNC_INTERVAL:-300}"

mkdir -p "${DOCS_ROOT}"

# A volume from the single-branch layout holds one clone at its root: start clean.
if [ -d "${DOCS_ROOT}/.git" ]; then
    echo "[sync] removing the single-branch checkout in ${DOCS_ROOT}"
    find "${DOCS_ROOT}" -mindepth 1 -delete
fi

# Print "<version> <branch>" per line from versions.json (stdin).
versions_to_branches() {
    python -c '
import json, sys
for v in json.load(sys.stdin):
    name = v["version"]
    print(name, "main" if name == "dev" else f"branch-{name}")
'
}

# Clone or fast-forward one version. Only the Markdown under docs/ and mkdocs.yml
# are checked out; with the blob filter, images are never downloaded.
sync_version() {
    local version="$1" branch="$2" dir="${DOCS_ROOT}/$1"
    if [ -d "${dir}/.git" ]; then
        git -C "${dir}" fetch -q --depth 1 origin "${branch}" \
            && git -C "${dir}" reset -q --hard FETCH_HEAD
    else
        rm -rf "${dir}"
        git clone -q --depth 1 --filter=blob:none --sparse --branch "${branch}" \
            "${DOCS_REPO}" "${dir}" \
            && git -C "${dir}" sparse-checkout set --no-cone '/docs/**/*.md' /mkdocs.yml
    fi
}

sync_all() {
    local tmp="${DOCS_ROOT}/.versions.json.tmp" version branch synced=0
    if ! python -c 'import sys, urllib.request; sys.stdout.buffer.write(urllib.request.urlopen(sys.argv[1], timeout=30).read())' \
        "${DOCS_VERSIONS_URL}" > "${tmp}"; then
        echo "[sync] could not fetch ${DOCS_VERSIONS_URL}, keeping the current versions" >&2
        return 1
    fi
    while read -r version branch; do
        if sync_version "${version}" "${branch}"; then
            synced=$((synced + 1))
        elif [ -d "${DOCS_ROOT}/${version}/.git" ]; then
            echo "[sync] ${version}: fetch of ${branch} failed, serving the previous checkout" >&2
        else
            echo "[sync] ${version}: no usable ${branch}, skipped" >&2
            rm -rf "${DOCS_ROOT:?}/${version}"
        fi
    done < <(versions_to_branches < "${tmp}")
    # Drop checkouts of versions the site no longer lists.
    for dir in "${DOCS_ROOT}"/*/; do
        version="$(basename "${dir}")"
        python -c 'import json, sys; sys.exit(sys.argv[2] not in {v["version"] for v in json.load(open(sys.argv[1]))})' \
            "${tmp}" "${version}" || rm -rf "${dir}"
    done
    # Publish the list last, so the server never sees a version before its checkout.
    mv "${tmp}" "${DOCS_ROOT}/versions.json"
    echo "[sync] ${synced} version(s) in sync"
}

echo "[sync] initial sync from ${DOCS_VERSIONS_URL} into ${DOCS_ROOT}"
sync_all || [ -f "${DOCS_ROOT}/versions.json" ] || {
    echo "[sync] no versions available, cannot start" >&2
    exit 1
}

export HOPSWORKS_DOCS_ROOT="${DOCS_ROOT}"

# Background: resync on an interval. A failed tick is logged and retried, never fatal.
(
    while true; do
        sleep "${SYNC_INTERVAL}"
        sync_all || true
    done
) &

echo "[serve] starting MCP on ${MCP_HOST:-0.0.0.0}:${MCP_PORT:-8080} (docs root: ${HOPSWORKS_DOCS_ROOT})"
exec python -m hopsworks_docs_mcp
