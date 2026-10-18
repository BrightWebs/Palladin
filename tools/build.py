"""Build Olympus from a small, auditable content definition. Python 3.10+."""
import json, pathlib, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
PACK=ROOT/'addonpacks'/'olympus'
def write(path,obj):
 p=PACK/path;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(obj,indent=2)+'\n' if isinstance(obj,(dict,list)) else obj,encoding='utf-8')
def fn(name,lines): write(f'data/olympus/functions/{name}.mcfunction','\n'.join(lines)+'\n')
def tell(message,color='aqua'):return 'tellraw @s '+json.dumps({'text':message,'color':color})
write('pack.mcmeta',{'pack':{'id':'olympus','description':'Olympus | Greek divine lineages | 0.1.0 alpha','pack_format':15,'version':'0.1.0'},'dependencies':{'common':{'minecraft':'[1.20.1,1.20.2)','palladium':'[4.5.9,5.0.0)'}}})
write('data/minecraft/tags/functions/load.json',{'values':['olympus:load']})
write('data/minecraft/tags/functions/tick.json',{'values':['olympus:tick']})
write('data/olympus/tracked_scores.json',{'objectives':['oly_rank']})
fn('load',[f'scoreboard objectives add {n} {kind}' for n,kind in [('oly_claim','trigger'),('oly_guide','trigger'),('oly_rank','dummy'),('oly_lineage','dummy'),('oly_ray','dummy'),('oly_ok','dummy')]])
fn('tick',[
 'execute as @a[tag=!olympus_initialized] run function olympus:init',
 'scoreboard players enable @a oly_guide',
 'scoreboard players enable @a[scores={oly_lineage=0}] oly_claim',
 'execute as @a[scores={oly_guide=1..}] at @s run function olympus:guide',
 *[f'execute as @a[scores={{oly_lineage=0,oly_claim={i}}}] at @s run function olympus:claim/{g}' for i,g in enumerate(['zeus','poseidon','hades'],1)],
 'scoreboard players set @a[scores={oly_claim=1..}] oly_claim 0'])
fn('init',['scoreboard players add @s oly_rank 0','scoreboard players add @s oly_lineage 0','scoreboard players set @s oly_claim 0','scoreboard players set @s oly_guide 0','tag @s add olympus_initialized',tell('Welcome to Olympus. Use /trigger oly_guide for claiming and trial instructions.')])
fn('guide',['scoreboard players set @s oly_guide 0',tell('OLYMPUS • Choose one parent. Your choice persists through death.','gold'),*[tell(f'/trigger oly_claim set {i} • Child of {g.title()}') for i,g in enumerate(['zeus','poseidon','hades'],1)],tell('Open Palladium powers to bind abilities. Complete the Olympus advancement page to grow.'),tell('Ranks: Claimed > Trained > Hero > Champion > Deity. Use /trigger oly_guide to return.')])
write('data/olympus/tags/entity_types/hostiles.json',{'replace':False,'values':['minecraft:zombie','minecraft:husk','minecraft:drowned','minecraft:skeleton','minecraft:stray','minecraft:wither_skeleton','minecraft:spider','minecraft:cave_spider','minecraft:creeper','minecraft:witch','minecraft:slime','minecraft:magma_cube','minecraft:blaze','minecraft:phantom','minecraft:pillager','minecraft:vindicator','minecraft:evoker','minecraft:ravager','minecraft:guardian','minecraft:elder_guardian','minecraft:silverfish','minecraft:endermite','minecraft:hoglin','minecraft:zoglin']})
write('data/olympus/tags/blocks/ray_passable.json',{'values':['minecraft:air','minecraft:cave_air','minecraft:void_air','minecraft:water','minecraft:grass','minecraft:tall_grass','minecraft:fern','minecraft:large_fern','minecraft:seagrass','minecraft:tall_seagrass']})
write('data/olympus/advancements/root.json',{'display':{'icon':{'item':'minecraft:nether_star'},'title':'Olympus','description':'Discover your divine lineage. /trigger oly_guide','background':'minecraft:textures/block/quartz_block_side.png','show_toast':False,'announce_to_chat':False},'criteria':{'claimed':{'trigger':'minecraft:impossible'}}})
GODS={
 'zeus':{'icon':'lightning_rod','color':'#e8d77b','passive':('Skyborn','effect give @s minecraft:slow_falling 2 0 true'),'particle':'electric_spark','attack':'Thunderbolt','move':('Windrunner',['effect give @s minecraft:speed 6 1 true','effect give @s minecraft:jump_boost 6 1 true']),'guard':('Storm Aegis','minecraft:resistance'),'trial_item':'minecraft:lightning_rod','enemy':'minecraft:phantom','trial_biome':'minecraft:windswept_hills'},
 'poseidon':{'icon':'trident','color':'#46d9d0','passive':('Child of the Sea','effect give @s minecraft:water_breathing 2 0 true'),'particle':'bubble_pop','attack':'Water Strike','move':('Ocean Current',['effect give @s minecraft:dolphins_grace 8 0 true']),'guard':('Tidal Guard','minecraft:resistance'),'trial_item':'minecraft:prismarine_shard','enemy':'minecraft:elder_guardian','trial_biome':'minecraft:deep_ocean'},
 'hades':{'icon':'soul_lantern','color':'#ae91e5','passive':('Underworld Sight','effect give @s minecraft:night_vision 12 0 true'),'particle':'soul','attack':'Soul Lance','move':('Shade Step',['effect give @s minecraft:speed 5 1 true','effect give @s minecraft:invisibility 5 0 true']),'guard':('Grave Mantle','minecraft:resistance'),'trial_item':'minecraft:diamond','enemy':'minecraft:wither_skeleton','trial_biome':'minecraft:soul_sand_valley'}}
def rankcond(n):return {'type':'palladium:objective_score','objective':'oly_rank','min_score':n}
for idx,(god,d) in enumerate(GODS.items(),1):
 fn(f'claim/{god}',[
  'scoreboard players set @s oly_ok 0',
  f'execute store success score @s oly_ok run superpower add olympus:{god} @s',
  f'execute if score @s oly_ok matches 1 run function olympus:claim/{god}_success'])
 fn(f'claim/{god}_success',[f'scoreboard players set @s oly_lineage {idx}','scoreboard players set @s oly_rank 1',f'tag @s add olympus_{god}','advancement grant @s only olympus:root',f'energybar value set @s olympus:{god} ichor 100',f'particle minecraft:{d["particle"]} ~ ~1 ~ 0.5 0.8 0.5 0.02 40','playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.6',tell(f'{god.title()} has claimed you. Your divine journey begins.','gold')])
 abilities={}
 def ability(key,title,desc,rank,commands,cost=0,cd=0,x=0,y=0,passive=False):
  a={'type':'palladium:command','title':title,'description':desc,'icon':f'minecraft:{d["icon"]}','gui_position':[x,y],'commands':commands,'conditions':{'unlocking':[rankcond(rank)]}}
  if not passive:
   a['conditions']['enabling']=[{'type':'palladium:energy_bar','energy_bar':'ichor','min':cost},{'type':'palladium:action','cooldown':cd,'key_type':'key_bind'}]
   a['energy_bar_usage']={'energy_bar':'ichor','amount':cost}
  abilities[key]=a
 ability('birthright',*d['passive'][:1],f'Inherited gift of {god.title()}. Free passive.',1,[d['passive'][1]],x=0,y=0,passive=True)
 ability('strike',d['attack'],'Hostile-only aimed strike, 24 blocks. Stops at solid blocks. 10 Ichor; 2s cooldown.',1,[f'function olympus:combat/{god}/cast'],10,40,-60,55)
 ability('movement',d['move'][0],'Movement blessing. 15 Ichor; 12s cooldown.',2,d['move'][1],15,240,60,55)
 ability('guard',d['guard'][0],'Resistance I for 6 seconds. 20 Ichor; 18s cooldown.',3,[f'effect give @s {d["guard"][1]} 6 0 true'],20,360,-60,110)
 ability('ultimate',{'zeus':'Judgment of the Sky','poseidon':'Wrath of the Sea','hades':'Underworld Reckoning'}[god],'Empowered aimed strike: 12 damage. 60 Ichor; 40s cooldown.',4,[f'function olympus:combat/{god}/ultimate'],60,800,60,110)
 ability('manifestation','Divine Manifestation','15 seconds of Strength I, Resistance I and Speed I. 75 Ichor; 90s cooldown.',5,['effect give @s minecraft:strength 15 0 true','effect give @s minecraft:resistance 15 0 true','effect give @s minecraft:speed 15 0 true',f'particle minecraft:{d["particle"]} ~ ~1 ~ 0.7 0.8 0.7 0.04 60'],75,1800,0,170)
 write(f'data/olympus/palladium/powers/{god}.json',{'name':f'Olympus • Child of {god.title()}','icon':f'minecraft:{d["icon"]}','background':'minecraft:textures/block/quartz_block_side.png','gui_display_type':'tree','energy_bars':{'ichor':{'max':100,'auto_increase_per_tick':2,'auto_increase_interval':20,'color':d['color']}},'abilities':abilities})
 for mode,damage in [('cast',6),('ultimate',12)]:
  fn(f'combat/{god}/{mode}',['scoreboard players set @s oly_ray 0',f'execute anchored eyes positioned ^ ^ ^0.5 run function olympus:combat/{god}/ray_{mode}'])
  fn(f'combat/{god}/ray_{mode}',[
   f'particle minecraft:{d["particle"]} ~ ~ ~ 0.03 0.03 0.03 0 1',
   'scoreboard players add @s oly_ray 1',
   f'execute if block ~ ~ ~ #olympus:ray_passable if entity @e[type=#olympus:hostiles,distance=..0.65,limit=1,sort=nearest] run damage @e[type=#olympus:hostiles,distance=..0.65,limit=1,sort=nearest] {damage} minecraft:magic by @s',
   f'execute unless entity @e[type=#olympus:hostiles,distance=..0.65,limit=1] if score @s oly_ray matches ..47 if block ~ ~ ~ #olympus:ray_passable positioned ^ ^ ^0.5 run function olympus:combat/{god}/ray_{mode}'])
 # Four rank trials. All require claiming before earning credit; progression checks run after every trial.
 trials={
 'offering':{'trigger':'minecraft:inventory_changed','conditions':{'player':[{'condition':'minecraft:entity_properties','entity':'this','predicate':{'nbt':f'{{Tags:["olympus_{god}"]}}'}}],'items':[{'items':[d['trial_item']]}]}},
 'journey':{'trigger':'minecraft:location','conditions':{'player':[{'condition':'minecraft:entity_properties','entity':'this','predicate':{'nbt':f'{{Tags:["olympus_{god}"]}}','location':{'biome':d['trial_biome']}}}]}},
 'victory':{'trigger':'minecraft:player_killed_entity','conditions':{'player':[{'condition':'minecraft:entity_properties','entity':'this','predicate':{'nbt':f'{{Tags:["olympus_{god}"]}}'}}],'entity':{'type':d['enemy']}}},
 'ascension':{'trigger':'minecraft:player_killed_entity','conditions':{'player':[{'condition':'minecraft:entity_properties','entity':'this','predicate':{'nbt':f'{{Tags:["olympus_{god}"]}}'}}],'entity':{'type':'minecraft:wither'}}}}
 parent='olympus:root'
 for key,criterion in trials.items():
  aid=f'olympus:{god}/{key}'
  write(f'data/olympus/advancements/{god}/{key}.json',{'parent':parent,'display':{'icon':{'item':f'minecraft:{d["icon"]}'},'title':f'{god.title()}: {key.title()}','description':{'offering':f'Obtain {d["trial_item"]} after claiming.','journey':f'Visit {d["trial_biome"]} after claiming.','victory':f'Defeat {d["enemy"]} after claiming.','ascension':'Defeat a Wither after claiming. Finish all earlier trials to ascend.'}[key],'frame':'challenge' if key=='ascension' else 'task','announce_to_chat':False},'criteria':{'complete':criterion},'rewards':{'function':f'olympus:progress/{god}'}})
  parent=aid
 fn(f'progress/{god}',[
  *[f'execute if score @s oly_lineage matches {idx} if score @s oly_rank matches {rank-1} if entity @s[advancements={{{",".join(f"olympus:{god}/{t}=true" for t in list(trials)[:rank-1])}}}] run function olympus:rank/{god}_{rank}' for rank in range(2,6)]])
 for rank in range(2,6):
  cap={2:125,3:150,4:175,5:250}[rank]
  fn(f'rank/{god}_{rank}',[f'scoreboard players set @s oly_rank {rank}',f'energybar max set @s olympus:{god} ichor {cap}',tell(f'Rank earned: { {2:"Trained Demigod",3:"Hero",4:"Divine Champion",5:"Deity"}[rank]}. New abilities unlocked.','gold')])
fn('admin/reset',['# OP only. Run as the player being reset.',*[f'superpower remove olympus:{g} @s' for g in GODS],*[f'tag @s remove olympus_{g}' for g in GODS],'advancement revoke @s from olympus:root','scoreboard players set @s oly_rank 0','scoreboard players set @s oly_lineage 0','scoreboard players set @s oly_claim 0',tell('Olympus lineage reset. /trigger oly_guide')])
# Explicit archive root: pack.mcmeta is at ZIP root.
(ROOT/'dist').mkdir(exist_ok=True)
with zipfile.ZipFile(ROOT/'dist'/'Olympus-0.1.0.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(PACK.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(PACK))
print('Built',len(list(PACK.rglob('*.json'))),'JSON files and',len(list(PACK.rglob('*.mcfunction'))),'functions')
