"""Generate the cluster configuration variables reference page.

Parses the Hopsworks server-side Java sources that declare cluster
configuration keys (no Java build involved, only text parsing) and writes a
Markdown table between injection markers in
``docs/setup_installation/admin/configuration_reference.md``.

Four sources are unioned:

- ``Settings.java`` (``HopsworksSettingKeys`` enum) -- the bulk of the keys,
  each with an explicit ``Type.class`` and either a 2-arg constructor
  (``NAME("default", Type.class)``, DB key = ``name().toLowerCase()``) or a
  3-arg constructor (``NAME("legacy_key", "default", Type.class)``, DB key =
  the explicit override).
- ``CAConf.java`` (``CAConfKeys`` enum) -- ``NAME("key", "default")``, no type.
- ``KubeSettings.java`` (``KubeSettingKeys`` enum) -- same shape as CAConf.
- ``VariablesHelper.java`` -- keys are ``private static final String``
  constants; their defaults live at the ``getStrValue``/``getIntValue`` call
  sites instead of next to the declaration, so those call sites are parsed
  separately.

Some defaults are Java expressions, not literals (e.g.
``Long.toString(HdfsConstants.QUOTA_DONT_SET)``, a reference to a constant in
a class this script never loads). Guessing the runtime value would be
dishonest, so those are only resolved when every token is either a quoted
string literal or a same-file ``private static final String`` constant
(pure, file-local, deterministic); anything else is emitted as the raw
expression and flagged "computed" rather than guessed.

Run from a checkout with ``hopsworks-ee`` as a sibling directory of this repo
(override with ``--hopsworks-ee`` otherwise).
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


_DEFAULT_PAGE = (
    _DOCS_ROOT / "docs" / "setup_installation" / "admin" / "configuration_reference.md"
)
_DEFAULT_HOPSWORKS_EE = _DOCS_ROOT.parent / "hopsworks-ee"
_BEGIN = "<!-- BEGIN GENERATED -->"
_END = "<!-- END GENERATED -->"

_SETTINGS_REL = (
    "hopsworks-common/src/main/java/io/hops/hopsworks/common/util/Settings.java"
)
_CACONF_REL = (
    "hopsworks-ca/src/main/java/io/hops/hopsworks/ca/configuration/CAConf.java"
)
_KUBESETTINGS_REL = (
    "hopsworks-kube-client/src/main/java/io/hops/hopsworks/kube/client/utils/"
    "KubeSettings.java"
)
_VARIABLESHELPER_REL = (
    "hopsworks-audit/src/main/java/io/hops/hopsworks/audit/helper/VariablesHelper.java"
)

_SETTINGS_SOURCE = "Settings.java"
_CACONF_SOURCE = "CAConf.java"
_KUBESETTINGS_SOURCE = "KubeSettings.java"
_VARIABLESHELPER_SOURCE = "VariablesHelper.java"


@dataclass(frozen=True)
class ConfigVar:
    """A single cluster configuration key, as declared in one source file."""

    key: str
    type_: str
    default: str
    computed: bool
    source: str


# --- Java-source-aware text plumbing -----------------------------------
# These are intentionally small and generic: comment/string-aware scanning is
# the one piece of real complexity a stdlib-only regex parser needs, since a
# naive comment-stripping regex would corrupt string literals that contain
# "//" (e.g. "https://pypi.org/...") or "/*".


def _strip_comments(text: str) -> str:
    """Blank out // and /* */ comments, leaving string literals untouched."""
    out: list[str] = []
    in_string = False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if in_string:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            out.append(c)
            i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            j = n if j == -1 else j
            out.append("\n")
            i = j
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append(" ")
            i = j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _split_top_level(text: str, sep: str) -> list[str]:
    """Split on ``sep`` at paren-depth 0, outside string literals."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if in_string:
            current.append(c)
            if c == "\\" and i + 1 < n:
                current.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
            current.append(c)
            i += 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif text.startswith(sep, i) and depth == 0:
            parts.append("".join(current))
            current = []
            i += len(sep)
            continue
        current.append(c)
        i += 1
    parts.append("".join(current))
    return parts


def _find_enum_body(clean: str, enum_name: str) -> str:
    """Return the enum-constant list text, up to (excluding) its terminating ';'.

    ``clean`` must already be comment-stripped (see ``_strip_comments``) so
    indices line up with the depth/string scan below.
    """
    marker_idx = clean.index(f"enum {enum_name}")
    brace_idx = clean.index("{", marker_idx)
    body_start = brace_idx + 1
    depth = 0
    in_string = False
    i, n = body_start, len(clean)
    while i < n:
        c = clean[i]
        if in_string:
            if c == "\\" and i + 1 < n:
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == ";" and depth == 0:
            return clean[body_start:i]
        i += 1
    msg = f"could not find end of enum {enum_name} body"
    raise ValueError(msg)


def _local_string_consts(clean: str) -> dict[str, str]:
    """Map ``private static final String NAME = "literal";`` -> literal.

    Used to resolve defaults that reference another constant declared in the
    same file (e.g. VariablesHelper's ``DEFAULT_DATE_FORMAT``) without
    reaching outside the parsed source.
    """
    pattern = re.compile(
        r'private\s+static\s+final\s+String\s+(\w+)\s*=\s*"([^"]*)"\s*;'
    )
    return dict(pattern.findall(clean))


def _resolve_default(expr: str, local_consts: dict[str, str]) -> tuple[str, bool]:
    """Resolve a default-value expression to a display string.

    Returns ``(value, computed)``. Only resolves expressions built purely
    from quoted string literals and same-file constants (joined by ``+``);
    anything referencing an external class/enum/method is returned verbatim
    with ``computed=True`` rather than guessed.
    """
    expr = expr.strip()
    literal = re.fullmatch(r'"((?:[^"\\]|\\.)*)"', expr)
    if literal:
        return literal.group(1), False
    # Bare numeric literals (e.g. VariablesHelper's getIntValue(KEY, 256000000))
    # are literals too, not just quoted strings -- only Settings.java-style
    # enums always quote their defaults regardless of declared type.
    if re.fullmatch(r"-?\d+(\.\d+)?", expr):
        return expr, False

    tokens = _split_top_level(expr, "+")
    resolved: list[str] = []
    for token in tokens:
        token = token.strip()
        m = re.fullmatch(r'"((?:[^"\\]|\\.)*)"', token)
        if m:
            resolved.append(m.group(1))
            continue
        if re.fullmatch(r"\w+", token) and token in local_consts:
            resolved.append(local_consts[token])
            continue
        return expr, True
    return "".join(resolved), False


# --- Settings.java (2/3-arg, typed) --------------------------------------


def _parse_settings(text: str, source: str) -> list[ConfigVar]:
    clean = _strip_comments(text)
    local_consts = _local_string_consts(clean)
    body = _find_enum_body(clean, "HopsworksSettingKeys")
    entries = _split_top_level(body, ",")

    results: list[ConfigVar] = []
    for raw_entry in entries:
        entry = " ".join(raw_entry.split())
        if not entry:
            continue
        m = re.fullmatch(r"(\w+)\((.*)\)", entry)
        if not m:
            msg = f"unrecognized Settings.java enum entry: {entry!r}"
            raise ValueError(msg)
        name, args_text = m.group(1), m.group(2)
        args = _split_top_level(args_text, ",")
        args = [a.strip() for a in args]
        if len(args) == 2:
            key_arg, default_arg, type_arg = None, args[0], args[1]
        elif len(args) == 3:
            key_arg, default_arg, type_arg = args[0], args[1], args[2]
        else:
            msg = f"unexpected arity for Settings.java entry {name}: {args!r}"
            raise ValueError(msg)

        type_m = re.search(r"(\w+)\.class$", type_arg)
        type_name = type_m.group(1) if type_m else type_arg

        if key_arg is None:
            db_key = name.lower()
        else:
            key_literal, key_computed = _resolve_default(key_arg, local_consts)
            db_key = key_literal if not key_computed else key_arg

        default_val, computed = _resolve_default(default_arg, local_consts)
        results.append(ConfigVar(db_key, type_name, default_val, computed, source))
    return results


# --- CAConf.java / KubeSettings.java (2-arg, untyped) --------------------


def _parse_simple_key_default_enum(
    text: str, enum_name: str, source: str
) -> list[ConfigVar]:
    clean = _strip_comments(text)
    local_consts = _local_string_consts(clean)
    body = _find_enum_body(clean, enum_name)
    entries = _split_top_level(body, ",")

    results: list[ConfigVar] = []
    for raw_entry in entries:
        entry = " ".join(raw_entry.split())
        if not entry:
            continue
        m = re.fullmatch(r"(\w+)\((.*)\)", entry)
        if not m:
            msg = f"unrecognized {enum_name} enum entry: {entry!r}"
            raise ValueError(msg)
        _name, args_text = m.group(1), m.group(2)
        args = [a.strip() for a in _split_top_level(args_text, ",")]
        if len(args) != 2:
            msg = f"unexpected arity for {enum_name} entry {_name}: {args!r}"
            raise ValueError(msg)
        key_literal, key_computed = _resolve_default(args[0], local_consts)
        db_key = key_literal if not key_computed else args[0]
        default_val, computed = _resolve_default(args[1], local_consts)
        # These enums declare `key` and `defaultValue` as plain String fields;
        # there is no type metadata to derive from the declaration itself.
        results.append(ConfigVar(db_key, "String", default_val, computed, source))
    return results


# --- VariablesHelper.java (key constants + separate call-site defaults) --


def _parse_variables_helper(text: str, source: str) -> list[ConfigVar]:
    clean = _strip_comments(text)
    local_consts = _local_string_consts(clean)
    call_re = re.compile(r"get(Str|Int)Value\(\s*(\w+)\s*,\s*(.+?)\)\s*;")

    results: list[ConfigVar] = []
    for kind, const_name, default_expr in call_re.findall(clean):
        if const_name not in local_consts:
            msg = f"VariablesHelper call site references unknown constant {const_name}"
            raise ValueError(msg)
        db_key = local_consts[const_name]
        default_val, computed = _resolve_default(default_expr, local_consts)
        type_name = "String" if kind == "Str" else "Integer"
        results.append(ConfigVar(db_key, type_name, default_val, computed, source))
    return results


# --- Markdown rendering ---------------------------------------------------


def _md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _default_cell(value: str, computed: bool) -> str:
    if computed:
        return f"`{_md_escape(value)}` *(computed expression, not a literal)*"
    if value == "":
        return "*(empty string)*"
    return f"`{_md_escape(value)}`"


def _render_table(configs: list[ConfigVar]) -> str:
    by_key: dict[str, list[ConfigVar]] = {}
    for cv in configs:
        by_key.setdefault(cv.key, []).append(cv)

    lines = [
        "| Key | Type | Default | Source module |",
        "| --- | --- | --- | --- |",
    ]
    for cv in sorted(configs, key=lambda c: (c.key, c.source)):
        group = by_key[cv.key]
        default_cell = _default_cell(cv.default, cv.computed)
        if len(group) > 1:
            others = sorted({g.source for g in group if g is not cv})
            defaults = {g.default for g in group}
            divergence = "match" if len(defaults) == 1 else "diverge"
            default_cell += (
                f" *(duplicate key, also declared in {', '.join(others)}; "
                f"values {divergence})*"
            )
        lines.append(
            f"| `{_md_escape(cv.key)}` | {cv.type_} | {default_cell} | {cv.source} |"
        )
    return "\n".join(lines)


def gen_config_vars(
    hopsworks_ee: Annotated[
        Path,
        typer.Option(help="Path to a hopsworks-ee checkout (source of truth)."),
    ] = _DEFAULT_HOPSWORKS_EE,
    page: Annotated[
        Path,
        typer.Option(help="Reference page to inject the generated table into."),
    ] = _DEFAULT_PAGE,
) -> None:
    """Parse the Hopsworks Java settings sources and inject the reference table.

    Reads (never writes) ``Settings.java``, ``CAConf.java``,
    ``KubeSettings.java``, and ``VariablesHelper.java`` from ``hopsworks_ee``,
    unions their declared configuration keys, and writes the result as a
    Markdown table between the injection markers in ``page``. Fails loudly
    (rather than silently skipping) if a source file is missing or its shape
    no longer matches what this parser expects, since a partially-generated
    reference page is worse than a build failure that says why.
    """
    settings_path = hopsworks_ee / _SETTINGS_REL
    caconf_path = hopsworks_ee / _CACONF_REL
    kubesettings_path = hopsworks_ee / _KUBESETTINGS_REL
    variableshelper_path = hopsworks_ee / _VARIABLESHELPER_REL
    for path in (settings_path, caconf_path, kubesettings_path, variableshelper_path):
        if not path.is_file():
            msg = f"source file not found: {path}"
            raise typer.BadParameter(msg)

    configs = [
        *_parse_settings(settings_path.read_text(encoding="utf-8"), _SETTINGS_SOURCE),
        *_parse_simple_key_default_enum(
            caconf_path.read_text(encoding="utf-8"), "CAConfKeys", _CACONF_SOURCE
        ),
        *_parse_simple_key_default_enum(
            kubesettings_path.read_text(encoding="utf-8"),
            "KubeSettingKeys",
            _KUBESETTINGS_SOURCE,
        ),
        *_parse_variables_helper(
            variableshelper_path.read_text(encoding="utf-8"), _VARIABLESHELPER_SOURCE
        ),
    ]

    table = _render_table(configs)

    content = page.read_text()
    if _BEGIN not in content or _END not in content:
        msg = f"Injection markers ({_BEGIN} / {_END}) not found in {page}"
        raise typer.BadParameter(msg)
    head = content[: content.index(_BEGIN) + len(_BEGIN)]
    tail = content[content.index(_END) :]
    page.write_text(f"{head}\n\n{table}\n\n{tail}")

    by_source: dict[str, int] = {}
    for cv in configs:
        by_source[cv.source] = by_source.get(cv.source, 0) + 1
    computed_count = sum(1 for cv in configs if cv.computed)
    sources_by_key: dict[str, set[str]] = {}
    for cv in configs:
        sources_by_key.setdefault(cv.key, set()).add(cv.source)
    dup_keys = {key for key, srcs in sources_by_key.items() if len(srcs) > 1}

    typer.echo(f"Total keys emitted: {len(configs)}")
    for src, count in by_source.items():
        typer.echo(f"  {src}: {count}")
    typer.echo(f"Computed-default rows: {computed_count}")
    typer.echo(f"Duplicate keys (declared in >1 source): {len(dup_keys)}")
    if dup_keys:
        typer.echo(f"  {', '.join(sorted(dup_keys))}")
