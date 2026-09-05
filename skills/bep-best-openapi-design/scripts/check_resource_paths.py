#!/usr/bin/env python3
"""Check path structure and optionally enforce the BEP path profile."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit


FORBIDDEN_SEGMENTS = frozenset(
    {
        "accept",
        "action",
        "actions",
        "activate",
        "approve",
        "assign",
        "ban",
        "calculate",
        "cancel",
        "checkout",
        "clone",
        "close",
        "command",
        "commands",
        "confirm",
        "create",
        "deactivate",
        "delete",
        "disable",
        "dismiss",
        "enable",
        "execute",
        "generate",
        "get",
        "import",
        "list",
        "login",
        "logout",
        "open",
        "patch",
        "post",
        "publish",
        "put",
        "refresh",
        "reject",
        "reset",
        "restore",
        "retry",
        "revoke",
        "rotate",
        "run",
        "send",
        "start",
        "stop",
        "submit",
        "suspend",
        "sync",
        "trigger",
        "unban",
        "unlock",
        "unpublish",
        "update",
        "upload",
        "validate",
        "verify",
    }
)

FORBIDDEN_QUERY_KEYS = frozenset({"action", "command", "do", "method", "operation"})

FORBIDDEN_VERSION_QUERY_KEYS = frozenset(
    {"api-version", "api_version", "apiversion", "version"}
)

LITERAL_SEGMENT = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
PATH_PARAMETER = re.compile(r"^\{[a-z][A-Za-z0-9]*\}$")
PATH_VERSION_SEGMENT = re.compile(r"^v[0-9]+$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check API paths against the BEP or existing-contract profile."
    )
    parser.add_argument(
        "--profile", choices=("bep", "existing"), default="bep",
        help="bep enforces BEP style; existing checks structure without changing conventions.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="Read one API path per line.")
    source.add_argument("paths", nargs="*", help="API paths to check.")
    args = parser.parse_args()
    if args.file is None and not args.paths:
        parser.error("provide at least one API path")
    return args


def load_paths(args: argparse.Namespace) -> list[str]:
    if args.file is None:
        return args.paths

    return [
        line.strip()
        for line in args.file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def audit_path(raw_path: str, profile: str = "bep") -> list[str]:
    if profile not in {"bep", "existing"}:
        raise ValueError(f"unknown profile: {profile}")
    violations: list[str] = []
    parsed = urlsplit(raw_path)

    if parsed.scheme or parsed.netloc or not raw_path.startswith("/"):
        violations.append("provide an absolute path starting with '/', not a URL")
    if parsed.fragment:
        violations.append("API path must not contain a fragment")
    if any(char.isspace() for char in raw_path):
        violations.append("API path must not contain literal whitespace")
    if "//" in parsed.path:
        violations.append("API path must not contain an empty segment")
    path_without_parameters = re.sub(r"\{[^{}]+\}", "", parsed.path)
    if "{" in path_without_parameters or "}" in path_without_parameters:
        violations.append("path parameters must have balanced non-empty braces")

    if profile == "existing":
        return violations

    for encoded_segment in parsed.path.split("/"):
        if not encoded_segment:
            continue

        segment = unquote(encoded_segment)
        if ":" in segment:
            violations.append(f"RPC-style ':' suffix in segment {segment!r}")

        if segment.startswith("{") and segment.endswith("}"):
            if PATH_PARAMETER.fullmatch(segment) is None:
                violations.append(
                    f"path parameter {segment!r} must use lowerCamelCase"
                )
            continue

        if PATH_VERSION_SEGMENT.fullmatch(segment):
            violations.append(f"version segment {segment!r}; use API-Version header")

        if LITERAL_SEGMENT.fullmatch(segment) is None:
            violations.append(
                f"literal segment {segment!r} must use lowercase kebab-case"
            )

        if segment.casefold() in FORBIDDEN_SEGMENTS:
            violations.append(f"action-oriented segment {segment!r}")

    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
        if key.casefold() in FORBIDDEN_QUERY_KEYS:
            violations.append(f"command-selecting query parameter {key!r}")
        if key.casefold() in FORBIDDEN_VERSION_QUERY_KEYS:
            violations.append(f"version query parameter {key!r}; use API-Version header")

    return violations


def main() -> int:
    args = parse_args()
    paths = load_paths(args)
    if not paths:
        raise ValueError("no API paths found")

    failures = 0
    for path in paths:
        violations = audit_path(path, args.profile)
        for violation in violations:
            print(f"{path}: {violation}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"Resource path audit failed with {failures} violation(s).", file=sys.stderr)
        return 1

    print(f"Path check passed for {len(paths)} path(s) under {args.profile} profile; resource semantics require review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
