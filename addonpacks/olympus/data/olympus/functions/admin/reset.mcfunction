# OP only. Run as the player being reset.
superpower remove olympus:zeus @s
superpower remove olympus:poseidon @s
superpower remove olympus:hades @s
tag @s remove olympus_zeus
tag @s remove olympus_poseidon
tag @s remove olympus_hades
advancement revoke @s from olympus:root
scoreboard players set @s oly_rank 0
scoreboard players set @s oly_lineage 0
scoreboard players set @s oly_claim 0
tellraw @s {"text": "Olympus lineage reset. /trigger oly_guide", "color": "aqua"}
