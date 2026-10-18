scoreboard players set @s oly_lineage 2
scoreboard players set @s oly_rank 1
tag @s add olympus_poseidon
advancement grant @s only olympus:root
energybar value set @s olympus:poseidon ichor 100
particle minecraft:bubble_pop ~ ~1 ~ 0.5 0.8 0.5 0.02 40
playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6
tellraw @s {"text": "Poseidon has claimed you. Your divine journey begins.", "color": "gold"}
