#!/usr/bin/env python3
"""Parse Wolfenstein 3D asset-enumeration headers in WOLFSRC/ into flat tables.

Source of truth is the original id Software headers (IGRAB / MUSE / TED5 output).
Emits CSV + JSON into this directory. Re-runnable; no third-party deps.
"""
import csv
import json
import os
import re

SRC = os.path.join(os.path.dirname(__file__), "..", "WOLFSRC")
OUT = os.path.dirname(__file__)

# ---- header -> (product set, kind) -----------------------------------------
GRAPHICS = [
    ("GFXV_WL6.H", "WL6", "vga"),
    ("GFXV_WL1.H", "WL1", "vga"),
    ("GFXV_SOD.H", "SOD", "vga"),
    ("GFXV_SDM.H", "SDM", "vga"),
    ("GFXE_WL1.H", "WL1", "ega"),
    ("GFXE_WL6.H", "WL6", "ega"),
    ("GFXE_SOD.H", "SOD", "ega"),
]
AUDIO = [
    ("AUDIOWL1.H", "WL1"),
    ("AUDIOWL6.H", "WL6"),
    ("AUDIOSOD.H", "SOD"),
    ("AUDIOSDM.H", "SDM"),
]
MAPS = [
    ("MAPSWL6.H", "WL6"),
    ("MAPSWL1.H", "WL1"),
    ("MAPSSOD.H", "SOD"),
    ("MAPSSDM.H", "SDM"),
    ("MAPSWLF.H", "WLF"),
]

ENTRY = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:=\s*(\d+))?\s*,?\s*(?://\s*(.*))?$")
STOP = {"ENUMEND", "LASTSOUND", "LASTMUSIC", "LASTMAP"}


def parse_enum_lines(path):
    """Yield (id, symbol, note) preserving authored // numbering when present."""
    nxt = 0
    with open(path, "r", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("//") or line.startswith("#"):
                continue
            if line.startswith("}") or line.startswith("typedef"):
                continue
            m = ENTRY.match(raw)
            if not m:
                continue
            sym, num, note = m.group(1), m.group(2), (m.group(3) or "").strip()
            if sym in STOP:
                break
            if num is not None and num != "":
                nxt = int(num)
            yield nxt, sym, note
            nxt += 1


def parse_audio(path):
    """Return (sounds, music) — the header holds two enums split by a marker."""
    sounds, music = [], []
    bucket = sounds
    nxt = 0
    with open(path, "r", errors="replace") as fh:
        for raw in fh:
            low = raw.lower()
            if "music names" in low:
                bucket = music
                nxt = 0
                continue
            line = raw.strip()
            if not line or line.startswith("//") or line.startswith("#"):
                continue
            if line.startswith("}") or line.startswith("typedef"):
                continue
            m = ENTRY.match(raw)
            if not m:
                continue
            sym, num, note = m.group(1), m.group(2), (m.group(3) or "").strip()
            if sym in STOP:
                continue
            if num is not None and num != "":
                nxt = int(num)
            bucket.append((nxt, sym, note))
            nxt += 1
    return sounds, music


def write_csv(name, rows, header):
    with open(os.path.join(OUT, name), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {name}: {len(rows)} rows")


def main():
    gfx, snd, mus, mp = [], [], [], []

    for fn, aset, kind in GRAPHICS:
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            continue
        for gid, sym, note in parse_enum_lines(path):
            gfx.append([aset, kind, gid, sym, note])

    for fn, aset in AUDIO:
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            continue
        sounds, music = parse_audio(path)
        for sid, sym, note in sounds:
            snd.append([aset, sid, sym, note])
        for mid, sym, note in music:
            mus.append([aset, mid, sym, note])

    for fn, aset in MAPS:
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            continue
        for mid, sym, note in parse_enum_lines(path):
            mp.append([aset, mid, sym, note])

    write_csv("graphics.csv", gfx, ["set", "kind", "id", "symbol", "note"])
    write_csv("sounds.csv", snd, ["set", "id", "symbol", "note"])
    write_csv("music.csv", mus, ["set", "id", "symbol", "note"])
    write_csv("maps.csv", mp, ["set", "id", "symbol", "note"])

    with open(os.path.join(OUT, "assets.json"), "w") as fh:
        json.dump(
            {
                "graphics": [
                    {"set": a, "kind": k, "id": i, "symbol": s, "note": n}
                    for a, k, i, s, n in gfx
                ],
                "sounds": [{"set": a, "id": i, "symbol": s, "note": n} for a, i, s, n in snd],
                "music": [{"set": a, "id": i, "symbol": s, "note": n} for a, i, s, n in mus],
                "maps": [{"set": a, "id": i, "symbol": s, "note": n} for a, i, s, n in mp],
            },
            fh,
            indent=1,
        )
    print("wrote assets.json")


if __name__ == "__main__":
    main()
