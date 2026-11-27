"""One-time OVizLAB v1.0.0 public release builder. Offline stdlib; no publication."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def build(root, destination):
    root, destination = Path(root).resolve(), Path(destination).resolve()
    pinned = json.loads((root / "release-v1.lock.json").read_text(encoding="utf-8"))
    if (pinned.get("schema_version") != 1
            or pinned.get("release") != "v1.0.0"
            or pinned.get("source_commit") != "debd8455a9d0293a00ea8fe7a812fa29d1073512"
            or pinned.get("skill_count") != 28):
        raise ValueError("RELEASE_LOCK_IDENTITY_INVALID")
    files = pinned.get("files")
    if not isinstance(files, dict) or len(files) != 47:
        raise ValueError("RELEASE_LOCK_INVENTORY_INVALID")
    raw = {}
    for rel, expected_blob in files.items():
        parts = rel.split("/")
        if (not rel or rel.startswith("/") or "\\" in rel
                or any(x in ("", ".", "..") for x in parts)
                or not re.fullmatch(r"[a-f0-9]{40}", expected_blob)):
            raise ValueError("UNSAFE_RELEASE_MEMBER: " + str(rel))
        item = root.joinpath(*parts)
        if item.is_symlink() or not item.is_file() or any(parent.is_symlink() for parent in item.parents if parent != root.parent):
            raise ValueError("MISSING_OR_LINKED_RELEASE_FILE: " + rel)
        data = item.read_bytes()
        if len(data) > 2_000_000 or git_blob(data) != expected_blob:
            raise ValueError("GIT_BLOB_DRIFT: " + rel)
        raw[rel] = data
    skills = sorted({x.split("/")[1] for x in raw if x.startswith("skills/")})
    if len(skills) != 28 or not all("skills/" + name + "/SKILL.md" in raw for name in skills):
        raise ValueError("SKILL_COUNT_OR_ENTRYPOINT_MISMATCH")
    manifest = {
        "schema_version": 1,
        "repository": "lutiy-dev/GitHab-Skills",
        "source_commit": pinned["source_commit"],
        "skills": skills,
        "files": {p: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
                  for p, data in sorted(raw.items()) if p.startswith("skills/")},
    }
    # Add only the canonical files from the locked public source, no repo history.
    extras = {"bundle.json": (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()}
    if not all(name in raw for name in ("install.py", "agent_installer.py",
             "auto_update.py", "ovizlab_auto_update_task.ps1", "LICENSE",
             "NOTICE", "README_FOR_AGENTS.md")):
        raise ValueError("MISSING_INSTALLER_OR_ATTRIBUTION")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted({**raw, **extras}.items()):
            item = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or len(archive.namelist()) != 48:
            raise ValueError("RELEASE_ARCHIVE_INVALID")
        content = json.loads(archive.read("bundle.json"))
        if content["source_commit"] != pinned["source_commit"] or len(content["files"]) != 35:
            raise ValueError("RELEASE_MANIFEST_INVALID")
        for rel, meta in content["files"].items():
            data = archive.read(rel)
            if meta["sha256"] != hashlib.sha256(data).hexdigest() or meta["bytes"] != len(data):
                raise ValueError("RELEASE_SKILL_HASH_MISMATCH")
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    channel = {
        "schema_version": 1,
        "repository": "lutiy-dev/OVizLAB-Skills",
        "sequence": 1,
        "source_commit": pinned["source_commit"],
        "archive_url": "https://github.com/lutiy-dev/OVizLAB-Skills/releases/download/v1.0.0/ovizlab-agent-installer.zip",
        "archive_sha256": digest,
    }
    candidate_path = destination.parent / "channel-v1.candidate.json"
    candidate_path.write_text(json.dumps(channel, indent=2) + "\n", encoding="utf-8")
    return {"status": "GENERATED_NOT_PUBLISHED", "count": len(raw) + len(extras),
            "skills": len(skills), "sha256": digest, "channel": str(candidate_path)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("USAGE: build_release_v1.py SOURCE_ROOT OUTPUT_ZIP")
    print(json.dumps(build(sys.argv[1], sys.argv[2]), indent=2))
