import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
const root='src/data';
for (const collection of ['education','publications','teaching','research','talks','recognitions','media']) {
  let files=readdirSync(join(root,collection)).filter(x=>x.endsWith('.json'));
  for (const file of files) {
    const data=JSON.parse(readFileSync(join(root,collection,file),'utf8'));
    if (!data.title && !data.title_es && !data.event) throw new Error(`Sin título: ${collection}/${file}`);
  }
  console.log(`${collection}: ${files.length}`);
}
const profile=JSON.parse(readFileSync(join(root,'profile.json'),'utf8'));
if (!profile.name) throw new Error('Falta nombre');
console.log('Datos correctos.');
