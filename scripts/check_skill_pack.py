#!/usr/bin/env python3
"""Check the local Phat skill pack's catalog and maintained references."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKILL_DIR = Path(".agents/skills")
MIGRATION_DOC = Path("docs/migrations/skill-identifier-migration.md")
CORE_COUNT_PATTERNS = {
    Path("AGENTS.md"): re.compile(r"current pack contains (\d+) skills", re.I),
    Path("README.md"): re.compile(r"collection contains (\d+) skills", re.I),
    Path("CONTEXT.md"): re.compile(r"repository currently contains (\d+) skills", re.I),
    Path("docs/requirement.md"): re.compile(
        r"published collection contains (\d+) installable skills", re.I
    ),
}
SKILL_REFERENCE_RE = re.compile(r"\$([a-z][a-z0-9]*(?:-[a-z0-9]+)+)")
INLINE_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.M)
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
HTML_ANCHOR_RE = re.compile(r"<a\s+(?:id|name)=['\"]([^'\"]+)['\"]", re.I)


def remove_fenced_code(text: str) -> str:
    result: list[str] = []
    fence_char: str | None = None
    fence_size = 0
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence_char is None and match:
            fence_char = match.group(1)[0]
            fence_size = len(match.group(1))
            continue
        if fence_char is not None:
            if re.match(rf"^\s{{0,3}}{re.escape(fence_char)}{{{fence_size},}}\s*$", line):
                fence_char = None
                fence_size = 0
            continue
        result.append(line)
    return "\n".join(result)


def frontmatter_fields(path: Path) -> tuple[dict[str, str], str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, "missing opening YAML frontmatter delimiter"
    end = text.find("\n---", 4)
    if end < 0:
        return {}, "missing closing YAML frontmatter delimiter"
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fields[match.group(1)] = value
    return fields, None


def migration_map(root: Path) -> dict[str, str]:
    path = root / MIGRATION_DOC
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    row = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = row.match(line)
        if match:
            result[match.group(1)] = match.group(2)
    return result


def document_status(text: str) -> str | None:
    match = re.search(r"^\s*-?\s*Status:\s*([a-z_]+)\s*$", text, re.I | re.M)
    return match.group(1).lower() if match else None


def is_active_document(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    if relative == MIGRATION_DOC or relative.parts[:2] == ("docs", "migrations"):
        return False
    if relative.parts[:2] in (("docs", "specs"), ("docs", "tasks")):
        status = document_status(path.read_text(encoding="utf-8"))
        return status != "done"
    return True


def paragraph_at(text: str, position: int) -> str:
    start = text.rfind("\n\n", 0, position) + 2
    end = text.find("\n\n", position)
    return text[start:] if end < 0 else text[start:end]


def check_retired_mentions(
    root: Path,
    path: Path,
    text: str,
    aliases: dict[str, str],
    errors: list[str],
) -> None:
    if not is_active_document(root, path):
        return
    # Ignore legacy names that occur only in a historical task filename link.
    text = re.sub(r"\]\([^)]*\)", "]()", text)
    for retired, current in aliases.items():
        pattern = re.compile(rf"(?<![A-Za-z0-9-]){re.escape(retired)}(?![A-Za-z0-9-])")
        for match in pattern.finditer(text):
            paragraph = paragraph_at(text, match.start())
            if re.search(rf"\${re.escape(retired)}\b", paragraph):
                errors.append(
                    f"{path.relative_to(root)}: active reference invokes retired skill "
                    f"${retired}; use ${current}"
                )
                continue
            has_history_label = re.search(r"historical|retired identifier|earlier identifier", paragraph, re.I)
            names_current = re.search(
                rf"(?<![A-Za-z0-9-]){re.escape(current)}(?![A-Za-z0-9-])",
                paragraph,
                re.I,
            )
            if not (has_history_label and names_current):
                errors.append(
                    f"{path.relative_to(root)}: retired identifier {retired!r} is not "
                    f"clearly labeled historical with current identifier {current!r}"
                )


def markdown_anchors(text: str) -> set[str]:
    anchors = set(HTML_ANCHOR_RE.findall(text))
    used: dict[str, int] = {}
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = match.group(2)
        heading = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"`([^`]+)`", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).lower()
        slug = re.sub(r"[^\w -]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        occurrence = used.get(slug, 0)
        anchors.add(slug if occurrence == 0 else f"{slug}-{occurrence}")
        used[slug] = occurrence + 1
    return anchors


def check_local_links(root: Path, markdown_files: list[Path], errors: list[str]) -> None:
    for source in markdown_files:
        original = source.read_text(encoding="utf-8")
        body = remove_fenced_code(original)
        links = [match.group(1).strip() for match in INLINE_LINK_RE.finditer(body)]
        links.extend(match.group(1).strip() for match in REFERENCE_LINK_RE.finditer(body))
        anchors_by_target: dict[Path, set[str]] = {}
        for raw_target in links:
            target = raw_target
            if target.startswith("<") and ">" in target:
                target = target[1 : target.index(">")]
            else:
                target = target.split(maxsplit=1)[0]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            decoded_path = unquote(parsed.path)
            target_path = (source.parent / decoded_path).resolve() if decoded_path else source.resolve()
            if not target_path.exists():
                errors.append(
                    f"{source.relative_to(root)}: local link target does not exist: {raw_target}"
                )
                continue
            fragment = unquote(parsed.fragment)
            if fragment:
                if target_path.is_dir():
                    continue
                if target_path.suffix.lower() != ".md":
                    continue
                if target_path not in anchors_by_target:
                    anchors_by_target[target_path] = markdown_anchors(
                        target_path.read_text(encoding="utf-8")
                    )
                anchors = anchors_by_target[target_path]
                if fragment not in anchors:
                    errors.append(
                        f"{source.relative_to(root)}: local link fragment not found: {raw_target}"
                    )


def markdown_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.md") if ".git" not in path.parts]


def reference_files(root: Path) -> list[Path]:
    return markdown_files(root) + [
        path for path in root.rglob("*.yaml") if ".git" not in path.parts
    ]


def check_pack(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / SKILL_DIR
    if not skills_root.is_dir():
        return [f"missing skill directory: {SKILL_DIR}"]

    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    names = {path.name for path in skill_dirs}
    if not skill_dirs:
        errors.append(f"no skill directories found under {SKILL_DIR}")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        interface_file = skill_dir / "agents" / "openai.yaml"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.relative_to(root)}: missing SKILL.md")
            continue
        if not interface_file.is_file():
            errors.append(f"{skill_dir.relative_to(root)}: missing agents/openai.yaml")
        fields, frontmatter_error = frontmatter_fields(skill_file)
        if frontmatter_error:
            errors.append(f"{skill_file.relative_to(root)}: {frontmatter_error}")
            continue
        if fields.get("name") != skill_dir.name:
            errors.append(
                f"{skill_file.relative_to(root)}: frontmatter name {fields.get('name')!r} "
                f"does not match directory {skill_dir.name!r}"
            )
        if not fields.get("description", "").strip():
            errors.append(f"{skill_file.relative_to(root)}: missing description frontmatter")

    for relative, pattern in CORE_COUNT_PATTERNS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing catalog count source: {relative}")
            continue
        counts = [int(value) for value in pattern.findall(path.read_text(encoding="utf-8"))]
        if len(counts) != 1:
            errors.append(
                f"{relative}: expected one canonical skill-count statement; found {len(counts)}"
            )
        elif counts[0] != len(skill_dirs):
            errors.append(
                f"{relative}: declares {counts[0]} skills; found {len(skill_dirs)} skill directories"
            )

    readme = root / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        catalog = re.search(r"^## Skill catalog\s*$([\s\S]*?)(?=^## |\Z)", text, re.M)
        if not catalog:
            errors.append("README.md: missing '## Skill catalog' section")
        else:
            listed = set(re.findall(r"^\|\s*`([^`]+)`\s*\|", catalog.group(1), re.M))
            if listed != names:
                missing = sorted(names - listed)
                extra = sorted(listed - names)
                errors.append(
                    "README.md: skill catalog differs from source directories; "
                    f"missing={missing}, unknown={extra}"
                )

    workflow = root / "docs/workflow.md"
    router = root / ".agents/skills/ask-workflow/SKILL.md"
    if workflow.is_file() and router.is_file():
        workflow_text = workflow.read_text(encoding="utf-8")
        category = re.search(
            r"- \*\*Workflow skills:\*\*(.*?)(?=\n- \*\*)",
            workflow_text,
            re.S,
        )
        route_section = re.search(
            r"^## Choose the route\s*$([\s\S]*?)(?=^## |\Z)",
            router.read_text(encoding="utf-8"),
            re.M,
        )
        if not category:
            errors.append("docs/workflow.md: cannot read the canonical workflow-skill list")
        elif not route_section:
            errors.append("ask-workflow: missing 'Choose the route' section")
        else:
            workflow_skills = set(re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`", category.group(1)))
            routed = set(SKILL_REFERENCE_RE.findall(route_section.group(1)))
            missing_routes = sorted((workflow_skills & names) - {"ask-workflow"} - routed)
            if missing_routes:
                errors.append(
                    "ask-workflow: missing routes for workflow skills: "
                    + ", ".join(missing_routes)
                )

    aliases = migration_map(root)
    current_docs = markdown_files(root)
    for path in reference_files(root):
        content = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".md":
            content = remove_fenced_code(content)
        check_retired_mentions(root, path, content, aliases, errors)
        for identifier in SKILL_REFERENCE_RE.findall(content):
            relative = path.relative_to(root)
            if identifier in aliases:
                continue
            if identifier not in names:
                errors.append(f"{relative}: referenced skill ${identifier} does not exist")

    check_local_links(root, current_docs, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="skill-pack repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors = check_pack(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Skill pack check failed with {len(errors)} issue(s).", file=sys.stderr)
        return 1
    count = sum(1 for path in (root / SKILL_DIR).iterdir() if path.is_dir())
    print(
        "Skill pack check passed: "
        f"{count} skills, required files, catalog counts, references, router coverage, and local Markdown links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
