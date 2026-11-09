#!/usr/bin/env python3
"""Validate the distributed package without cloud access or third-party dependencies."""
import argparse
import ast
import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urlsplit

from stack import CLIENTS, NAME, PROVIDER_NAMES, ROOT, package_files, registry, render_config

# These are leak indicators, not a comprehensive secret scanner.
LEAKS = {
    "personal-home-path": re.compile(r"(?:/home/|/Users/|[A-Z]:\\Users\\)[A-Za-z0-9_.-]+"),
    "tailnet-address": re.compile(r"[A-Za-z0-9.-]+\.ts\.net\b"),
    "private-key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "resend-key": re.compile(r"\bre_[A-Za-z0-9]{24,}\b"),
    "cloud-database-url": re.compile(r"postgres(?:ql)?://[^\s]+@[^\s]*(?:neon\.tech|railway\.internal)"),
}


def frontmatter(skill):
    """Validate this package's deliberately small YAML subset; not a YAML library.

    Top-level scalars are single-line plain strings or JSON-quoted strings.
    Metadata is a two-space-indented mapping of JSON-quoted string values.
    Reject unsupported YAML rather than silently accepting malformed syntax.
    """
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
    if not match:
        raise ValueError("Missing frontmatter")
    data = {}
    in_metadata = False
    allowed = {"name", "description", "license", "compatibility", "metadata"}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and in_metadata:
            item = re.fullmatch(r"  ([a-z][a-z0-9_-]*): (.+)", line)
            if not item or item[1] in data["metadata"]:
                raise ValueError("Invalid or duplicate metadata key")
            value = json.loads(item[2])
            if not isinstance(value, str):
                raise ValueError("Metadata values must be strings")
            data["metadata"][item[1]] = value
            continue
        item = re.fullmatch(r"([a-z][a-z0-9-]*):(.*)", line)
        if not item or item[1] not in allowed or item[1] in data:
            raise ValueError("Invalid, unsupported or duplicate frontmatter key")
        key, raw = item[1], item[2].strip()
        in_metadata = key == "metadata"
        if in_metadata:
            if raw:
                raise ValueError("Metadata must use the supported mapping form")
            data[key] = {}
        else:
            if raw.startswith('"'):
                value = json.loads(raw)
                if not isinstance(value, str):
                    raise ValueError("Frontmatter must contain string scalars")
            else:
                if not raw or not re.match(r"[A-Za-z]", raw) or ": " in raw or " #" in raw or raw.lower() in {"null", "true", "false", "yes", "no", "on", "off"}:
                    raise ValueError("Unsupported plain scalar; use a JSON-quoted string")
                value = raw
            data[key] = value
    if set(data) != allowed:
        raise ValueError("Missing required package frontmatter fields")
    return data


def validate(root=ROOT):
    root = Path(root)
    errors = []
    try:
        manifest, files = package_files(root)
    except (OSError, ValueError, KeyError, TypeError):
        return ["Invalid/missing package manifest or unsafe package path"]
    if root.resolve().name != NAME:
        errors.append("Package directory must match the skill name")
    try:
        skill = files["SKILL.md"].read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        return errors + ["SKILL.md: expected readable UTF-8 text"]
    try:
        front = frontmatter(skill)
        if front["name"] != NAME:
            errors.append("SKILL.md: invalid skill name")
        if not 1 <= len(front["description"]) <= 1024:
            errors.append("SKILL.md: invalid description")
        if not 1 <= len(front["compatibility"]) <= 500:
            errors.append("SKILL.md: invalid compatibility")
        if front["metadata"].get("version") != manifest.get("version"):
            errors.append("Skill and manifest versions differ")
        if front["license"] != "MIT":
            errors.append("Missing license declaration")
    except (ValueError, KeyError, TypeError):
        errors.append("SKILL.md: invalid or unsupported package frontmatter")
    if len(skill.splitlines()) >= 500:
        errors.append("SKILL.md must remain under 500 lines")
    if manifest.get("entrypoint") != "SKILL.md":
        errors.append("Invalid entrypoint")
    for relative, path in files.items():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(relative + ": expected readable UTF-8 text")
            continue
        for label, pattern in LEAKS.items():
            if pattern.search(text):
                errors.append(relative + ": privacy indicator " + label)
        if "[SKILL_" + "PRUNED]" in text:
            errors.append(relative + ": inaccessible instruction placeholder")
        if any(line.rstrip() != line for line in text.splitlines()):
            errors.append(relative + ": trailing whitespace")
        if not text.endswith("\n"):
            errors.append(relative + ": missing final newline")
        if path.suffix == ".py":
            try:
                ast.parse(text, filename=relative)
            except SyntaxError:
                errors.append(relative + ": invalid Python")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except ValueError:
                errors.append(relative + ": invalid JSON")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text):
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                link = (path.parent / unquote(target.split("#", 1)[0])).resolve()
                if not link.is_relative_to(root.resolve()) or not link.is_file():
                    errors.append(relative + ": broken/escaping local link " + target)
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in (".git", "__pycache__") for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append(str(relative) + ": symlinks are not distributable")
        elif path.is_file() and relative.as_posix() not in files:
            errors.append(str(relative) + ": not allowlisted; review before distribution")
    try:
        providers = registry(root)
        for provider in providers.values():
            for key in ("url", "docs"):
                if not isinstance(provider.get(key), str):
                    raise ValueError("Invalid provider URL type")
                url = urlsplit(provider[key])
                if url.scheme != "https" or not url.hostname or url.username or url.password or url.query or url.fragment:
                    errors.append("Unsafe provider URL")
    except (OSError, ValueError, KeyError, TypeError):
        errors.append("Invalid provider registry or unreviewed endpoint")
    # Render the installed package's current config, not arbitrary files as code.
    if root.resolve() == ROOT.resolve():
        for client in CLIENTS:
            for transport in ("http", "stdio"):
                try:
                    text = render_config(client, PROVIDER_NAMES, railway_transport=transport)
                    tomllib.loads(text) if client == "codex" else json.loads(text)
                except (ValueError, KeyError, TypeError):
                    errors.append(client + ": generated config parse failed")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate(args.root)
    print(json.dumps({"valid": not errors, "errors": errors,
                      "scope": "package structure, syntax, links, allowlist, privacy indicators"}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
