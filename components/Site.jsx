import Head from 'next/head';
import { useState } from 'react';
import { tinaField } from 'tinacms/dist/react';
import { SECTIONS, href } from './routes';

const T = {
  es: {
    identity:'Perfil académico',home:'Inicio',intro:'Doctora en Filosofía por la Pontificia Universidad Católica de Chile, con Distinción Máxima.',
    explore:'Explorar trayectoria',download:'Currículum PDF',research:'Investigación y publicaciones',projects:'Proyectos de investigación',
    publications:'Publicaciones',featured:'Publicaciones seleccionadas',highlighted:'Investigación destacada',
    teaching:'Docencia',talks:'Conferencias',education:'Formación',recognitions:'Becas y distinciones',gallery:'Galería',
    media:'Material didáctico y divulgación',profile:'Perfil y contacto',bio:'Resumen biográfico',contacts:'Contacto',languages:'Idiomas',
    articles:'Artículos',chapters:'Capítulos de libro',edited:'Libros coordinados',reviews:'Reseñas',columns:'Columnas de prensa',
    open:'Consultar publicación',pdf:'Ver PDF',doi:'Abrir DOI',video:'Ver video',slide:'Abrir presentación',view:'Ver enlace',
    photo:'Fotografía pendiente',missingBio:'La biografía podrá completarse desde el editor visual.',
    galleryEmpty:'Aquí podrás incorporar imágenes de tus publicaciones que enlacen a sus páginas de lectura o compra.',
    mediaEmpty:'Aquí podrás añadir videos, presentaciones, PDF y otros recursos.',
    profiles:'Perfiles académicos',year:'Año',back:'Volver al inicio',projectsHint:'Tesis, estancias, tutorías, proyectos de investigación y actividades académicas.',
    pubHint:'Artículos, capítulos de libros, libros coordinados, reseñas y columnas.',
    more:'Conocer más', filter:'Buscar entre publicaciones',searchPlaceholder:'Escribe un título, año o revista',noResults:'No se encontraron resultados.',
    all:'Todos los trabajos',teachingRecord:'Docencia y ayudantías',
    viewPublication:'Ver publicación',buy:'Comprar publicación',read:'Leer publicación',
    personalLinks:'Sitios profesionales', institutionLabel:'Institución de formación doctoral',
  },
  en: {
    identity:'Academic profile',home:'Home',intro:'PhD in Philosophy from the Pontificia Universidad Católica de Chile, awarded the highest distinction.',
    explore:'Explore academic record',download:'Download CV',research:'Research and publications',projects:'Research projects',
    publications:'Publications',featured:'Selected publications',highlighted:'Selected research',
    teaching:'Teaching',talks:'Talks and conferences',education:'Education',recognitions:'Grants and distinctions',gallery:'Gallery',
    media:'Teaching and outreach resources',profile:'Profile and contact',bio:'Short biography',contacts:'Contact',languages:'Languages',
    articles:'Journal articles',chapters:'Book chapters',edited:'Edited books',reviews:'Reviews',columns:'Newspaper columns',
    open:'View publication',pdf:'Open PDF',doi:'Open DOI',video:'Watch video',slide:'Open presentation',view:'Open link',
    photo:'Photograph to be added',missingBio:'The biography can be completed through the visual editor.',
    galleryEmpty:'Publication covers and images, linking to reading or purchase pages, will appear here.',
    mediaEmpty:'Videos, slide presentations, PDF files and other resources can be added here.',
    profiles:'Academic profiles',year:'Year',back:'Back to home',projectsHint:'Doctoral thesis, research visits, supervision and academic projects.',
    pubHint:'Journal articles, book chapters, edited books, reviews and newspaper columns.',
    more:'Read more',filter:'Search publications',searchPlaceholder:'Enter a title, year or journal',noResults:'No matching publications found.',
    all:'All publications',teachingRecord:'Teaching and assistance',
    viewPublication:'View publication',buy:'Buy publication',read:'Read publication',
    personalLinks:'Professional links',institutionLabel:'Doctoral university',
  },
};

function safeUrl(value) {
  if (typeof value !== 'string' || !value.trim()) return '';
  const u = value.trim();
  if (u.startsWith('/uploads/')) return u;
  try { const url = new URL(u); if (url.protocol === 'https:' || url.protocol === 'http:') return url.href; }
  catch (_) {}
  return '';
}
function youtubeEmbed(value) {
  const link = safeUrl(value);
  if (!link) return '';
  try {
    const u = new URL(link);
    const host = u.hostname.replace(/^www\./,'');
    let id='';
    if (host==='youtube.com' || host==='m.youtube.com') id = u.searchParams.get('v') || (u.pathname.match(/^\/(?:embed|shorts)\/([\w-]+)/)||[])[1];
    if (host==='youtu.be') id=u.pathname.split('/').filter(Boolean)[0];
    if (id && /^[a-zA-Z0-9_-]{11}$/.test(id)) return `https://www.youtube-nocookie.com/embed/${id}`;
  } catch (_){}
  return '';
}
function f(obj,field){ try{return tinaField(obj,field)}catch(_){return undefined} }
function Paragraph({children}) {return children ? <p className="description">{children}</p> : null}
function LinkPill({value,children}) {const link=safeUrl(value); return link?<a className="small-link" href={link} target="_blank" rel="noopener noreferrer">{children}<span aria-hidden="true"> ↗</span></a>:null}
function takeSorted(items) {
 return [...(items||[])].filter(Boolean).sort((a,b)=>{
  const extract = x => Number((String(x.date||x.year||'').match(/(?:19|20)\d{2}/g)||['0']).slice(-1)[0]);
  return extract(b)-extract(a);
 });
}
function Eye({data}) {const p=data?.profile||{};return <div className="photo-shell">
 {safeUrl(p.photo)? <img data-tina-field={f(p,'photo')} src={safeUrl(p.photo)} alt={p.name||'Fotografía'} /> : <div data-tina-field={f(p,'photo')} className="photo-empty"><span>VRM</span><small>{T.es.photo}</small></div>}
 </div>}
function Heading({eyebrow,title,desc}) {return <div className="page-heading"><div className="eyebrow">{eyebrow}</div><h1>{title}</h1>{desc&&<p>{desc}</p>}</div>}
function PublicItem({p,t}) {return <article className="record" data-tina-field={f(p,'title')}>
 <div className="record-meta"><span>{p.year}</span><span>{p.kind}</span></div>
 <h3>{p.title}</h3><p>{p.citation}</p>
 <div className="links"><LinkPill value={p.url}>{t.open}</LinkPill><LinkPill value={p.pdf_url}>{t.pdf}</LinkPill><LinkPill value={p.doi && (p.doi.startsWith('http')?p.doi:`https://doi.org/${p.doi}`)}>{t.doi}</LinkPill></div>
 {safeUrl(p.embed_url) && <details className="document-view"><summary>{t.pdf}</summary><iframe title={p.title} src={safeUrl(p.embed_url)} loading="lazy" /></details>}
 </article>}
function Projects({data,lang,t,limit}) {const rows=takeSorted(data.research);return <div className="records-grid">{(limit?rows.filter(x=>x.featured).slice(0,2):rows).map((r,i)=><article key={i} className="record" data-tina-field={f(r,'title')}>
 <div className="record-meta"><span>{r.year}</span><span>{r.kind}</span></div><h3>{r.title}</h3><Paragraph>{r[`description_${lang}`] || r.description_es}</Paragraph>
 <div className="links"><LinkPill value={r.url}>{t.view}</LinkPill><LinkPill value={r.pdf_url}>{t.pdf}</LinkPill></div>
 </article>)}</div>}
function Publications({data,t,limit}) {
 const [search,setSearch]=useState(''); const rows=takeSorted(data.publications);
 const list=limit?rows.filter(r=>r.featured):rows.filter(r=>(`${r.title} ${r.citation} ${r.year}`).toLocaleLowerCase().includes(search.toLocaleLowerCase()));
 const groups=[['article',t.articles],['chapter',t.chapters],['book',t.edited],['review',t.reviews],['column',t.columns]];
 return <>
 {!limit&&<div className="search-row"><label htmlFor="publication-search">{t.filter}</label><input id="publication-search" value={search} onChange={e=>setSearch(e.target.value)} placeholder={t.searchPlaceholder}/></div>}
 {limit?<div className="records-grid">{list.slice(0,3).map((r,i)=><PublicItem p={r} t={t} key={i}/>)}</div>:
 groups.map(([k,title])=>{const subset=list.filter(r=>r.kind===k || (k==='book'&&(r.kind==='edited'||r.kind==='edited_book')));return subset.length?<section className="bibliography-group" key={k}><h3>{title} <span>{subset.length}</span></h3><div className="records-grid">{subset.map((r,i)=><PublicItem p={r} t={t} key={i}/>)}</div></section>:null})}
 {!list.length && <p>{t.noResults}</p>}
 </>
}
function Timeline({records,lang,type='default',t}) {return <div className="timeline">{takeSorted(records).map((r,i)=><article className="timeline-item" key={i} data-tina-field={f(r,'title')}>
 <div className="timeline-date">{r.date||r.year}</div>
 <div><h3 data-tina-field={f(r,type==='education'?'title_es':(type==='talks'?'event':'title'))}>{type==='education'?(r[`title_${lang}`]||r.title_es):(type==='talks'?r.event:r.title)}</h3>
 {type==='talks'&&r.title&&<p className="lecture-title">{r.title}</p>}
 {r.institution&&<p className="institution">{r.institution}</p>}
 <Paragraph>{r[`description_${lang}`] || r.description_es}</Paragraph>
 <div className="links"><LinkPill value={r.url}>{t.view}</LinkPill><LinkPill value={r.video_url}>{t.video}</LinkPill><LinkPill value={r.slides_url}>{t.slide}</LinkPill><LinkPill value={r.pdf_url}>{t.pdf}</LinkPill></div>
 </div></article>)}</div>}
function Gallery({data,lang,t}) {const gallery=data.gallery||[];return gallery.length?<div className="gallery-grid">{gallery.map((g,i)=>{
 const dest=safeUrl(g.url);const img=safeUrl(g.image);const inner=<><div className="cover">{img?<img src={img} alt={g.title||'Portada'} loading="lazy"/>:<span>Sin imagen</span>}</div><h3>{g.title}</h3><small>{g.year}</small><Paragraph>{g[`description_${lang}`]||g.description_es}</Paragraph><span className="small-link">{g.kind==='buy'?t.buy:g.kind==='read'?t.read:t.viewPublication} ↗</span></>;
 return dest?<a data-tina-field={f(g,'title')} key={i} className="gallery-item" href={dest} target="_blank" rel="noopener noreferrer">{inner}</a>:<div key={i} className="gallery-item" data-tina-field={f(g,'title')}>{inner}</div>;
 })}</div>:<p className="empty-state">{t.galleryEmpty}</p>}
function Media({data,lang,t}) {const items=data.media||[];return items.length?<div className="media-grid">{items.map((m,i)=>{const video=youtubeEmbed(m.video_url);return <article key={i} className="record media-card" data-tina-field={f(m,'title')}>
 <div className="record-meta"><span>{m.year}</span><span>{m.kind}</span></div><h3>{m.title}</h3><Paragraph>{m[`description_${lang}`]||m.description_es}</Paragraph>
 {video&&<div className="video-shell"><iframe title={m.title} src={video} allowFullScreen loading="lazy" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" /></div>}
 {!video&&safeUrl(m.embed_url)&&<div className="video-shell"><iframe title={m.title} src={safeUrl(m.embed_url)} loading="lazy" /></div>}
 <div className="links"><LinkPill value={m.url}>{t.view}</LinkPill><LinkPill value={m.video_url}>{t.video}</LinkPill><LinkPill value={m.slides_url}>{t.slide}</LinkPill><LinkPill value={m.pdf_url}>{t.pdf}</LinkPill></div>
 </article>})}</div>:<p className="empty-state">{t.mediaEmpty}</p>}
function Profile({data,lang,t}) {const p=data.profile||{};return <>
 <div className="profile-layout"><Eye data={data}/><div><h2>{p.name}</h2><p className="academic-degree" data-tina-field={f(p,lang==='es'?'degree_es':'degree_en')}>{p[`degree_${lang}`]}</p><h3>{t.bio}</h3><Paragraph><span data-tina-field={f(p,`bio_${lang}`)}>{p[`bio_${lang}`]||t.missingBio}</span></Paragraph><h3>{t.contacts}</h3>
 <div className="contact-links">{p.email&&<a data-tina-field={f(p,'email')} href={`mailto:${p.email}`}>{p.email}</a>}{[['website',t.personalLinks],['orcid','ORCID'],['google_scholar','Google Scholar'],['philpapers','PhilPapers']].map(([key,l])=><LinkPill key={key} value={p[key]}>{l}</LinkPill>)}</div>
 {safeUrl(p.cv_pdf)&&<p><LinkPill value={p.cv_pdf}>{t.download}</LinkPill></p>}
 </div></div><section className="long-section"><h2>{t.languages}</h2><div className="language-grid">{(data.languages||[]).map((l,i)=><div className="language-record" data-tina-field={f(l,`name_${lang}`)} key={i}><strong>{l[`name_${lang}`]}</strong><p>{l[`level_${lang}`]}</p></div>)}</div></section>
 </>}
export default function Site({content,lang='es',section='home'}) {
 const [navOpen,setNavOpen]=useState(false);const t=T[lang];const d=content||{};const p=d.profile||{};
 const title=SECTIONS.find(s=>s.key===section)?.[`label_${lang}`]||t.home;const translated=lang==='es'?'en':'es';
 const sw=href(translated,section);
 const baseTitle=p.name||'Valeria Rodríguez Morales';
 return <>
 <Head><title>{section==='home'?baseTitle:`${title} | ${baseTitle}`}</title><meta name="description" content={p[`tagline_${lang}`]||t.intro}/><meta name="viewport" content="width=device-width, initial-scale=1"/></Head>
 <a className="skip-link" href="#contenido">{lang==='es'?'Saltar al contenido':'Skip to content'}</a>
 <header className="site-header"><div className="header-top"><a className="brand" href={href(lang,'home')} aria-label={baseTitle}><span className="brand-square">VRM</span><span><strong>{baseTitle}</strong><small>{p[`degree_${lang}`]||'PhD in Philosophy'}</small></span></a>
 <div className="head-actions"><a className="language-switch" href={sw} aria-label={translated==='en'?'English':'Español'}>{translated.toUpperCase()}</a><button type="button" className="menu-button" onClick={()=>setNavOpen(!navOpen)} aria-expanded={navOpen}>{lang==='es'?'Menú':'Menu'}</button></div></div>
 <nav aria-label={lang==='es'?'Navegación principal':'Main navigation'} className={`main-nav ${navOpen?'open':''}`}><div className="nav-wrap">{SECTIONS.map(s=><a key={s.key} className={section===s.key?'active':''} href={href(lang,s.key)}>{s[`label_${lang}`]}</a>)}</div></nav></header>
 <main id="contenido" className="content-wrap">
 {section==='home' ? <>
 <section className="hero"><div className="hero-text"><div className="eyebrow">{t.identity}</div><h1 data-tina-field={f(p,'name')}>{baseTitle}</h1><p className="hero-degree" data-tina-field={f(p,lang==='es'?'degree_es':'degree_en')}>{p[`degree_${lang}`]}</p><p className="hero-tagline" data-tina-field={f(p,`tagline_${lang}`)}>{p[`tagline_${lang}`]}</p><p data-tina-field={f(p,`intro_note_${lang}`)}>{p[`intro_note_${lang}`]||t.intro}</p><div className="hero-buttons"><a className="button-primary" href={href(lang,'research')}>{t.explore} →</a>{safeUrl(p.cv_pdf)&&<a className="button-secondary" href={safeUrl(p.cv_pdf)} target="_blank" rel="noreferrer">{t.download}</a>}</div><p className="doctoral-institution">{t.institutionLabel}: {p.institution}</p></div><Eye data={d}/></section>
 <section className="home-intro"><div className="eyebrow">{t.identity}</div><h2>{t.identity}</h2><p>{p[`bio_${lang}`]||t.intro}</p><div className="stats"><a href={href(lang,'research')+'#publicaciones'}><strong>{d.publications?.length||0}</strong><span>{t.publications}</span></a><a href={href(lang,'talks')}><strong>{d.talks?.length||0}</strong><span>{t.talks}</span></a><a href={href(lang,'teaching')}><strong>{d.teaching?.length||0}</strong><span>{t.teaching}</span></a></div></section>
 <section className="home-section"><div className="section-heading"><div><div className="eyebrow">{t.research}</div><h2>{t.highlighted}</h2></div><a className="arrow-link" href={href(lang,'research')+'#proyectos'}>{t.more} →</a></div><Projects data={d} lang={lang} t={t} limit/></section>
 <section className="home-section"><div className="section-heading"><div><div className="eyebrow">{t.publications}</div><h2>{t.featured}</h2></div><a className="arrow-link" href={href(lang,'research')+'#publicaciones'}>{t.all} →</a></div><Publications data={d} t={t} limit/></section>
 </>:null}
 {section==='research'&&<><Heading eyebrow={t.identity} title={t.research} desc={t.projectsHint}/><nav className="anchor-nav"><a href="#proyectos">{t.projects} ↓</a><a href="#publicaciones">{t.publications} ↓</a></nav><section id="proyectos" className="long-section"><h2>{t.projects}</h2><Projects data={d} lang={lang} t={t}/></section><section id="publicaciones" className="long-section"><h2>{t.publications}</h2><p>{t.pubHint}</p><Publications data={d} t={t}/></section></>}
 {section==='gallery'&&<><Heading eyebrow={t.identity} title={t.gallery}/><Gallery data={d} lang={lang} t={t}/></>}
 {section==='teaching'&&<><Heading eyebrow={t.identity} title={t.teaching}/><Timeline records={d.teaching} lang={lang} t={t}/></>}
 {section==='talks'&&<><Heading eyebrow={t.identity} title={t.talks}/><Timeline records={d.talks} type="talks" lang={lang} t={t}/></>}
 {section==='education'&&<><Heading eyebrow={t.identity} title={t.education}/><Timeline records={d.education} type="education" lang={lang} t={t}/></>}
 {section==='recognitions'&&<><Heading eyebrow={t.identity} title={t.recognitions}/><Timeline records={d.recognitions} lang={lang} t={t}/></>}
 {section==='media'&&<><Heading eyebrow={t.identity} title={t.media}/><Media data={d} lang={lang} t={t}/></>}
 {section==='profile'&&<><Heading eyebrow={t.identity} title={t.profile}/><Profile data={d} lang={lang} t={t}/></>}
 </main><footer className="footer"><div><span>{baseTitle}</span><span>{p[`degree_${lang}`]}</span></div><a href="#contenido">{t.back} ↑</a></footer>
 </>
}
