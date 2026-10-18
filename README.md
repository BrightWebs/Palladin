# Olympus

Greek mythology addon for **Palladium 4.5.9, Minecraft Java 1.20.1**.

## Status

0.1.0 alpha: implemented source, statically validated; **not yet launched in Minecraft**. This is a first playable candidate, not the full planned mod. No Roman paths.

## Included

- Zeus, Poseidon and Hades power trees, each with a passive and five active techniques.
- Permanent one-parent claiming, server-validated through non-OP trigger commands.
- Ichor, individual cooldowns and five progression ranks through Deity.
- Four post-claim trials per lineage, an advancement page and increasing Ichor capacity.
- Hostile-only aimed magic strikes, 24-block range, with terrain obstruction and caster damage attribution. Players, pets, villagers and blocks are not attack targets.
- An administrator reset limited to Olympus powers and progression.

## Install

1. Install Minecraft Java **1.20.1** with Palladium **4.5.9** and that release's required dependencies. This pack is not for Minecraft 1.21.1 or the newer preview API.
2. Download this repository. With Python 3.10+, run `python tools/build.py` from the repository folder. It creates `dist/Olympus-0.1.0.zip`.
3. Put the ZIP in your instance's `.minecraft/addonpacks/` directory. Do not put it in `mods`. Alternatively copy `addonpacks/olympus/` into that directory. Install exactly one copy.
4. Restart Minecraft. On dedicated servers, install the addon on both server and clients.
5. Enter a test world. Use `/trigger oly_guide`. Claim using `/trigger oly_claim set 1` for Zeus, `2` for Poseidon, or `3` for Hades.
6. Open Palladium's powers interface and configure its ability keys. No fixed Z/X/C/V bindings are imposed.

Commands become available after the first world tick. Claiming needs no operator permissions. If a power cannot be granted, claiming does not record a successful lineage.

## Trials

All trial credit requires your lineage tag and an event after claiming. Inventory trials require a subsequent inventory change if you already hold the item.

| Parent | Trained | Hero | Champion | Deity |
| --- | --- | --- | --- | --- |
| Zeus | Obtain a lightning rod | Visit windswept hills | Kill a phantom | Kill a Wither |
| Poseidon | Obtain a prismarine shard | Visit deep ocean | Kill an Elder Guardian | Kill a Wither |
| Hades | Obtain a diamond | Visit soul sand valley | Kill a Wither Skeleton | Kill a Wither |

Later trials can be completed early, but ranks advance only when every preceding trial is complete. Items are checked, not consumed: the first trial is an acquisition milestone, not an offering ritual.

Ichor capacity: 100 / 125 / 150 / 175 / 250. Regeneration: 2 per second. Regular strikes: 10 Ichor / 2s; movement: 15 / 12s; guard: 20 / 18s; ultimate: 60 / 40s; manifestation: 75 / 90s. Manifestation grants 15 seconds of Strength I, Resistance I and Speed I. No terrain destruction, fire spawning or permanent water placement.

## Administration

As an operator: `/execute as PLAYER at @s run function olympus:admin/reset`.
This intentionally revokes Olympus trial records and removes Olympus lineages. It preserves other packs' powers. Temporary potion effects expire naturally, at most 15 seconds after reset; they are not globally cleared because other mods may own the same effects.

## Build and verify

`python tools/build.py`

`python tools/validate.py`

GitHub Actions runs both and uploads the installable ZIP as an Actions artifact. Validation checks JSON, references, rank gating, energy/cooldown guards, ray bounds and archive layout. It does not replace an actual Minecraft integration test.

## Still planned

Specializations, claiming sigil items and ceremonies, custom textures/models, relics, equipment blessings, remaining parents, camps, original mythological monsters, unique ascension quests and truly distinct divine forms. Current ultimates are stronger aimed strikes; current manifestation is a temporary buff. Zeus Windrunner is speed/jump, not flight; Hades Shade Step is speed/invisibility, not teleportation.

## Runtime acceptance checklist

In a disposable world: inspect latest.log for pack errors; claim every parent on fresh players; check duplicate claiming; unlock ranks in and out of order; test walls, range, hostile hits and pet/player immunity; exhaust Ichor; verify cooldowns; die and reconnect at each rank; test server/client synchronization with two players; reset and reclaim. Do not call the alpha verified until those checks pass.

## Compatibility evidence

Schemas and commands checked against ThreeTAG Palladium 4.5.9 source commit `512d330efc41b733c4ed9607ceb00ecf091d23be`: ActionCondition, ObjectiveScoreCondition, CommandAbility, EnergyBarCondition, TrackedScoresManager, SuperpowerCommand and EnergyBarCommand, plus the project's energy/cooldown example packs.

Official docs: https://docs.threetag.net/
Source: https://git.threetag.net/ThreeTAG/Palladium
