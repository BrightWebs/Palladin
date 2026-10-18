execute as @a[tag=!olympus_initialized] run function olympus:init
scoreboard players enable @a oly_guide
scoreboard players enable @a[scores={oly_lineage=0}] oly_claim
execute as @a[scores={oly_guide=1..}] at @s run function olympus:guide
execute as @a[scores={oly_lineage=0,oly_claim=1}] at @s run function olympus:claim/zeus
execute as @a[scores={oly_lineage=0,oly_claim=2}] at @s run function olympus:claim/poseidon
execute as @a[scores={oly_lineage=0,oly_claim=3}] at @s run function olympus:claim/hades
scoreboard players set @a[scores={oly_claim=1..}] oly_claim 0
