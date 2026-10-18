"""Static integration checks; does not claim Minecraft runtime validation."""
import json,pathlib,re,zipfile
root=pathlib.Path(__file__).resolve().parents[1];pack=root/'addonpacks/olympus'
files=list(pack.rglob('*'));parsed={str(p.relative_to(pack)):json.loads(p.read_text()) for p in files if p.suffix=='.json' or p.name=='pack.mcmeta'}
functions={str(p.relative_to(pack/'data/olympus/functions')).removesuffix('.mcfunction') for p in files if p.suffix=='.mcfunction'}
for p in files:
 if p.suffix=='.mcfunction':
  for target in re.findall(r'\bfunction olympus:([\w/]+)',p.read_text()):assert target in functions,(p,target)
for god in ('zeus','poseidon','hades'):
 power=parsed[f'data/olympus/palladium/powers/{god}.json']
 assert len(power['abilities'])==6
 for key,a in power['abilities'].items():
  assert a['conditions']['unlocking'][0]['objective']=='oly_rank'
  if key!='birthright':
   gates=a['conditions']['enabling'];cost=a['energy_bar_usage']['amount']
   assert gates[0]['min']==cost and gates[1]['type']=='palladium:action' and gates[1]['cooldown']>0
 assert 'store success' in (pack/f'data/olympus/functions/claim/{god}.mcfunction').read_text()
 for trial in ('offering','journey','victory','ascension'):
  a=parsed[f'data/olympus/advancements/{god}/{trial}.json']
  assert f'olympus_{god}' in json.dumps(a['criteria'])
  assert a['rewards']['function'].removeprefix('olympus:') in functions
 for mode in ('cast','ultimate'):
  ray=(pack/f'data/olympus/functions/combat/{god}/ray_{mode}.mcfunction').read_text()
  assert 'matches ..47' in ray and '#olympus:ray_passable' in ray
  assert 'type=#olympus:hostiles' in ray and 'minecraft:magic by @s' in ray
  assert 'summon minecraft:lightning_bolt' not in ray
with zipfile.ZipFile(root/'dist/Olympus-0.1.0.zip') as z:
 assert 'pack.mcmeta' in z.namelist()
 assert len(z.namelist())==len([p for p in files if p.is_file()])
print(f'PASS: {len(parsed)} JSON documents, {len(functions)} functions; references, claiming guards, energy, cooldowns, trial filters, bounded raycast and ZIP layout')
