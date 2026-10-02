# Hosted Hopsworks docs MCP server (streamable-http).
#
# The server code is baked into the image; the docs it indexes are not. The sync
# loop in docker-entrypoint.sh keeps one checkout per published docs version
# (from the site's versions.json) and the server reindexes on change. Rebuild
# the image only when server code changes, never when the docs do.
FROM python:3.13-slim

# git: clone/pull the docs repo at runtime. No build toolchain needed (pure-Python deps).
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY hopsworks_docs_mcp ./hopsworks_docs_mcp
RUN pip install --no-cache-dir .

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Defaults; override in compose. DOCS_REPO/DOCS_VERSIONS_URL drive the sync loop.
ENV MCP_TRANSPORT=streamable-http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8080 \
    MCP_REINDEX_INTERVAL=60 \
    DOCS_REPO=https://github.com/logicalclocks/logicalclocks.github.io.git \
    DOCS_VERSIONS_URL=https://docs.hopsworks.ai/versions.json \
    DOCS_ROOT=/docs-repo \
    SYNC_INTERVAL=300

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
