scoreboard players add @s oly_rank 0
scoreboard players add @s oly_lineage 0
scoreboard players set @s oly_claim 0
scoreboard players set @s oly_guide 0
tag @s add olympus_initialized
tellraw @s {"text": "Welcome to Olympus. Use /trigger oly_guide for claiming and trial instructions.", "color": "aqua"}
