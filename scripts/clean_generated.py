#!/usr/bin/env python3
"""Remove rebuildable local products while retaining experiment evidence."""

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def candidates():
    # build now also contains the pinned OSS CAD Suite and private staged keys.
    # Never delete that directory wholesale or remove an installed toolchain.
    for parent in (ROOT / "scripts", ROOT / "tests"):
        yield parent / "__pycache__"
    for parent in (ROOT, ROOT / "results", ROOT / "project_background_reading"):
        yield parent / ".DS_Store"
    for parent in (ROOT / "results", ROOT / "build"):
        if not parent.exists():
            continue
        for path in parent.rglob("*"):
            if parent.name == 'build' and any(p in {'tools', 'private'} for p in path.relative_to(parent).parts):
                continue
            if path.is_dir() and path.name in {
                "verilator-build", "plot-cache", "mplconfig", "cache"
            }:
                yield path
            elif path.is_file() and path.suffix == '.vvp':
                yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="delete listed paths")
    parser.add_argument("--manifest", type=Path, help="save exact removal inventory")
    args = parser.parse_args()
    found = sorted({path for path in candidates() if path.exists()}, key=str)
    records = []
    for path in found:
        size = sum(p.stat().st_size for p in path.rglob('*') if p.is_file() and not p.is_symlink()) if path.is_dir() else path.stat().st_size
        records.append({'path': str(path.relative_to(ROOT)), 'bytes': size,
                        'reason': 'rebuildable compiler product or cache', 'removed': args.apply})
        print(f"{'remove' if args.apply else 'would remove'} {path.relative_to(ROOT)}")
        if args.apply:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
    print(f"{len(found)} generated paths {'removed' if args.apply else 'found'}")
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps({'applied': args.apply, 'bytes': sum(r['bytes'] for r in records),
                                             'records': records}, indent=2)+'\n')


if __name__ == "__main__":
    main()
