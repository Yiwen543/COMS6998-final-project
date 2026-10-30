#!/usr/bin/env python3
"""Remove rebuildable local products while retaining experiment evidence."""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def candidates():
    yield ROOT / "build"
    yield ROOT / "egraph" / "target"
    for parent in (ROOT / "scripts", ROOT / "tests"):
        yield parent / "__pycache__"
    for parent in (ROOT, ROOT / "results", ROOT / "project_background_reading"):
        yield parent / ".DS_Store"
    results = ROOT / "results"
    if results.exists():
        for path in results.rglob("*"):
            if path.is_dir() and path.name in {
                "verilator-build", "plot-cache", "mplconfig", "cache"
            }:
                yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="delete listed paths")
    args = parser.parse_args()
    found = sorted({path for path in candidates() if path.exists()}, key=str)
    for path in found:
        print(f"{'remove' if args.apply else 'would remove'} {path.relative_to(ROOT)}")
        if args.apply:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
    print(f"{len(found)} generated paths {'removed' if args.apply else 'found'}")


if __name__ == "__main__":
    main()
