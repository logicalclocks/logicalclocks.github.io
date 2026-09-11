"""Generate the REST API status code reference page from RESTCodes.java.

``RESTCodes.java`` (in the ``hopsworks-ee`` product repo, not this one) defines
one Java enum per resource category, each implementing ``RESTErrorCode``.
Every constant has the shape ``NAME(id, "message", Response.Status.STATUS)``
and its resolved numeric code is ``range + id``, where ``range`` is a
category-wide ``private static final int`` field.

This script parses that file with regexes (no Java toolchain involved) and
writes one table per category into the page, between the
``<!-- BEGIN GENERATED -->`` / ``<!-- END GENERATED -->`` markers, mirroring
the injection pattern used by ``gen_helm_values`` in ``helm_values.py``.

Stdlib only, on purpose: this is a source-parsing text transform, not a
network client or a YAML consumer, so it carries no dependency on the ``cli``
extra and can run with a bare ``python3``.

Usage:
    python3 scripts/gen_error_codes.py --source /path/to/RESTCodes.java
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


_DEFAULT_PAGE = Path(__file__).resolve().parent.parent / "docs" / "reference" / (
    "rest_error_codes.md"
)
_BEGIN = "<!-- BEGIN GENERATED -->"
_END = "<!-- END GENERATED -->"

# The nested `Status` enum implements Response.StatusType (a shim for a
# status jakarta.ws.rs.core.Response.Status does not define, e.g. 422) but it
# is not itself a RESTErrorCode and carries no error codes, so it is excluded
# by construction: the enum-header regex below requires "implements
# RESTErrorCode", which `Status` does not.
_ENUM_HEADER = re.compile(r"public enum (\w+) implements RESTErrorCode \{")
_RANGE = re.compile(r"range\s*=\s*(\d+)")
_CONST_HEAD = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)$", re.DOTALL)
_STRING_LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"')

# jakarta.ws.rs.core.Response.Status values actually referenced in
# RESTCodes.java, plus the one custom code (UNPROCESSABLE_ENTITY, 422) the
# file defines itself via its own nested `Status` enum because the jakarta
# enum has no 422 member. Kept as an explicit map (not http.HTTPStatus)
# because JAX-RS names do not all match Python's http.HTTPStatus names.
_HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "NO_CONTENT": 204,
    "NOT_MODIFIED": 304,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "METHOD_NOT_ALLOWED": 405,
    "CONFLICT": 409,
    "PRECONDITION_FAILED": 412,
    "EXPECTATION_FAILED": 417,
    "UNPROCESSABLE_ENTITY": 422,  # custom `Status`, not Response.Status
    "TOO_MANY_REQUESTS": 429,
    "INTERNAL_SERVER_ERROR": 500,
    "NOT_IMPLEMENTED": 501,
    "BAD_GATEWAY": 502,
    "SERVICE_UNAVAILABLE": 503,
}

_JAVA_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}


class ParseError(RuntimeError):
    """Raised when RESTCodes.java does not match the expected shape."""


def _strip_comments(text: str) -> str:
    """Remove // and /* */ comments, leaving string literals untouched.

    None of the string literals in RESTCodes.java contain "//" or "/*" (the
    only file lines with a "//" are outside enum bodies or genuine line
    comments), so a single string-aware pass is enough.
    """
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
            i = n if j == -1 else j
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _split_top_level(text: str, sep: str) -> list[str]:
    """Split on `sep` only at paren-depth 0 and outside string literals."""
    parts: list[str] = []
    depth = 0
    in_string = False
    current: list[str] = []
    for c in text:
        if in_string:
            current.append(c)
            if c == "\\":
                continue
            if c == '"':
                in_string = False
            continue
        if c == '"':
            in_string = True
            current.append(c)
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == sep and depth == 0:
            parts.append("".join(current))
            current = []
            continue
        current.append(c)
    parts.append("".join(current))
    return parts


def _unescape_java(literal: str) -> str:
    out: list[str] = []
    i, n = 0, len(literal)
    while i < n:
        c = literal[i]
        if c == "\\" and i + 1 < n:
            out.append(_JAVA_ESCAPES.get(literal[i + 1], literal[i + 1]))
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _extract_message(expr: str) -> str:
    """Concatenate the string literals in a `"a" + "b" + "c"` expression."""
    return "".join(_unescape_java(m) for m in _STRING_LITERAL.findall(expr))


def _resolve_status(expr: str) -> tuple[str, int | None]:
    expr = expr.strip()
    if expr == "null":
        # GenericErrorCode.WEBAPPLICATION passes a literal `null`: the actual
        # HTTP status is set at runtime from the wrapped WebApplicationException
        # rather than fixed at declaration time, so there is no status to show.
        return "dynamic (from wrapped exception)", None
    name = expr.rsplit(".", 1)[-1]
    if name not in _HTTP_STATUS:
        msg = f"unknown status expression: {expr!r}"
        raise ParseError(msg)
    return name, _HTTP_STATUS[name]


class Constant:
    __slots__ = ("name", "code", "status_name", "status_code", "message")

    def __init__(
        self,
        name: str,
        code: int,
        status_name: str,
        status_code: int | None,
        message: str,
    ) -> None:
        self.name = name
        self.code = code
        self.status_name = status_name
        self.status_code = status_code
        self.message = message


class Category:
    __slots__ = ("enum_name", "range", "has_range", "constants")

    def __init__(self, enum_name: str, range_: int, has_range: bool) -> None:
        self.enum_name = enum_name
        self.range = range_
        self.has_range = has_range
        self.constants: list[Constant] = []


def parse_categories(source: str) -> list[Category]:
    clean = _strip_comments(source)
    categories: list[Category] = []
    for header in _ENUM_HEADER.finditer(clean):
        enum_name = header.group(1)
        brace = clean.index("{", header.end() - 1)
        end = clean.index("\n  }", brace)
        body = clean[brace + 1 : end]

        range_match = _RANGE.search(body)
        has_range = range_match is not None
        range_value = int(range_match.group(1)) if range_match else 0
        category = Category(enum_name, range_value, has_range)

        # The constants section runs from the top of the body to the first
        # top-level ';' (the one that ends the enum-constant list, before any
        # field declarations).
        depth = 0
        in_string = False
        term = len(body)
        for i, c in enumerate(body):
            if in_string:
                if c == "\\":
                    continue
                if c == '"':
                    in_string = False
                continue
            if c == '"':
                in_string = True
                continue
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == ";" and depth == 0:
                term = i
                break
        const_text = body[:term]

        for chunk in _split_top_level(const_text, ","):
            chunk = chunk.strip()
            if not chunk:
                continue
            head_match = _CONST_HEAD.match(chunk)
            if head_match is None:
                msg = f"{enum_name}: cannot parse constant {chunk[:80]!r}"
                raise ParseError(msg)
            const_name, args = head_match.groups()
            arg_parts = _split_top_level(args, ",")
            if len(arg_parts) != 3:
                msg = (
                    f"{enum_name}.{const_name}: expected 3 constructor args, "
                    f"got {len(arg_parts)}"
                )
                raise ParseError(msg)
            id_expr, message_expr, status_expr = arg_parts
            id_expr = id_expr.strip()
            if not re.fullmatch(r"\d+", id_expr):
                msg = f"{enum_name}.{const_name}: non-numeric id {id_expr!r}"
                raise ParseError(msg)
            const_id = int(id_expr)
            status_name, status_code = _resolve_status(status_expr)
            message = _extract_message(message_expr).strip()
            code = range_value + const_id
            category.constants.append(
                Constant(const_name, code, status_name, status_code, message)
            )
        categories.append(category)
    return categories


def _escape_cell(text: str) -> str:
    """Make message text safe as a single Markdown table cell.

    Escapes square brackets so messages that happen to contain them (e.g. a
    regex like ``[a-zA-Z0-9]((?!__)[_a-zA-Z0-9]){0,62}`` in a validation
    error) are not parsed as Markdown reference-link syntax, which otherwise
    mangles the cell into a broken `<a href=...>` in the rendered page. None
    of these messages contain genuine Markdown links, so escaping is
    unconditional (contrast with helm_values.py, which must preserve real
    links in its input).
    """
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("[", "\\[").replace("]", "\\]")
    return text.replace("|", "\\|")


def render_table(category: Category) -> str:
    rows = sorted(category.constants, key=lambda c: c.code)
    lines = [
        "| Code | Name | HTTP status | Message |",
        "| --- | --- | --- | --- |",
    ]
    for c in rows:
        message = _escape_cell(c.message)
        status = (
            f"{c.status_code} {c.status_name}"
            if c.status_code is not None
            else c.status_name
        )
        lines.append(f"| {c.code} | `{c.name}` | {status} | {message} |")
    return "\n".join(lines)


def render_body(categories: list[Category]) -> str:
    # SchemaRegistryErrorCode does not follow the range convention (it mirrors
    # Confluent Schema Registry's own 5-digit codes), so the numerically
    # sorted categories go first and it is footnoted at the end instead of
    # sorting in at range 0, which would be misleading.
    ranged = sorted(
        (cat for cat in categories if cat.has_range), key=lambda cat: cat.range
    )
    unranged = [cat for cat in categories if not cat.has_range]

    sections: list[str] = []
    for cat in ranged + unranged:
        sections.append(f"## {cat.enum_name}\n")
        if not cat.has_range:
            sections.append(
                "This category does not follow the 6-digit convention "
                "described at the top of this page; it mirrors the "
                "Confluent Schema Registry's own error codes instead.\n"
            )
        sections.append(render_table(cat))
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def generate(source_path: Path, page_path: Path) -> int:
    source = source_path.read_text(encoding="utf-8")
    categories = parse_categories(source)
    total = sum(len(cat.constants) for cat in categories)

    body = render_body(categories)

    page_text = page_path.read_text(encoding="utf-8")
    if _BEGIN not in page_text or _END not in page_text:
        msg = f"injection markers ({_BEGIN} / {_END}) not found in {page_path}"
        raise ParseError(msg)
    head = page_text[: page_text.index(_BEGIN) + len(_BEGIN)]
    tail = page_text[page_text.index(_END) :]
    page_path.write_text(f"{head}\n\n{body}\n{tail}")
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        required=True,
        type=Path,
        help=(
            "Path to RESTCodes.java in a hopsworks-ee checkout "
            "(io/hops/hopsworks/restutils/RESTCodes.java)."
        ),
    )
    parser.add_argument(
        "--page",
        type=Path,
        default=_DEFAULT_PAGE,
        help="Reference page to inject the generated tables into.",
    )
    args = parser.parse_args()

    total = generate(args.source, args.page)
    print(f"Wrote {total} status codes across their categories to {args.page}")


if __name__ == "__main__":
    main()
