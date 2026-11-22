#!/usr/bin/env python3
"""Create standalone, browsable local previews from dist/ without a server.
Run after scripts/build.py. Only preview files are updated.
"""
from pathlib import Path
import sys,re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import SECTIONS, SLUGS, path
out=ROOT/'vista-previa';out.mkdir(exist_ok=True)
css=(ROOT/'dist/assets/site.css').read_text(encoding='utf-8')
js=(ROOT/'dist/assets/site.js').read_text(encoding='utf-8')
urls={}
for lang in ('es','en'):
    for page in SECTIONS:
        slug=SLUGS[lang][page]
        if lang=='es':
            name='inicio.html' if page=='home' else slug+'.html'
        else:
            name='en.html' if page=='home' else 'en-'+slug+'.html'
        urls[path(lang,page)]=name
for uri,name in urls.items():
    src=ROOT/'dist'/uri.lstrip('/')/'index.html'
    html=src.read_text(encoding='utf-8')
    html=html.replace('<link rel="stylesheet" href="/assets/site.css">','<style>'+css+'</style>')
    html=html.replace('<script src="/assets/site.js" defer></script>','<script>'+js+'</script>')
    html=html.replace('<link rel="icon" type="image/svg+xml" href="/favicon.svg">','')
    html=re.sub(r'href="(/[^"]*)"',lambda m:'href="'+urls.get(m.group(1),m.group(1))+'"',html)
    html=html.replace('href="/uploads/','href="../dist/uploads/').replace('src="/uploads/','src="../dist/uploads/')
    (out/name).write_text(html,encoding='utf-8')
(out/'INSTRUCCIONES.txt').write_text('Abre inicio.html con doble clic para visualizar la web localmente. Esta vista previa es un archivo de consulta: no la subas a GitHub. Para generar una nueva después de editar, ejecuta python3 scripts/build.py y python3 scripts/build_preview.py.\n',encoding='utf-8')
print(f'Vista previa generada: {len(urls)} páginas')
