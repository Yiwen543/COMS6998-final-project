#!/usr/bin/env python3
"""Build a clearly labeled, behavior-preserving FIFO redundancy stress case.

This is a synthetic *variant* of the pinned ZipCPU FIFO, never a claim that
these repeated deep guards occur in the original source. The source-level
transformations are checked later with formal equivalence.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from run_sfifo_fixed import EXPECTED_SOURCE_SHA, ROOT, SOURCE

DEST = ROOT / "examples/heldout_sfifo_stress/rtl/sfifo.v"


def change(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise AssertionError(f"Expected one transformation site: {old[:50]!r}")
    return source.replace(old, new)


def build() -> str:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SOURCE_SHA:
        raise AssertionError("Pinned original FIFO source changed")
    source = SOURCE.read_text()
    source = change(source,
        "\t2'b10: o_fill <= o_fill + 1;",
        "\t2'b10: begin\n"
        "\t\tif (o_fill == {1'b0, {LGFLEN{1'b1}}}) o_fill <= FLEN;\n"
        "\t\telse o_fill <= o_fill + 1;\n"
        "\tend")
    source = change(source,
        "\telse if (w_wr)\n\t\twr_addr <= wr_addr + 1'b1;",
        "\telse case ({ w_wr, w_rd })\n"
        "\t2'b10: begin\n"
        "\t\tif (!(o_fill != {1'b0, {LGFLEN{1'b1}}}))\n"
        "\t\t\twr_addr <= wr_addr - {(LGFLEN+1){1'b1}};\n"
        "\t\telse wr_addr <= wr_addr + 1'b1;\n"
        "\tend\n"
        "\t2'b11: wr_addr <= wr_addr + 1'b1;\n"
        "\tdefault: begin end\n"
        "\tendcase")
    source = change(source,
        "\t2'b10: r_empty <= 1'b0;",
        "\t2'b10: begin\n"
        "\t\tif (o_fill == {1'b0, {LGFLEN{1'b1}}}) r_empty <= (o_fill == 0);\n"
        "\t\telse r_empty <= 1'b0;\n"
        "\tend")
    source = change(source,
        "\t2'b01: o_fill <= o_fill - 1;",
        "\t2'b01: begin\n"
        "\t\tif (rd_addr[LGFLEN-1:0] == {LGFLEN{1'b1}})\n"
        "\t\t\to_fill <= o_fill + {(LGFLEN+1){1'b1}};\n"
        "\t\telse o_fill <= o_fill - 1;\n"
        "\tend")
    source = change(source,
        "\telse if (w_rd)\n\t\trd_addr <= rd_addr + 1;",
        "\telse case ({ w_wr, w_rd })\n"
        "\t2'b01: begin\n"
        "\t\tif (!(rd_addr[LGFLEN-1:0] != {LGFLEN{1'b1}}))\n"
        "\t\t\trd_addr <= rd_addr - {(LGFLEN+1){1'b1}};\n"
        "\t\telse rd_addr <= rd_addr + 1;\n"
        "\tend\n"
        "\t2'b11: rd_addr <= rd_addr + 1;\n"
        "\tdefault: begin end\n"
        "\tendcase")
    return source


if __name__ == "__main__":
    rendered = build()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists() and DEST.read_text() != rendered:
        raise AssertionError("Generated FIFO variant differs from pinned recipe")
    DEST.write_text(rendered)
    print(f"{DEST.relative_to(ROOT)} sha256={hashlib.sha256(DEST.read_bytes()).hexdigest()}")
