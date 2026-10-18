scoreboard players set @s oly_lineage 1
scoreboard players set @s oly_rank 1
tag @s add olympus_zeus
advancement grant @s only olympus:root
energybar value set @s olympus:zeus ichor 100
particle minecraft:electric_spark ~ ~1 ~ 0.5 0.8 0.5 0.02 40
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6
tellraw @s {"text": "Zeus has claimed you. Your divine journey begins.", "color": "gold"}
