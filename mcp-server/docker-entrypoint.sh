#!/usr/bin/env bash
# Keep a shallow clone of the docs repo in sync with its branch, then serve the
# MCP over HTTP. The server watches the docs on disk (MCP_REINDEX_INTERVAL) and
# rebuilds its index when this loop pulls new content, so the endpoint follows
# the branch with no restart. Run with `init: true` in compose so the
# background pull loop is reaped cleanly.
set -euo pipefail

DOCS_REPO="${DOCS_REPO:?DOCS_REPO is required}"
DOCS_BRANCH="${DOCS_BRANCH:-main}"
DOCS_DIR="${DOCS_DIR:-/docs-repo}"
SYNC_INTERVAL="${SYNC_INTERVAL:-300}"

if [ ! -d "${DOCS_DIR}/.git" ]; then
    echo "[sync] cloning ${DOCS_REPO} (${DOCS_BRANCH}) -> ${DOCS_DIR}"
    git clone --depth 1 --branch "${DOCS_BRANCH}" "${DOCS_REPO}" "${DOCS_DIR}"
fi

export HOPSWORKS_DOCS_DIR="${DOCS_DIR}/docs"

# Background: pull the branch on an interval. --ff-only never rewrites history;
# a failed pull (transient network) is logged and retried next tick, never fatal.
(
    while true; do
        sleep "${SYNC_INTERVAL}"
        if git -C "${DOCS_DIR}" pull --ff-only -q; then
            echo "[sync] pulled ${DOCS_BRANCH} @ $(git -C "${DOCS_DIR}" rev-parse --short HEAD)"
        else
            echo "[sync] pull failed, will retry in ${SYNC_INTERVAL}s" >&2
        fi
    done
) &

echo "[serve] starting MCP on ${MCP_HOST:-0.0.0.0}:${MCP_PORT:-8080} (docs: ${HOPSWORKS_DOCS_DIR})"
exec python -m hopsworks_docs_mcp
