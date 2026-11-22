#!/usr/bin/env python3
"""Build a bilingual academic website from Pages CMS JSON content.
Dependencies: Python standard library only.
Run: python scripts/build.py
"""
from __future__ import annotations
import json, os, re, shutil
from pathlib import Path
from html import escape
from urllib.parse import urlparse, parse_qs
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src' / 'data'
PUBLIC = ROOT / 'public'
DIST = ROOT / 'dist'
PROFILE = json.loads((DATA/'profile.json').read_text(encoding='utf-8'))
LANGUAGES = json.loads((DATA/'languages.json').read_text(encoding='utf-8'))

def read_records(folder):
    result=[]
    for path in sorted((DATA/folder).glob('*.json')):
        item=json.loads(path.read_text(encoding='utf-8'))
        assert isinstance(item,dict), f'El archivo {path} no es un registro válido'
        result.append(item)
    return sorted(result,key=lambda x:(-int(str(x.get('date', x.get('year','0'))).split('/')[-1][-4:] if str(x.get('date','')).count('/')==2 else max(re.findall(r'(?:19|20)\d{2}',str(x.get('year','0'))) or ['0'])),str(x.get('title',x.get('event','')))))

DB = {name:read_records(name) for name in ('education','publications','research','teaching','talks','recognitions','media','gallery')}
SLUGS={
'es':{'home':'','research':'investigacion','publications':'publicaciones','gallery':'galeria','teaching':'docencia','talks':'conferencias','education':'formacion','recognitions':'distinciones','media':'recursos','profile':'perfil'},
'en':{'home':'','research':'research','publications':'publications','gallery':'gallery','teaching':'teaching','talks':'talks','education':'education','recognitions':'recognition','media':'resources','profile':'profile'}}
SECTIONS=['home','research','publications','gallery','teaching','talks','education','recognitions','media','profile']
TEXT={
'es':{
'home':'Inicio','research':'Investigación','publications':'Publicaciones','gallery':'Galería','teaching':'Docencia','talks':'Conferencias','education':'Formación','recognitions':'Becas y distinciones','media':'Recursos','profile':'Perfil y contacto',
'academic':'Perfil académico','explore':'Explorar trayectoria','cv':'Currículum','year':'Año','featuredR':'Investigación destacada','featuredP':'Publicaciones seleccionadas','all':'Ver todas','more':'Conocer más','records':'Trayectoria completa','complete':'Conocer el perfil completo','back':'Volver arriba','download':'Descargar CV en PDF','addCv':'Podrás incorporar tu CV PDF desde el editor visual.','photo':'Espacio para fotografía','bio':'Resumen biográfico pendiente de incorporar.','contactEmpty':'Puedes completar tu correo y perfiles académicos desde el editor visual.','about':'Resumen biográfico','contact':'Contacto','links':'Perfiles académicos','areas':'Áreas de competencia','languages':'Idiomas','pubTotal':'Publicaciones y colaboraciones','talkTotal':'Participaciones académicas','teachTotal':'Experiencias docentes','opening':'Doctora en Filosofía por la Pontificia Universidad Católica de Chile, con Distinción Máxima.',
'articles':'Artículos en revistas especializadas','chapters':'Capítulos de libro','edited':'Libros coordinados','reviews':'Reseñas','columns':'Columnas en periódicos','lecturer':'Docencia','assistant':'Ayudantías','filter':'Buscar por título, año o referencia…','allKinds':'Todos los tipos','none':'No hay resultados para esa búsqueda.','presentation':'Ponencia','original':'Registro original del CV','open':'Abrir enlace','pdf':'Abrir PDF','doi':'Consultar DOI','viewHere':'Mostrar documento aquí','noteEmbed':'Algunos editores y plataformas no permiten incrustar sus páginas. Si el visor no carga, abre el enlace original.','source':'Abrir documento original','video':'Video de YouTube','slide':'Abrir presentación','mediaEmpty':'Esta sección está preparada para recibir videos, documentos PDF y presentaciones interactivas. Puedes agregarlos desde Pages CMS.','titles':'Los títulos de trabajos, publicaciones y ponencias se conservan en su idioma original.',
'intro_research':'Tesis doctoral, estancias de investigación, supervisión de tesis y proyectos académicos.',
'intro_publications':'Artículos, capítulos, coordinación editorial y colaboración en prensa.',
'intro_gallery':'Portadas e imágenes de publicaciones. Selecciona una imagen para abrir la página donde puedes leer o adquirir la obra.',
'galleryEmpty':'Próximamente encontrarás aquí imágenes de publicaciones y enlaces para leerlas o adquirirlas.',
'galleryOpen':'Ver publicación','galleryRead':'Leer publicación','galleryBuy':'Comprar publicación',
'intro_teaching':'Asignaturas dictadas y ayudantías en universidades.',
'intro_talks':'Conferencias, ponencias, seminarios y actividades académicas.',
'intro_education':'Estudios universitarios, diplomas y doctorado.',
'intro_recognitions':'Becas, distinciones, premios, cargos y sociedades académicas.',
'intro_media':'Material didáctico y divulgativo en formatos audiovisuales, PDF e interactivos.',
'intro_profile':'Información académica, idiomas y vías de contacto.',
'role_tesis':'Tesis doctoral','role_supervision':'Tutoría de tesis','role_estancia':'Estancia de investigación','role_archivo':'Investigación en archivos','role_edicion':'Edición','role_direccion':'Coordinación y gestión','role_beca':'Beca','role_premio':'Premio','role_membresia':'Asociación académica','role_financiamiento':'Financiamiento',
},
'en':{
'home':'Home','research':'Research','publications':'Publications','gallery':'Gallery','teaching':'Teaching','talks':'Conferences','education':'Education','recognitions':'Awards and distinctions','media':'Resources','profile':'Profile and contact',
'academic':'Academic profile','explore':'Explore academic work','cv':'Curriculum vitae','year':'Year','featuredR':'Selected research','featuredP':'Selected publications','all':'See all','more':'Explore more','records':'Full academic record','complete':'Explore my academic profile','back':'Back to top','download':'Download CV (PDF)','addCv':'You can upload your CV PDF through the visual editor.','photo':'Portrait placeholder','bio':'Biographical summary to be added.','contactEmpty':'You can add an email address and academic profiles in the visual editor.','about':'Biography','contact':'Contact','links':'Academic profiles','areas':'Areas of expertise','languages':'Languages','pubTotal':'Publications and contributions','talkTotal':'Academic event appearances','teachTotal':'Teaching appointments','opening':'PhD in Philosophy from Pontificia Universidad Católica de Chile, awarded the highest distinction.',
'articles':'Journal articles','chapters':'Book chapters','edited':'Edited volumes','reviews':'Reviews','columns':'Newspaper columns','lecturer':'Lecturer positions','assistant':'Teaching assistantships','filter':'Search by title, year or reference…','allKinds':'All types','none':'No results match your search.','presentation':'Presentation','original':'Original CV entry','open':'Open link','pdf':'Open PDF','doi':'View DOI','viewHere':'View document here','noteEmbed':'Some publishers and platforms prevent their pages from being embedded. If the viewer does not load, open the original link.','source':'Open original document','video':'YouTube video','slide':'Open presentation','mediaEmpty':'This section is ready for videos, PDF documents and interactive presentations. Add them through Pages CMS.','titles':'The original titles of works, publications and presentations are preserved.',
'intro_research':'Doctoral thesis, academic visits, thesis supervision and research projects.',
'intro_publications':'Journal articles, book chapters, editorial coordination and newspaper writing.',
'intro_gallery':'Covers and images of publications. Select an image to visit the page where you can read or purchase the work.',
'galleryEmpty':'Images of publications and links to read or purchase them will be featured here.',
'galleryOpen':'View publication','galleryRead':'Read publication','galleryBuy':'Buy publication',
'intro_teaching':'University courses taught and teaching assistantships.',
'intro_talks':'Conferences, presentations, seminars and academic events.',
'intro_education':'University degrees, postgraduate qualifications and doctoral education.',
'intro_recognitions':'Scholarships, awards, academic leadership and learned societies.',
'intro_media':'Teaching and outreach materials in video, PDF and interactive formats.',
'intro_profile':'Academic information, working languages and contact details.',
'role_tesis':'Doctoral dissertation','role_supervision':'Thesis supervision','role_estancia':'Research visit','role_archivo':'Archival research','role_edicion':'Editorial work','role_direccion':'Coordination and leadership','role_beca':'Scholarship','role_premio':'Prize','role_membresia':'Academic membership','role_financiamiento':'Research funding',
}}
PUBLABELS={'article':'articles','chapter':'chapters','edited_book':'edited','review':'reviews','column':'columns'}


def e(v):return escape(str(v if v is not None else ''),quote=True)
def langval(obj,stem,lang):return obj.get(f'{stem}_{lang}') or obj.get(f'{stem}_es') or ''
def path(lang,section): return ('/en/' if lang=='en' else '/') + (SLUGS[lang][section]+'/' if SLUGS[lang][section] else '')
def link(text,url,css='',external=False):
    if not url:return ''
    return f'<a href="{e(url)}" class="{e(css)}"'+(' target="_blank" rel="noopener noreferrer"' if external else '')+f'>{e(text)}</a>'
def safe_url(url):
    if not isinstance(url,str) or not url.strip():return ''
    v=url.strip()
    if v.startswith('/uploads/') and '..' not in v:return v
    q=urlparse(v)
    return v if q.scheme in ('http','https') and q.netloc else ''
def youtube_url(url):
    u=safe_url(url)
    if not u or u.startswith('/'):return ''
    q=urlparse(u); host=q.hostname or ''; id=''
    if host=='youtu.be':id=q.path.strip('/').split('/')[0]
    elif host in ('youtube.com','www.youtube.com','m.youtube.com','youtube-nocookie.com','www.youtube-nocookie.com'):
        id=parse_qs(q.query).get('v',[''])[0] or q.path.strip('/').split('/')[-1]
    return f'https://www.youtube-nocookie.com/embed/{id}' if re.fullmatch('[A-Za-z0-9_-]{11}',id or '') else ''
def viewer(lang,video='',pdf='',embed='',slides=''):
    t=TEXT[lang]; chunks=[]
    yt=youtube_url(video); tgt=safe_url(embed) or safe_url(pdf)
    if yt: chunks.append(f'<div class="embed-shell"><div class="embed-head">{t["video"]}</div><div class="embed-ratio"><iframe loading="lazy" src="{e(yt)}" title="{t["video"]}" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div></div>')
    if tgt: chunks.append(f'<div class="embed-shell"><div class="embed-head">{t["pdf"]}</div><div class="embed-pdf"><iframe loading="lazy" src="{e(tgt)}" title="{t["pdf"]}" referrerpolicy="no-referrer" sandbox="allow-same-origin allow-scripts allow-forms allow-popups"></iframe></div><p class="embed-note">{t["noteEmbed"]}</p>{link(t["source"]+" ↗",tgt,"text-link",True)}</div>')
    if safe_url(slides):chunks.append('<p class="more-link">'+link(t['slide']+' ↗',safe_url(slides),'',True)+'</p>')
    return ''.join(chunks)
def nav(lang,page):
    t=TEXT[lang]
    links=''.join(f'<a href="{path(lang,s)}"'+(' class="active" aria-current="page"' if s==page else '')+f'>{e(t[s])}</a>' for s in SECTIONS)
    swap=f'<a href="{path("es",page)}" lang="es" hreflang="es"'+(' aria-current="true"' if lang=='es' else '')+'>ES</a><span aria-hidden="true">/</span><a href="'+path('en',page)+'" lang="en" hreflang="en"'+(' aria-current="true"' if lang=='en' else '')+'>EN</a>'
    return f'''<header class="site-header"><div class="header-top container"><a href="{path(lang,'home')}" class="identity"><span class="identity-icon" aria-hidden="true">VRM</span><span class="identity-text"><strong>{e(PROFILE['name'])}</strong><small>{e(langval(PROFILE,'degree',lang))}</small></span></a><div class="header-actions"><div class="language-switch">{swap}</div><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="{'Abrir menú' if lang=='es' else 'Open menu'}"><span></span><span></span><span></span></button></div></div><nav class="main-nav" id="primary-nav"><div class="container nav-inner">{links}</div></nav></header>'''
def doc(lang,page,body):
    t=TEXT[lang];title=PROFILE['name'] if page=='home' else t[page]+' | '+PROFILE['name']
    desc=langval(PROFILE,'tagline',lang) if page=='home' else t.get('intro_'+page,t[page]);
    site=os.environ.get('SITE_URL','').rstrip('/')
    canonical=f'<link rel="canonical" href="{e(site+path(lang,page))}">' if site else ''
    footer=f'''<footer class="site-footer"><div class="container footer-inner"><div><strong>{e(PROFILE['name'])}</strong><p>{e(t['academic'])}</p></div><div><p>{e(t['titles'])}</p><small>{datetime.now().year} © {e(PROFILE['name'])}</small></div><a class="back-top" href="#main">{e(t['back'])} ↑</a></div></footer>'''
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#002147"><meta name="description" content="{e(desc)}"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="stylesheet" href="/assets/site.css"><link rel="alternate" hreflang="es" href="{path('es',page)}"><link rel="alternate" hreflang="en" href="{path('en',page)}">{canonical}<title>{e(title)}</title></head><body><a class="skip" href="#main">{'Saltar al contenido' if lang=='es' else 'Skip to content'}</a>{nav(lang,page)}<main id="main">{body}</main>{footer}<script src="/assets/site.js" defer></script></body></html>'''

def top(lang,page):
    t=TEXT[lang];desc=t.get('intro_'+page,'')
    return f'''<section class="page-title-section"><div class="container"><div class="crumb"><a href="{path(lang,'home')}">{e(t['home'])}</a><span aria-hidden="true">/</span><span>{e(t[page])}</span></div><p class="kicker light-kicker">{e(t['academic'])}</p><h1>{e(t[page])}</h1><p class="page-subtitle">{e(desc)}</p></div></section>'''

def article_feature(x,lang):
    return f'''<article class="featured-pub"><span class="pub-year">{e(x.get('year'))}</span><div><span class="item-type">{e(TEXT[lang][PUBLABELS.get(x.get('kind'),'articles')])}</span><h3>{e(x.get('title'))}</h3><p>{e(x.get('citation'))}</p></div><a class="circle-arrow" href="{path(lang,'publications')}" aria-label="{TEXT[lang]['publications']}">→</a></article>'''

def home(lang):
    p=PROFILE;t=TEXT[lang];photo=safe_url(p.get('photo'))
    portrait=f'<img src="{e(photo)}" alt="{e(p["name"])}">' if photo else f'<div class="portrait-placeholder"><div class="portrait-monogram">VRM</div><span>{e(t["photo"])}</span></div>'
    intro=langval(p,'bio',lang) or langval(p,'intro_note',lang)
    stats=[('publications','pubTotal'),('talks','talkTotal'),('teaching','teachTotal')]
    stat_html=''.join(f'<a class="stat" href="{path(lang,section)}"><strong>{len(DB[section])}</strong><span>{e(t[label])}</span><i aria-hidden="true">↗</i></a>' for section,label in stats)
    research=''.join(f'''<article class="feature-card"><div class="card-top"><span>{e(x['year'])}</span><span>{e(t.get('role_'+str(x.get('kind')),x.get('kind')))}</span></div><h3>{e(x['title'])}</h3><p>{e(langval(x,'description',lang))}</p>{link(t['more']+' →',path(lang,'research'),'text-link')}</article>''' for x in DB['research'] if x.get('featured'))
    pubs=''.join(article_feature(x,lang) for x in DB['publications'] if x.get('featured'))
    return f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy"><div class="eyebrow"><span class="small-line"></span>{e(t['academic'])}</div><h1>{e(p['name'])}</h1><p class="hero-degree">{e(langval(p,'degree',lang))}</p><p class="hero-fields">{e(langval(p,'tagline',lang))}</p><p class="hero-intro">{e(intro)}</p><div class="hero-actions"><a class="button primary" href="{path(lang,'research')}">{e(t['explore'])} →</a><a class="button secondary" href="{path(lang,'profile')}">{e(t['cv'])} →</a></div><p class="university-line"><span class="mini-rule"></span>{e(p['institution'])}</p></div><div class="portrait-wrap"><div class="portrait-frame">{portrait}</div><div class="portrait-caption">{e(langval(p,'location',lang) or t['academic'])}</div></div></div></section><div class="accent-divider"><div class="container"><span></span></div></div><section class="container section-padding"><div class="section-heading"><div><p class="kicker">{e(t['records'])}</p><h2>{e(t['academic'])}</h2></div><p>{e(t['opening'])}</p></div><div class="stats-grid">{stat_html}</div></section><section class="subtle-band"><div class="container section-padding"><div class="section-heading"><div><p class="kicker">{e(t['research'])}</p><h2>{e(t['featuredR'])}</h2></div>{link(t['all']+' →',path(lang,'research'),'arrow-link')}</div><div class="two-col-cards">{research}</div></div></section><section class="container section-padding"><div class="section-heading"><div><p class="kicker">{e(t['publications'])}</p><h2>{e(t['featuredP'])}</h2></div>{link(t['all']+' →',path(lang,'publications'),'arrow-link')}</div><div class="featured-pubs">{pubs}</div></section><section class="home-cta"><div class="container home-cta-inner"><div><p class="kicker">{e(t['records'])}</p><h2>{e(t['complete'])}</h2></div>{link(t['profile']+' →',path(lang,'profile'),'button light')}</div></section>'''

def pubs_page(lang):
    t=TEXT[lang]
    opts=''.join(f'<option value="{kind}">{e(t[label])}</option>' for kind,label in PUBLABELS.items())
    bar=f'<div class="filter-bar"><div class="filter-label">{e(t["publications"])}</div><div class="filter-controls"><label class="visually-hidden" for="publication-search">{e(t["filter"])}</label><input id="publication-search" class="search-field" type="search" placeholder="{e(t["filter"])}"><label class="visually-hidden" for="publication-kind">{e(t["allKinds"])}</label><select id="publication-kind" class="filter-select"><option value="">{e(t["allKinds"])}</option>{opts}</select></div></div>'
    groups=[]
    for kind,label in PUBLABELS.items():
        items=[r for r in DB['publications'] if r.get('kind')==kind]
        if not items:continue
        rows=[]
        for x in items:
            links=''.join(link(t[k]+' ↗',safe_url(x.get(field)),'',True) for field,k in [('doi','doi'),('url','open'),('pdf_url','pdf')] if safe_url(x.get(field)))
            embed=safe_url(x.get('embed_url')) or safe_url(x.get('pdf_url'))
            if embed:links+=f'<details class="viewer-details"><summary>{e(t["viewHere"])}</summary>{viewer(lang,pdf=x.get("pdf_url"),embed=x.get("embed_url"))}</details>'
            search=e((str(x.get('title'))+' '+str(x.get('year'))+' '+str(x.get('citation'))).lower())
            rows.append(f'<article class="publication-record" data-record data-kind="{kind}" data-search="{search}"><div class="record-year">{e(x.get("year"))}</div><div class="record-main"><h3>{e(x.get("title"))}</h3><p class="citation">{e(x.get("citation"))}</p><div class="record-links">{links}</div></div></article>')
        groups.append(f'<section class="record-section" data-group="{kind}"><div class="group-heading"><h2>{e(t[label])}</h2><span>{len(items)}</span></div><div class="pub-list">{"".join(rows)}</div></section>')
    return bar+f'<div class="stacked-sections">{"".join(groups)}</div><p class="no-results" id="pub-no-results" hidden>{e(t["none"])}</p>'

def gallery_page(lang):
    """Clickable visual gallery, managed independently from the CV bibliography."""
    t=TEXT[lang]
    if not DB['gallery']:
        return f'<div class="empty-state"><div class="empty-emblem" aria-hidden="true">▧</div><h2>{e(t["gallery"])}</h2><p>{e(t["galleryEmpty"])}</p></div>'
    cards=[]
    for x in DB['gallery']:
        title=str(x.get('title') or '')
        image=safe_url(x.get('image'))
        url=safe_url(x.get('url'))
        description=langval(x,'description',lang)
        caption=''.join(f'<span class="gallery-year">{e(x.get("year"))}</span>' if x.get('year') else '')
        caption+=f'<h2>{e(title)}</h2>'
        if description:caption+=f'<p>{e(description)}</p>'
        action=t.get('gallery'+{'read':'Read','buy':'Buy'}.get(x.get('link_kind'),'Open'),t['galleryOpen'])
        visual=f'<img src="{e(image)}" loading="lazy" alt="{e(title)}">' if image else '<span class="gallery-placeholder" aria-hidden="true">▧</span>'
        if url:
            visual=f'<a class="gallery-cover-link" href="{e(url)}" target="_blank" rel="noopener noreferrer" aria-label="{e(action)}: {e(title)}">{visual}<span class="gallery-visit">{e(action)} ↗</span></a>'
        cards.append(f'<article class="gallery-card"><div class="gallery-cover">{visual}</div><div class="gallery-info">{caption}</div></article>')
    return '<div class="gallery-grid">'+''.join(cards)+'</div>'

def timeline(lang,page,items,teaching=False):
    t=TEXT[lang];rows=[]
    for x in items:
        date=x.get('date') if page=='talks' else x.get('year')
        title=x.get('event') if page=='talks' else (langval(x,'title',lang) if page=='education' else x.get('title'))
        kind=x.get('kind',''); ty=t.get('role_'+str(kind),str(kind)) if kind else ''
        if page=='talks':ty=x.get('institution','')
        institution=x.get('institution','') if page in ('education','teaching') else ''
        intro=f'<div class="item-type">{e(ty)}</div>' if ty and page!='teaching' else ''
        sub=f'<p class="institution">{e(institution)}</p>' if institution else ''
        paper=f'<p class="talk-title"><strong>{e(t["presentation"])}:</strong> {e(x["title"])}</p>' if page=='talks' and x.get('title') else ''
        description=langval(x,'description',lang)
        record=e(description)
        exact=f'<details class="original-entry"><summary>{e(t["original"])}</summary><p>{e(x.get("description_es"))}</p></details>' if lang=='en' and x.get('description_es') and x.get('description_es')!=description else ''
        external=''.join(link(t[label]+' ↗',safe_url(x.get(field)),'',True) for field,label in [('url','open'),('pdf_url','pdf')] if safe_url(x.get(field)))
        extra=viewer(lang,video=x.get('video_url'),pdf=x.get('pdf_url') if page=='talks' else '',embed=x.get('embed_url') if page=='research' else '',slides=x.get('slides_url')) if page in ('talks','research') else ''
        rows.append(f'<article class="timeline-item"><div class="timeline-year">{e(date)}</div><div class="timeline-body">{intro}<h2>{e(title)}</h2>{sub}{paper}<p>{record}</p>{exact}<div class="record-links">{external}</div>{extra}</div></article>')
    return '<div class="timeline-list">'+''.join(rows)+'</div>'

def teaching_page(lang):
    t=TEXT[lang];parts=[]
    for kind,label in [('docencia','lecturer'),('ayudantia','assistant')]:
        filtered=[x for x in DB['teaching'] if x.get('kind')==kind]
        parts.append(f'<section class="record-section"><div class="group-heading"><h2>{e(t[label])}</h2><span>{len(filtered)}</span></div>'+timeline(lang,'teaching',filtered)+'</section>')
    return ''.join(parts)

def media_page(lang):
    t=TEXT[lang]
    if not DB['media']:
        return f'<div class="empty-state"><div class="empty-emblem" aria-hidden="true">▤</div><h2>{e(t["media"])}</h2><p>{e(t["mediaEmpty"])}</p></div>'
    cards=[]
    for x in DB['media']:
        linkhtml=link(t['open']+' ↗',safe_url(x.get('url')),'text-link',True)
        cards.append(f'<article class="material-card"><div class="card-top"><span>{e(x.get("kind"))}</span><span>{e(x.get("year"))}</span></div><h2>{e(x.get("title"))}</h2><p>{e(langval(x,"description",lang))}</p>{viewer(lang,video=x.get("video_url"),pdf=x.get("pdf_url"),embed=x.get("embed_url"))}{linkhtml}</article>')
    return '<div class="material-grid">'+''.join(cards)+'</div>'

def profile_page(lang):
    p=PROFILE;t=TEXT[lang]
    photo=safe_url(p.get('photo'))
    portrait=f'<img src="{e(photo)}" alt="{e(p["name"])}">' if photo else '<div class="portrait-placeholder"><span>VRM</span></div>'
    bio=langval(p,'bio',lang)
    email=p.get('email','');email_markup=link(email,'mailto:'+email,'contact-email') if email and '\n' not in email and '@' in email else f'<p class="empty-copy">{e(t["contactEmpty"])}</p>'
    outlets=[(label,safe_url(p.get(field))) for label,field in [('ORCID','orcid'),('Google Scholar','google_scholar'),('PhilPapers','philpapers'),('Web','website')]]
    outlets=[(label,url) for label,url in outlets if url]
    socials=f'<div class="profile-social"><h3>{e(t["links"])}</h3>'+''.join(link(label+' ↗',url,'',True) for label,url in outlets)+'</div>' if outlets else ''
    cv=safe_url(p.get('cv_pdf'))
    cv_html=link(t['download']+' ↗',cv,'button primary',True) if cv else f'<p class="download-hint">{e(t["addCv"])}</p>'
    location=langval(p,'location',lang)
    details=f'''<div class="profile-layout"><div class="profile-panel"><div class="profile-photo-small">{portrait}</div><h2>{e(p['name'])}</h2><p>{e(langval(p,'degree',lang))}</p><p class="institution">{e(p['institution'])}</p></div><div class="profile-copy"><p class="kicker">{e(t['academic'])}</p><h2>{e(t['areas'])}</h2><p>{e(langval(p,'tagline',lang))}</p><h2>{e(t['about'])}</h2><p class="{'empty-copy' if not bio else ''}">{e(bio or t['bio'])}</p>{f'<p>{e(location)}</p>' if location else ''}<div class="contact-block"><h2>{e(t['contact'])}</h2>{email_markup}{socials}</div>{cv_html}</div></div>'''
    langs=''.join(f'<div class="language-row"><strong>{e(langval(x,"name",lang))}</strong><span>{e(langval(x,"level",lang))}</span></div>' for x in LANGUAGES)
    other=''.join(f'<a href="{path(lang,s)}">{e(t[s])} <span aria-hidden="true">→</span></a>' for s in ['education','research','publications','gallery','teaching','talks','recognitions'])
    return details+f'<section class="record-section languages-section"><div class="group-heading"><h2>{e(t["languages"])}</h2></div><div class="language-table">{langs}</div></section><section class="profile-jump"><h2>{e(t["complete"])}</h2><div class="profile-jump-grid">{other}</div></section>'

def page_content(lang,page):
    if page=='home':return home(lang)
    if page=='publications':inside=pubs_page(lang)
    elif page=='gallery':inside=gallery_page(lang)
    elif page=='teaching':inside=teaching_page(lang)
    elif page=='media':inside=media_page(lang)
    elif page=='profile':inside=profile_page(lang)
    else:inside=timeline(lang,page,DB[page])
    return top(lang,page)+f'<div class="container page-content">{inside}</div>'

def write_page(lang,page):
    dest=DIST/path(lang,page).lstrip('/')/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(doc(lang,page,page_content(lang,page)),encoding='utf-8')
    return dest

def main():
    DIST.mkdir(parents=True,exist_ok=True)
    for item in PUBLIC.iterdir():
        target=DIST/item.name
        if item.is_dir():shutil.copytree(item,target,dirs_exist_ok=True)
        else:shutil.copy2(item,target)
    (DIST/'assets').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'src/styles/site.css', DIST/'assets/site.css')
    shutil.copy2(ROOT/'src/styles/site.js', DIST/'assets/site.js')
    written=[]
    for lang in ('es','en'):
        for page in SECTIONS:
            written.append(write_page(lang,page))
    site=os.environ.get('SITE_URL','').rstrip('/')
    if site:
        import xml.sax.saxutils as xml
        items=''.join('<url><loc>'+xml.escape(site+path(l,p))+'</loc></url>' for l in ('es','en') for p in SECTIONS)
        (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="utf-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+items+'</urlset>',encoding='utf-8')
    (DIST/'robots.txt').write_text('User-agent: *\nAllow: /\n'+('Sitemap: '+site+'/sitemap.xml\n' if site else ''),encoding='utf-8')
    print(f"Sitio generado: {len(written)} páginas, {len(DB['publications'])} publicaciones, {len(DB['talks'])} ponencias, {len(DB['teaching'])} experiencias docentes.")
    print('Carpeta: '+str(DIST))

if __name__=='__main__':main()
