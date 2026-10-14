# Wolfenstein 3D — Generated Catalogues & Code Analysis

Machine-readable extracts of the asset enums in `../WOLFSRC/`, plus the
code↔asset relationship and the control-flow analysis. The human-readable
overview lives one level up in [`../ASSET-CATALOG.md`](../ASSET-CATALOG.md).

## Files

| File | Contents |
| --- | --- |
| [`parse_assets.py`](parse_assets.py) | Parser: reads the enum headers in `WOLFSRC/` and regenerates everything below. No third-party deps. |
| [`graphics.csv`](graphics.csv) | `set,kind,id,symbol,note` — every VGA/EGA `graphicnums` entry. |
| [`sounds.csv`](sounds.csv) | `set,id,symbol,note` — every `soundnames` entry. |
| [`music.csv`](music.csv) | `set,id,symbol,note` — every `musicnames` entry. |
| [`maps.csv`](maps.csv) | `set,id,symbol,note` — every TED5 `mapnames` entry. |
| [`assets.json`](assets.json) | Same data as the CSVs, keyed by category (`graphics`/`sounds`/`music`/`maps`). |
| [`CODE-ASSET-MAP.md`](CODE-ASSET-MAP.md) | Relational map: runtime caches, table-driven bindings, subsystem↔asset matrix, reverse map, binding diagram. |
| [`FLOWCHART.md`](FLOWCHART.md) | Order of operations: boot → attract → game/level load → per-frame → render pipeline, with Mermaid flowcharts. |
| [`FORMATS.md`](FORMATS.md) | Byte-level container formats: VSWAP page layout, VGAHEAD/VGRAPH/VGADICT, AUDIOHED/AUDIOT, MAPHEAD/GAMEMAPS, and the Huffman/Carmack/RLEW codecs. |
| [`SOUND-USAGE.md`](SOUND-USAGE.md) | Curated sound→actor/trigger map (sight/death/weapon/pickup/menu) and the digitized-voice `wolfdigimap`. |
| [`sound_usage.py`](sound_usage.py) | Parser: scans `WOLFSRC/*.C` for sound references and regenerates the raw index below. |
| [`sound-references.md`](sound-references.md) | Raw per-symbol sound reference index (`file:line`, enclosing function/table). |
| [`DATA-REQUIREMENTS.md`](DATA-REQUIREMENTS.md) | Per-set files, runtime extension selection, compile flags, and index constants. |

## Regenerating

```sh
cd catalog
python3 parse_assets.py
python3 sound_usage.py          # regenerates sound-references.md
```

The parser derives `set`/`kind` from the header it is reading, so adding a new
header only requires an entry in the `GRAPHICS` / `AUDIO` / `MAPS` lists at the
top of `parse_assets.py`.

## Row counts (current run)

| Table | Rows | Breakdown |
| --- | ---: | --- |
| graphics | 717 | WL6 vga 145 · WL1 vga 138 · WL1 ega 140 · SOD vga 165 · SDM vga 129 |
| sounds | 318 | WL6 87 · WL1 69 · SOD 81 · SDM 81 |
| music | 102 | WL6 27 · WL1 27 · SOD 24 · SDM 24 |
| maps | 118 | WL6 61 · WL1 30 · SOD 21 · SDM 2 · WLF 4 |

### Why the graphics counts exceed `NUMPICS`

The trailing block of each `graphicnums` enum (from `STARTEXTERNS` up) are
**externs** — the IGRAB "external art" group (order/error screens, help/end/
demo art). In this build (`ARTSEXTERN`/`DEMOSEXTERN` are defined in
`WOLFSRC/VERSION.H`) they are still stored as `VGRAPH` chunks and loaded with
`CA_CacheGrChunk` (`ID_CA.C:1318`; e.g. `T_HELPART` at `WL_TEXT.C:769`,
`T_DEMO0` at `WL_GAME.C:1056`, `T_ENDART1+episode` at `WL_TEXT.C:830`). The
alternate non-`ARTSEXTERN` build instead reads separate `HELPART.<ext>` /
`ENDART<n>.<ext>` files (`WL_TEXT.C:773,835`) and separate `DEMO<n>.<ext>`
files (`WL_GAME.C:1061`). Either way the compile-time enum includes them, so
`enum symbols = NUMPICS + NUMEXTERNS`:

| Set | NUMPICS | NUMEXTERNS | Symbols |
| --- | ---: | ---: | ---: |
| WL6 | 132 | 13 | 145 |
| WL1 | 136 | 2 | 138 |
| SOD | 147 | 18 | 165 |
| SDM | 125 | 4 | 129 |

The parser also preserves intentional gaps (e.g. WL6 jumps from id 134 straight
to `ORDERSCREEN` at 136), so ids are the true on-disk chunk indices.
