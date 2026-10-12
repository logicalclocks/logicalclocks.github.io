"""MkDocs build hook for the release notes site (``mkdocs.releases.yml``).

Its ``docs_dir`` is ``docs/releases``, so the stylesheets, scripts, logo and
favicon the inherited config points at are outside it; this adds them from ``docs/``.
"""

from __future__ import annotations

import os

from mkdocs.structure.files import File


def on_files(files, *, config):
    docs = os.path.join(os.path.dirname(config.config_file_path), "docs")
    shared = [
        *config.extra_css,
        *(str(script) for script in config.extra_javascript),
        config.theme["logo"],
        config.theme["favicon"],
    ]
    for path in shared:
        files.append(File(path, docs, config.site_dir, config.use_directory_urls))
    return files
