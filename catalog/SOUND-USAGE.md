# Sound usage & actor map

WHERE each sound asset is used, by subsystem and trigger. Sound enums live in
`WOLFSRC/AUDIO*.H`; the raw per-symbol reference index (every `file:line` +
enclosing function) is auto-generated in
[`sound-references.md`](sound-references.md). Container/format details are in
[`FORMATS.md`](FORMATS.md) §3.

## 0. How a sound gets played

| Helper | Defined | Semantics |
| --- | --- | --- |
| `SD_PlaySound(s)` | `ID_SD.C` | 2D/global playback; returns true if a channel was claimed. Used by menus, pickups, UI. |
| `PlaySoundLocGlobal(s,gx,gy)` | `WL_GAME.C:170` | computes stereo channel from position, calls `SD_PositionSound` then `SD_PlaySound`; remembers `globalsoundx/y` for `UpdateSoundLoc`. |
| `PlaySoundLocActor(s,ob)` | macro `WL_DEF.H:851` | `PlaySoundLocGlobal(s, ob->x, ob->y)`. |
| `PlaySoundLocTile(s,tx,ty)` | macro `WL_DEF.H:850` | positional by tile. |

Actor ambient sounds additionally gate on `areabyplayer[ob->areanumber]`
(e.g. `A_MechaSound`, `WL_ACT2.C:2912`). The two big actor dispatch tables are
`FirstSighting` (`WL_STATE.C:1253`) and `A_DeathScream` (`WL_ACT2.C:1061`).

---

## 1. Enemy **sight** sounds — `FirstSighting` (`WL_STATE.C:1253`)

| `obclass` | Sound | Line |
| --- | --- | --- |
| `guardobj` | `HALTSND` | 1261 |
| `officerobj` | `SPIONSND` | 1267 |
| `ssobj` | `SCHUTZADSND` | 1278 |
| `dogobj` | `DOGBARKSND` | 1284 |
| `bossobj` | `GUTENTAGSND` | 1291 |
| `gretelobj` | `KEINSND` | 1297 |
| `giftobj` | `EINESND` | 1303 |
| `fatobj` | `ERLAUBENSND` | 1309 |
| `schabbobj` | `SCHABBSHASND` | 1315 |
| `fakeobj` | `TOT_HUNDSND` | 1321 |
| `mechahitlerobj` | `DIESND` | 1327 |
| `realhitlerobj` | `DIESND` | 1333 |
| `spectreobj` (`SPEAR`) | `GHOSTSIGHTSND` | 1345 |
| `angelobj` (`SPEAR`) | `ANGELSIGHTSND` | 1351 |
| `transobj` (`SPEAR`) | `TRANSSIGHTSND` | 1357 |
| `willobj` (`SPEAR`) | `WILHELMSIGHTSND` | 1368 |
| `deathobj` (`SPEAR`) | `KNIGHTSIGHTSND` | 1374 |
| `mutantobj`, `ghostobj`, `uberobj` | _(silent)_ | — |

## 2. Enemy **death** sounds — `A_DeathScream` (`WL_ACT2.C:1061`)

| `obclass` | Sound | Line |
| --- | --- | --- |
| `mutantobj` | `AHHHGSND` | 1086 |
| `guardobj` | random of `DEATHSCREAM1..5,7,8,9` (`sounds[US_RndT()%8]`) | 1091–1102 |
| `officerobj` | `NEINSOVASSND` | 1109 |
| `ssobj` | `LEBENSND` | 1112 |
| `dogobj` | `DOGDEATHSND` | 1115 |
| `bossobj` | `MUTTISND` | 1119 |
| `schabbobj` | `MEINGOTTSND` | 1122 |
| `fakeobj` | `HITLERHASND` | 1125 |
| `mechahitlerobj` | `SCHEISTSND` | 1128 |
| `realhitlerobj` | `EVASND` | 1131 |
| `gretelobj` | `MEINSND` | 1134 |
| `giftobj` | `DONNERSND` | 1137 |
| `fatobj` | `ROSESND` | 1140 |
| `spectreobj` (`SPEAR`) | `GHOSTFADESND` | 1144 |
| `angelobj` (`SPEAR`) | `ANGELDEATHSND` | 1147 |
| `transobj` (`SPEAR`) | `TRANSDEATHSND` | 1150 |
| `uberobj` (`SPEAR`) | `UBERDEATHSND` | 1153 |
| `willobj` (`SPEAR`) | `WILHELMDEATHSND` | 1156 |
| `deathobj` (`SPEAR`) | `KNIGHTDEATHSND` | 1159 |

> **Secret-map easter egg:** on the WL6 secret map (`mapon == 9`, or maps 18/19
> in Spear) there is a 1/256 chance that mutant/guard/officer/ss/dog use
> `DEATHSCREAM6SND` (the "fart") instead — `WL_ACT2.C:1065-1078`.

## 3. Weapon / projectile / attack sounds

| Sound | Trigger | Line |
| --- | --- | --- |
| `ATKKNIFESND` | `KnifeAttack` | `WL_AGENT.C:1138` |
| `ATKPISTOLSND` | `GunAttack` (pistol) | `WL_AGENT.C:1178` |
| `ATKMACHINEGUNSND` | `GunAttack` (machine gun) | `WL_AGENT.C:1181` |
| `ATKGATLINGSND` | `GunAttack` (chaingun) | `WL_AGENT.C:1184` |
| `MISSILEFIRESND` | `T_Launch`, `T_GiftThrow`, boss `T_Shoot` | `WL_ACT2.C:1675,2367,3501` |
| `MISSILEHITSND` | `T_Projectile` impact | `WL_ACT2.C:328,334` |
| `BOSSFIRESND` | boss `T_Shoot` | `WL_ACT2.C:3506` |
| `SSFIRESND` | ss `T_Shoot` | `WL_ACT2.C:3496` |
| `NAZIFIRESND` | nazi `T_Shoot` | `WL_ACT2.C:3516` |
| `SCHABBSTHROWSND` | `T_SchabbThrow`, schabb `T_Shoot` | `WL_ACT2.C:2328,3509` |
| `DOGATTACKSND` | dog `T_Bite` | `WL_ACT2.C:3536` |
| `KNIGHTMISSILESND` (`SPEAR`) | death-knight `T_Launch` | `WL_ACT2.C:1667` |
| `ANGELFIRESND` (`SPEAR`) | angel `T_Launch` | `WL_ACT2.C:1672` |
| `FLAMETHROWERSND` (`SPEAR`) | `T_FakeFire`, fake-hitler `T_Shoot` | `WL_ACT2.C:2961,3512` |
| `SLURPIESND` | `A_Slurpie` (projectile gibs) | `WL_ACT2.C:1777,2922` |
| `MECHSTEPSND` | `A_MechaSound` (gated by `areabyplayer`) | `WL_ACT2.C:2915` |
| `ANGELTIREDSND` (`SPEAR`) | `A_Breathing` | `WL_ACT2.C:1783` |
| `YEAHSND` | `T_BJYell` (boss death yell from BJ) | `WL_ACT2.C:3700` |

## 4. Player pickups — `GetBonus` (`WL_AGENT.C:667`), `GiveExtraMan` (`:492`)

| Item (`itemnumber`) | Sound | Line |
| --- | --- | --- |
| `bo_firstaid` | `HEALTH2SND` | 675 |
| `bo_key1..4` | `GETKEYSND` | 684 |
| `bo_cross` | `BONUS1SND` | 688 |
| `bo_chalice` | `BONUS2SND` | 693 |
| `bo_bible` | `BONUS3SND` | 698 |
| `bo_crown` | `BONUS4SND` | 703 |
| `bo_clip`, `bo_clip2` | `GETAMMOSND` | 712,719 |
| `bo_25clip` (`SPEAR`) | `GETAMMOBOXSND` | 728 |
| `bo_machinegun` | `GETMACHINESND` | 734 |
| `bo_chaingun` | `GETGATLINGSND` | 738 |
| `bo_fullheal` | `BONUS1UPSND` | 747 |
| `bo_food`, `bo_alpo` | `HEALTH1SND` | 758,766 |
| `bo_gibs` (low health) | `SLURPIESND` | 774 |
| `bo_spear` (`SPEAR` exit) | _(silent — ends level)_ | 778 |
| extra life (`GiveExtraMan`) | `BONUS1UPSND` | 497 |

## 5. Doors, walls, pushwalls, use

| Sound | Trigger | Line |
| --- | --- | --- |
| `OPENDOORSND` | `DoorOpening` | `WL_ACT1.C:586` |
| `CLOSEDOORSND` | `CloseDoor` | `WL_ACT1.C:475` |
| `PUSHWALLSND` | `PushWall` | `WL_ACT1.C:796` |
| `NOWAYSND` | `OperateDoor` (locked), `PushWall` (blocked) | `WL_ACT1.C:507,749,759,769,779` |
| `HITWALLSND` | `ClipMove` (player bumps wall) | `WL_AGENT.C:884` |
| `LEVELDONESND` | `Cmd_Use` on the elevator switch | `WL_AGENT.C:1069` |
| `DONOTHINGSND` | `Cmd_Use` on a no-op object | `WL_AGENT.C:1078` |

## 6. Intermission / menu / UI

| Sound | Trigger | Line |
| --- | --- | --- |
| `ENDBONUS1SND`, `ENDBONUS2SND`, `PERCENT100SND`, `NOBONUSSND`, `BONUS1UPSND` | `LevelCompleted` (per-stat roll-up) | `WL_INTER.C:672-926` |
| `ESCPRESSEDSND` | menu "back/escape" | `WL_MENU.C:1637,1948,2359,2790,3341,3594,3670` |
| `MOVEGUN1SND`, `MOVEGUN2SND` | menu cursor move / `DrawHalfStep` / `DrawGun` | `WL_MENU.C:1907,1923,2336,2349,3371,3397` |
| `SHOOTSND` | menu accept; joystick calibrate; mouse sensitivity | `WL_MENU.C:1706,1740,1951,2800,3594,3670,3873` |
| `HITWALLSND`, `NOWAYSND` | menu "blocked" feedback | `WL_MENU.C:951,2215,2761,2772` |
| `SHOOTDOORSND` | control-config "shoot" binding | `WL_MENU.C:2251,2278` |
| `NOBONUSSND`/`ENDBONUS2SND` | Spear god-mode cheat toggle | `WL_PLAY.C:639,644` |
| `PLAYERDEATHSND` | `Died` | `WL_GAME.C:1121` |
| `GETSPEARSND` | `GameLoop` (Spear grab) | `WL_GAME.C:1291` |

## 7. Digitized-voice map — `wolfdigimap[]` (`WL_MAIN.C:849`)

The AdLib/SB builds can replace certain sounds with sampled speech. Table maps
`soundnames → digi index` (used by `SD_PlayDigitized(DigiMap[...])`). WL6
(`#ifndef UPLOAD`) entries:

`HALTSND`0, `DOGBARKSND`1, `CLOSEDOORSND`2, `OPENDOORSND`3,
`ATKMACHINEGUNSND`4, `ATKPISTOLSND`5, `ATKGATLINGSND`6, `SCHUTZADSND`7,
`GUTENTAGSND`8, `MUTTISND`9, `BOSSFIRESND`10, `SSFIRESND`11,
`DEATHSCREAM1`12, `DEATHSCREAM2`13, `DEATHSCREAM3`13, `TAKEDAMAGESND`14,
`PUSHWALLSND`15, `DOGDEATHSND`16, `AHHHGSND`17, `DIESND`18, `EVASND`19,
`LEBENSND`20, `NAZIFIRESND`21, `SLURPIESND`22, `TOT_HUNDSND`23,
`MEINGOTTSND`24, `SCHABBSHASND`25, `HITLERHASND`26, `SPIONSND`27,
`NEINSOVASSND`28, `DOGATTACKSND`29, `LEVELDONESND`30, `MECHSTEPSND`31,
`YEAHSND`32, `SCHEISTSND`33, `DEATHSCREAM4`34, `DEATHSCREAM5`35,
`DONNERSND`36, `EINESND`37, `ERLAUBENSND`38, `DEATHSCREAM6`39,
`DEATHSCREAM7`40, `DEATHSCREAM8`41, `DEATHSCREAM9`42, `KEINSND`43,
`MEINSND`44, `ROSESND`45.

The Spear variant (`WL_MAIN.C:913+`) uses a different index list
(`HALTSND`0, `CLOSEDOORSND`2, `OPENDOORSND`3, `ATKMACHINEGUNSND`4, …,
`ANGELSIGHTSND`, `TRANSSIGHTSND`, `WILHELMSIGHTSND`, `KNIGHTSIGHTSND`).

## 8. Sounds defined but never referenced

These are present in the `soundnames` enum(s) but no `.C` file uses them
(legacy carry-overs from earlier Id titles / trimmed features):

`SELECTWPNSND`, `SELECTITEMSND`, `HEARTBEATSND`, `NAZIHITPLAYERSND`,
`NOITEMSND`, `WALK1SND`, `WALK2SND`, `GAMEOVERSND`, `HITENEMYSND`,
`BOSSACTIVESND`, and `GOOBSSND` (WL6 header only).

## 9. Regenerating the raw index

```
python3 catalog/sound_usage.py          # writes catalog/sound-references.md
python3 catalog/sound_usage.py -        # or print to stdout
```
