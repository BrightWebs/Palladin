scoreboard players set @s oly_lineage 3
scoreboard players set @s oly_rank 1
tag @s add olympus_hades
advancement grant @s only olympus:root
energybar value set @s olympus:hades ichor 100
particle minecraft:soul ~ ~1 ~ 0.5 0.8 0.5 0.02 40
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6
tellraw @s {"text": "Hades has claimed you. Your divine journey begins.", "color": "gold"}
