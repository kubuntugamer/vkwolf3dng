# Wolfenstein 3D — Asset Catalogue

Initial catalogue of the assets defined/referenced by the original Wolfenstein 3D
source release (`WOLFSRC/`). This is a **source-and-definitions** catalogue: the
retail data blobs (VSWAP, VGAHEAD, GAMEMAPS, AUDIOT, …) are **not** in this repo —
they must come from a released copy of the game (see `README.rst` / `RELEASE.TXT`).

Status legend: `[x]` catalogued, `[~]` partially catalogued, `[ ]` todo.

---

## 1. Repository overview

| Path | Role |
| --- | --- |
| `DEICE.EXE`, `INSTALL.BAT`, `WOLFSRC.DAT`, `WOLFSRC.1` | Original DeIce installer + split archive used to produce `WOLFSRC/` |
| `WOLFSRC/` | The original id Software source tree (Borland C++ 3.0/3.1, DOS) |
| `WOLFSRC/README/` | `LICENSE.DOC`, `README.TXT`, `RELEASE.TXT` |
| `WOLFSRC/OBJ/` | Linked-in binary assets: `SIGNON.OBJ`, `GAMEPAL.OBJ` |
| `README.rst` | Repo readme; embeds RELEASE/README/LICENSE text |

Source is 16-bit DOS: 26 `.C`, 44 `.H`, 10 `.ASM`, 9 `.EQU` files.

---

## 2. Game versions / asset sets

Asset enums are selected at compile time via `VERSION.H` + per-platform version
headers (`WOLFVER.H`, `WOLF1VER.H`, `WOLFJVER.H`, `WLFJ1VER.H`, `WOLFGTV.H`,
`SODVER.H`, `SDMVER.H`, `SPANVER.H`), wired in `ID_HEADS.H`. The on-disk data
file *extension* is chosen at runtime in `WL_MENU.C` (`WJ1`, `WJ6`, `WL6`, `WL3`,
`SOD`, `SDM`, `WL1`).

| Code | Product / data set | Notes |
| --- | --- | --- |
| `WL6` | Wolfenstein 3D (full/registered), default build | `GFXV_WL6.H`, `AUDIOWL6.H`, `MAPSWL6.H` |
| `WL1` | Earlier/alternate Wolf3D release | `GFXV_WL1.H`, `GFXE_WL1.H`, `AUDIOWL1.H`, `MAPSWL1.H`, `PICLIST.H` |
| `SOD` | Spear of Destiny (full) | `GFXV_SOD.H`, `AUDIOSOD.H`, `MAPSSOD.H` |
| `SDM` | Spear of Destiny demo | `GFXV_SDM.H`, `AUDIOSDM.H`, `MAPSSDM.H` |
| `WLF` | "Wolf" variant (hardcoded `EXTENSION "WLF"` in `ID_HEAD.H`) | `MAPSWLF.H` |
| `WJ1`/`WJ6` | Japanese releases (referenced, headers not in this tree) | `FOREIGN\JAPAN\GFXV_WJ*.H` |

`BUDIOWL6.H` / `BUDIOSOD.H` are backups of `AUDIOWL6.H` / `AUDIOSOD.H`
(identical except the MUSE creation-date comment).

---

## 3. Asset containers / on-disk formats

Formats are implemented in `ID_CA.C` (graphics/maps/audio cache) and
`ID_PM.C` (paging). Filenames are `<BASE>.<extension>`, extension from §2.

| Container | Files | Content | Encoding |
| --- | --- | --- | --- |
| VSWAP | `VSWAP.<ext>` | Textures, sprites, floor/ceiling, fonts, pics | raw, paged (`ID_PM.C`) |
| VGA graphics | `VGAHEAD.<ext>` + `VGRAPH.<ext>` + `VGADICT.<ext>` | Pics/sprites/tiles/fonts | Huffman + RLEW (`GREXT="VGA"`) |
| EGA graphics | `EGAHEAD.<ext>` + `EGAGRAPH.<ext>` + `EGADICT.<ext>` | Same, EGA variant | Huffman + RLEW |
| CGA graphics | `CGAHEAD.<ext>` + `CGAGRAPH.<ext>` + `CGADICT.<ext>` | Legacy path (refs in `ID_CA.C`) | Huffman + RLEW |
| Maps | `MAPHEAD.<ext>` + `GAMEMAPS.<ext>` (aka `MAPTEMP.<ext>`) | TED5 level planes | RLEW (`RLEWtag`) |
| Audio | `AUDIOHED.<ext>` + `AUDIOT.<ext>` (aka `AUDIO.<ext>`) | PC / AdLib / Digi / music chunks | Huffman |
| Config | `<configname>.<ext>` | Keybinds / setup | textual |
| Savegame | `<SaveName>.<ext>` | Saved game | binary |
| Demos | `<demoname>.<ext>` | `DEMO0..3` | binary |
| Help / end text | `<helpfilename>.<ext>`, `<endfilename>.<ext>` | Story/help screens | textual |

Map header record (`maptype`, `ID_CA.H`): `planestart[3]`, `planelength[3]`,
`width`, `height`, `name[16]`. `NUMMAPS = 60`, `MAPPLANES = 2`.

---

## 4. Graphics assets (VGA)

`graphicnums` enums; each is split into "lumps" (contiguous ID ranges, marked by
`*_LUMP_START/END`) that the cache manager loads/releases as a group.

### 4.1 Per-set totals `[x]`

| Set | Header | Chunks | Fonts | Pics | Tile8 | Tile16 | Tile16M | Externs |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WL6 | `GFXV_WL6.H` | 149 | 2 | 132 | 72 | 0 | 0 | 13 |
| WL1 | `GFXV_WL1.H` | 556 | 2 | 136 | 72 | 144 | 270 | 2 |
| SOD | `GFXV_SOD.H` | 169 | 2 | 147 | 72 | 0 | 0 | 18 |
| SDM | `GFXV_SDM.H` | 133 | 2 | 125 | 72 | 0 | 0 | 4 |

### 4.2 WL6 lump groups `[x]`

| Lump | Range | Count | Contents |
| --- | --- | ---: | --- |
| README | 3–9 | 7 | `H_BJPIC`, castle, Blazkowicz, window frames |
| CONTROLS | 10–42 | 33 | Options, cursors, difficulty, episodes, load/save, joy |
| LEVELEND | 43–85 | 43 | `L_*` score/level-end pics, status bar, title, credits, high scores |
| LATCHPICS | 91–134 | 44 | Weapons, keys, `N_*` numbers, `FACE*` status faces, `PAUSED`, `GETPSYCHED` |
| (other) | 86–90, 135+ | — | `STATUSBARPIC`, intro `T_DEMO0..3`, `T_ENDART1..6`, `ORDERSCREEN`, `ERRORSCREEN` |

### 4.3 WL1 (shareware) lump groups `[x]`

The shareware data files (downloaded from Internet Archive, `wolf3dsw` collection) use the same lump-number ranges as the registered WL1 build, but with reduced content:

| Lump | Range | Count (shareware) | Contents |
| --- | --- | ---: | --- |
| README | 3–9 | 7 | same as WL6 |
| CONTROLS | 10–42 | 33 | same as WL6 |
| LEVELEND | 43–68 | 26 | reduced level-end pics (only episode 1) |
| LATCHPICS | 69–134 | 66 | weapons, keys, numbers (shared with registered) |
| (other) | 86–90, 135+ | — | `STATUSBARPIC`, intro `T_DEMO0` (only one demo) |

### 4.4 Shareware data files `[ ]`

A full copy of the shareware v1.4 data is available as `wolf3dshareware.zip` (654.8 KB, Internet Archive). It contains the nine container files listed in `FORMATS.md` §2, all with extension `WL1`. The counts match the WL1 enum defines (`NUMPICS 136`, `NUMEXTERNS 2`, `NUMSOUNDS 69`, `NUMSNDCHUNKS 234`, `NUMMUSIC 27`, `LASTMAP 30`). See `DATA-REQUIREMENTS.md` for the per-file breakdown.

### 4.5 SOD lump groups `[x]`

BACKDROP 3–8 · CONTROL 9–15 · OPTIONS 16 · SOUND 17–19 · NEWGAME 20–24 ·
LOADSAVE 25–28 · HIGHSCORES 29–30 · ENDGAME 31–35 · LEVELEND 36–78 ·
TITLESCREEN 79–80 · ENDGAME1 81 · ENDGAME2 82 · EASTEREGG 93–94 ·
COPYPROT 95–100 · LATCHPICS 101–149. Includes Spear-unique: `C_WONSPEARPIC`,
`BJCOLLAPSE1..4`, `ENDSCREEN1/12..9`, `IDGUYS1/2`, `COPYPROTTOP/BOX`,
`GODMODEFACE1..3`, `BJWAITING1/2`, `BJOUCHPIC`, plus **palettes**
(`TITLEPALETTE`, `END1..9PALETTE`, `IDGUYSPALETTE`).

### 4.4 SDM lump groups `[x]`

BACKDROP 3–8 · CONTROL 9–15 · OPTIONS 16 · SOUND 17–19 · NEWGAME 20–24 ·
LOADSAVE 25–28 · HIGHSCORES 29–30 · LEVELEND 31–73 · TITLESCREEN 74–75 ·
LATCHPICS 79–127.

### 4.5 WL1 lump groups `[x]`

VGA (`GFXV_WL1.H`): README 3–20 · CONTROLS 21–47 · LEVELEND 48–89 ·
LATCHPICS 95–138. Includes the early publisher/help screens
(`H_KEYBOARDPIC`, `H_HEALPIC`, `H_WOLFLOGOPIC`, `H_FAXPIC`, `H_GALACTIXPIC`,
`H_FGODMOMPIC`, `H_AUSTRALIAPIC`, `H_CANADAPIC`, `H_UKPIC`, …).

### 4.6 Graphics — EGA `[x]`

| Set | Header | Chunks | Fonts | Pics | Tile8 | Tile16 | Tile16M | Externs |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WL1 | `GFXE_WL1.H` | 558 | 2 | 139 | 72 | 144 | 270 | 1 |
| WL6 | `GFXE_WL6.H` | 414 | 0 | 0 | 0 | 144 | 270 | 0 |
| SOD | `GFXE_SOD.H` | 414 | 0 | 0 | 0 | 144 | 270 | 0 |

WL1-EGA lumps: README 3–25 · CONTROLS 26–52 · LEVELEND 53–93 · LATCHPICS 99–141.
(`GFXE_WL6.H`/`GFXE_SOD.H` define tiles only.)

### 4.7 Palette / fonts `[x]`

- Game palette: `gamepal` (768 bytes) linked in from `OBJ/GAMEPAL.OBJ`.
- Fonts: 2 per VGA set (`NUMFONT`) — start at chunk 1/`STARTFONT`.
- SOD adds per-screen palettes as graphics lumps (`*PALETTE`).

---

## 5. Audio assets

MUSE chunk tables. Verified: PC sounds → AdLib sounds → Digi sounds → music.

| Set | Header | Sounds | SndChunks | Music | PC | AdLib | Digi | Music base |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | ---: |
| WL1 | `AUDIOWL1.H` | 69 | 234 | 27 | 0–68 | 69–137 | 138–206 | 207 |
| WL6 | `AUDIOWL6.H` | 87 | 288 | 27 | 0–86 | 87–173 | 174–260 | 261 |
| SOD | `AUDIOSOD.H` | 81 | 267 | 24 | 0–80 | 81–161 | 162–242 | 243 |
| SDM | `AUDIOSDM.H` | 81 | 267 | 24 | 0–80 | 81–161 | 162–242 | 243 |

Backups: `BUDIOWL6.H` ≡ `AUDIOWL6.H`, `BUDIOSOD.H` ≡ `AUDIOSOD.H`.

Sound names are shared across sets (enums fall back to same indices; SOD swaps in
Spear-specific + digitized voices: `GHOSTSIGHT`, `ANGEL*`, `KNIGHT*`, `WILHELM*`,
`UBERDEATH`, `TRANS*`, `GETSPEAR`, …). Music track lists differ per set (see
headers). `[x]` names enumerated; `[ ]` map sound→usage/actor.

---

## 6. Map assets

TED5 map name enums (`MAPS*.H`); actual level data lives in `GAMEMAPS`.

| Set | Header | Named maps | `LASTMAP` | Grouping |
| --- | --- | ---: | ---: | --- |
| WL6 | `MAPSWL6.H` | 60 | 61 | 6 episodes × (8 levels + Boss + Secret); + `MAP4L10PATH_MAP` |
| WL1 | `MAPSWL1.H` | 30 | 30 | 3 episodes × (8 + Boss + Secret) |
| SOD | `MAPSSOD.H` | 21 | 21 | Tunnels, Dungeons, Castle, Ramparts, Death Knight, secrets, Angel of Death |
| SDM | `MAPSSDM.H` | 2 | 2 | Tunnels 1–2 |
| WLF | `MAPSWLF.H` | 4 | 4 | Levels One–Four |

`ID_CA.H` fixes `NUMMAPS = 60` (matches WL6).

---

## 7. Linked-in / compiled assets

| Asset | Source | Notes |
| --- | --- | --- |
| Signon / title screen | `OBJ/SIGNON.OBJ` (`signon`, `introscn`) | 64 KB VGA image; memory reclaimed at runtime (`SignonScreen`, `WL_MAIN.C`) |
| Game palette | `OBJ/GAMEPAL.OBJ` (`gamepal`) | 768-byte VGA palette |
| Ceiling/floor draw buffers | `WHACK_A.ASM` (`planepics`, `MapRow`) | 8 KB (4 KB ceiling + 4 KB floor) |
| Random table | `ID_US_A.ASM` (`rndtable`) | 256-byte table |
| CPU/refresh helpers | `JABHACK.ASM`, `WL_ASM.ASM`, `WL_DR_A.ASM` | `CheckIs386`, `jabhack2`, `AsmRefresh` |
| Low-level drivers | `ID_VL_A.ASM`, `ID_VH_A.ASM`, `ID_SD_A.ASM`, `ID_US_A.ASM` | video/sound/screen assembly |
| Long CPU startup | `C0.ASM` | Borland C runtime startup (not a game asset) |
| Long division | `H_LDIV.ASM` | runtime helper |

---

## 8. Build / tooling artifacts (non-asset)

| File | Type | Notes |
| --- | --- | --- |
| `WOLF.EXE` | DOS NE + Borland DOS extender stub | 50 KB |
| `WOLF3D.EXE` | MS-DOS MZ executable | 495 KB — linked game build |
| `WOLF3D.MAP` | linker map (ASCII) | symbol map |
| `WOLF3D.PRJ`, `WOLF.~DE` | Borland C++ project files | |
| `WOLF.DSW`, `WOLF.IDE`, `WOLF.OBR`, `WOLF3D.DSK` | IDE desktop/browser/context state | reference paths like `C:\SOURCE\WOLF\...` |
| `SV.EXE` | DOS utility | text viewer used by `GO.BAT` |
| `RULES.ASI` | Borland Turbo C++ assembler `RULES.ASI` | runtime rules, not game data |
| `GO.BAT` | build/run helper | |

---

## 9. Coverage & next steps

- `[x]` Version/asset-set matrix, containers, per-set graphics/audio/map counts & lump groups.
- `[x]` Each `graphicnums`/`soundnames`/`musicnames`/`mapnames` enum expanded to
  flat CSV/JSON tables — see [`catalog/`](catalog/README.md).
- `[x]` Code↔asset relational map — see [`catalog/CODE-ASSET-MAP.md`](catalog/CODE-ASSET-MAP.md).
- `[x]` Order-of-operations control flow + flowchart — see [`catalog/FLOWCHART.md`](catalog/FLOWCHART.md).
- `[x]` Byte-level container formats (VSWAP pages; VGAHEAD/VGRAPH/VGADICT;
  AUDIOHED/AUDIOT; MAPHEAD/GAMEMAPS) and the Huffman/Carmack/RLEW codecs —
  see [`catalog/FORMATS.md`](catalog/FORMATS.md).
- `[x]` Sound/music: flat tables done **and** per-sound actor/usage annotation —
  see [`catalog/SOUND-USAGE.md`](catalog/SOUND-USAGE.md) (raw index:
  [`catalog/sound-references.md`](catalog/sound-references.md)).
- `[x]` Retail data requirements per set (episode counts, shareware vs
  registered, compile flags, runtime extension selection) —
  see [`catalog/DATA-REQUIREMENTS.md`](catalog/DATA-REQUIREMENTS.md).

---

## 10. Derived catalogues & analysis

Flat, regeneratable extracts and the code analysis live in [`catalog/`](catalog/):

| File | Contents |
| --- | --- |
| [`catalog/parse_assets.py`](catalog/parse_assets.py) | Enum→table parser (rerun to refresh) |
| [`catalog/graphics.csv`](catalog/graphics.csv) | 717 rows — `set,kind,id,symbol,note` |
| [`catalog/sounds.csv`](catalog/sounds.csv) | 318 rows — `set,id,symbol,note` |
| [`catalog/music.csv`](catalog/music.csv) | 102 rows — `set,id,symbol,note` |
| [`catalog/maps.csv`](catalog/maps.csv) | 118 rows — `set,id,symbol,note` |
| [`catalog/assets.json`](catalog/assets.json) | Same data, keyed by category |
| [`catalog/CODE-ASSET-MAP.md`](catalog/CODE-ASSET-MAP.md) | Code↔asset relational map + diagrams |
| [`catalog/FLOWCHART.md`](catalog/FLOWCHART.md) | Order of operations + flowcharts |
| [`catalog/FORMATS.md`](catalog/FORMATS.md) | Byte-level container/codec reference |
| [`catalog/SOUND-USAGE.md`](catalog/SOUND-USAGE.md) | Sound→actor/trigger map + digitized-voice table |
| [`catalog/sound_usage.py`](catalog/sound_usage.py) | Sound-reference scanner (rerun to refresh) |
| [`catalog/sound-references.md`](catalog/sound-references.md) | Raw sound reference index |
| [`catalog/DATA-REQUIREMENTS.md`](catalog/DATA-REQUIREMENTS.md) | Per-set files, flags, index constants |

**Key finding for §4.1:** the enum symbol count equals `NUMPICS + NUMEXTERNS`.
The trailing block from `STARTEXTERNS` are the IGRAB **externs** (order/error
screens + help/end/demo art); in this build (`ARTSEXTERN`/`DEMOSEXTERN`) they
are `VGRAPH` chunks loaded via `CA_CacheGrChunk` (`ID_CA.C:1318`), and only the
non-`ARTSEXTERN` build stores them as separate files. See `catalog/README.md`
for the per-set table.
