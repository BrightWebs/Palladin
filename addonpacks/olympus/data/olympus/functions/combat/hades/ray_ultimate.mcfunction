particle minecraft:soul ~ ~ ~ 0.03 0.03 0.03 0 1
scoreboard players add @s oly_ray 1
execute if block ~ ~ ~ #olympus:ray_passable if entity @e[type=#olympus:hostiles,distance=..0.65,limit=1,sort=nearest] run damage @e[type=#olympus:hostiles,distance=..0.65,limit=1,sort=nearest] 12 minecraft:magic by @s
execute unless entity @e[type=#olympus:hostiles,distance=..0.65,limit=1] if score @s oly_ray matches ..47 if block ~ ~ ~ #olympus:ray_passable positioned ^ ^ ^0.5 run function olympus:combat/hades/ray_ultimate
