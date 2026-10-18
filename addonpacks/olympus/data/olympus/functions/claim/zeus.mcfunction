scoreboard players set @s oly_ok 0
execute store success score @s oly_ok run superpower add olympus:zeus @s
execute if score @s oly_ok matches 1 run function olympus:claim/zeus_success
