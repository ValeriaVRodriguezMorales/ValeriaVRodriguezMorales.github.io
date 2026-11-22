import json
from pathlib import Path
base = Path(__file__).resolve().parents[1]
s=json.loads((base/'content/site.json').read_text(encoding='utf-8'))
expected={'publications':16,'research':8,'teaching':9,'talks':16,'education':3,'recognitions':7,'languages':3}
for category,num in expected.items():
 assert len(s[category]) == num, f'{category}: esperado {num}, recibido {len(s[category])}'
assert 'Decolonizing environmental politics: sumak kawsay as a possible moral foundation for green policies' in [x['title'] for x in s['publications'] if x['featured']]
assert not any('physiología de los deseos' in x['title'] and x['featured'] for x in s['publications'])
assert not s['profile']['photo'] and not s['profile']['bio_es'] and not s['profile']['bio_en']
print('Contenido íntegro:', ', '.join(f'{k}={v}' for k,v in expected.items()))
