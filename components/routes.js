export const SECTIONS = [
  { key: 'home', es: '', en: 'en', label_es: 'Inicio', label_en: 'Home' },
  { key: 'research', es: 'investigacion', en: 'en/research', label_es: 'Investigación y publicaciones', label_en: 'Research and publications' },
  { key: 'gallery', es: 'galeria', en: 'en/gallery', label_es: 'Galería', label_en: 'Gallery' },
  { key: 'teaching', es: 'docencia', en: 'en/teaching', label_es: 'Docencia', label_en: 'Teaching' },
  { key: 'talks', es: 'conferencias', en: 'en/talks', label_es: 'Conferencias', label_en: 'Talks' },
  { key: 'education', es: 'formacion', en: 'en/education', label_es: 'Formación', label_en: 'Education' },
  { key: 'recognitions', es: 'distinciones', en: 'en/recognition', label_es: 'Becas y distinciones', label_en: 'Awards and grants' },
  { key: 'media', es: 'recursos', en: 'en/resources', label_es: 'Recursos', label_en: 'Resources' },
  { key: 'profile', es: 'perfil', en: 'en/profile', label_es: 'Perfil y contacto', label_en: 'Profile and contact' },
];
export const ALL_ROUTES = [
  ...SECTIONS.flatMap((s) => [
    { route: s.es, lang: 'es', section: s.key },
    { route: s.en, lang: 'en', section: s.key },
  ]),
  // Acceso de compatibilidad a las antiguas páginas de publicaciones.
  { route: 'publicaciones', lang: 'es', section: 'research' },
  { route: 'en/publications', lang: 'en', section: 'research' },
];
export const href = (lang, section) => `/${SECTIONS.find((s) => s.key === section)?.[lang] || ''}${section === 'home' && lang === 'es' ? '' : '/'} ` .trimEnd();
