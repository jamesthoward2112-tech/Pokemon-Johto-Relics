#!/usr/bin/env python3
"""Repair PNG chunk CRCs without changing pixel/chunk data.

The Azul Agua donor tiles were extracted correctly but passed through a transport
path that left stale CRC fields in otherwise valid PNG chunks. gbagfx/libpng
rejects those files. This tool rewrites only the 4-byte CRC after each chunk.
"""

from __future__ import annotations

import argparse
import struct
import zlib
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def repair(path: Path) -> None:
    data = path.read_bytes()
    if not data.startswith(PNG_SIG):
        raise SystemExit(f"{path}: not a PNG")

    out = bytearray(PNG_SIG)
    pos = len(PNG_SIG)
    saw_iend = False

    while pos < len(data):
        if pos + 12 > len(data):
            raise SystemExit(f"{path}: truncated PNG chunk header")

        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        data_start = pos + 8
        data_end = data_start + length
        crc_end = data_end + 4

        if crc_end > len(data):
            raise SystemExit(f"{path}: truncated {chunk_type!r} chunk")

        chunk_data = data[data_start:data_end]
        crc = zlib.crc32(chunk_type)
        crc = zlib.crc32(chunk_data, crc) & 0xFFFFFFFF

        out += struct.pack(">I", length)
        out += chunk_type
        out += chunk_data
        out += struct.pack(">I", crc)

        pos = crc_end
        if chunk_type == b"IEND":
            saw_iend = True
            break

    if not saw_iend:
        raise SystemExit(f"{path}: missing IEND")

    path.write_bytes(out)
    print(f"repaired PNG CRCs: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.files:
        repair(path)


if __name__ == "__main__":
    main()
