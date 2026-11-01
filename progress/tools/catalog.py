"""Check archive annotations and completeness; refresh hashes after intentional edits."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"


def inspect(refresh):
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported catalog schema")
    entries = data["files"]
    names = set()
    errors = []
    for entry in entries:
        for key in ("path", "kind", "purpose", "source", "status", "usage"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ValueError(f"Missing annotation {key}: {entry.get('path')}")
        for key in ("related_versions", "depends_on"):
            if not isinstance(entry.get(key), list) or not all(isinstance(v, str) for v in entry[key]):
                raise ValueError(f"Expected strings in {key}: {entry['path']}")
        name = entry["path"]
        rel = PurePosixPath(name)
        if rel.is_absolute() or ".." in rel.parts or str(rel) != name or name == "catalog.json":
            raise ValueError(f"Invalid archive path: {name}")
        if name in names:
            errors.append(f"Duplicate path: {name}")
        names.add(name)
    actual = set()
    for path in ROOT.rglob("*"):
        name = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            errors.append(f"Store actual files instead of symlinks: {name}")
        elif path.is_file() and path != CATALOG:
            actual.add(name)
    errors.extend(f"Unannotated file: {name}" for name in sorted(actual - names))
    errors.extend(f"File absent; register in missing: {name}" for name in sorted(names - actual))
    for entry in entries:
        for dependency in entry["depends_on"]:
            if dependency not in names:
                errors.append(f"Unregistered dependency for {entry['path']}: {dependency}")
    if errors:
        raise ValueError("\n".join(errors))
    for entry in entries:
        path = ROOT / entry["path"]
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        current = {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}
        if refresh:
            entry.update(current)
        elif any(entry.get(k) != v for k, v in current.items()):
            errors.append(f"Size/hash differs: {entry['path']}")
    if errors:
        raise ValueError("\n".join(errors))
    if refresh:
        CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{'Refreshed' if refresh else 'Verified'} {len(entries)} annotated files; "
          f"{len(data.get('missing', []))} missing-resource records. Media quality is checked separately.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    try:
        inspect(args.refresh)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
