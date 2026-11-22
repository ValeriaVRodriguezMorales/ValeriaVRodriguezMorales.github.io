import { defineConfig } from 'tinacms';

const field = (name: string, label: string, kind: string) => {
  if (kind === 'text') return { type: 'string' as const, name, label, ui: { component: 'textarea' as const } };
  if (kind === 'image') return { type: 'image' as const, name, label };
  if (kind === 'boolean') return { type: 'boolean' as const, name, label };
  if (kind === 'number') return { type: 'number' as const, name, label };
  return { type: 'string' as const, name, label };
};

const group = (name: string, label: string, cols: Array<[string,string,string]>, list=false) => ({
  type: 'object' as const,
  name,
  label,
  ...(list ? { list: true as const } : {}),
  fields: cols.map(([name,label,kind]) => field(name,label,kind)),
  ...(list ? { ui: { itemProps: (item: any) => ({ label: item?.title || item?.event || item?.title_es || item?.name_es || 'Nueva entrada' }) } } : {}),
});

export default defineConfig({
  branch: process.env.NEXT_PUBLIC_TINA_BRANCH || process.env.GITHUB_REF_NAME || 'main',
  clientId: process.env.NEXT_PUBLIC_TINA_CLIENT_ID || null,
  token: process.env.TINA_TOKEN || null,
  build: { outputFolder: 'admin', publicFolder: 'public' },
  media: { tina: { mediaRoot: 'uploads', publicFolder: 'public' } },
  schema: {
    collections: [{
      name: 'site',
      label: 'CV académico completo',
      path: 'content',
      format: 'json',
      match: { include: 'site' },
      ui: { global: true, router: () => '/' },
      fields: [
        group("profile", "01 Perfil, foto y contacto", [
          ["name", "Nombre", "string"],
          ["degree_es", "Grado académico ES", "string"],
          ["degree_en", "Degree EN", "string"],
          ["institution", "Universidad", "string"],
          ["tagline_es", "Especialidades ES", "text"],
          ["tagline_en", "Specialties EN", "text"],
          ["intro_note_es", "Introducción ES", "text"],
          ["intro_note_en", "Introduction EN", "text"],
          ["bio_es", "Biografía ES", "text"],
          ["bio_en", "Biography EN", "text"],
          ["photo", "Fotografía", "image"],
          ["email", "Correo electrónico público", "string"],
          ["website", "Sitio web", "string"],
          ["orcid", "ORCID", "string"],
          ["google_scholar", "Google Scholar", "string"],
          ["philpapers", "PhilPapers", "string"],
          ["cv_pdf", "URL CV PDF", "string"],
          ["location_es", "Ubicación ES", "string"],
          ["location_en", "Location EN", "string"],
        ], false),
        group("research", "02 Investigación y proyectos", [
          ["title", "Título original", "string"],
          ["year", "Año o período", "string"],
          ["kind", "Tipo", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
          ["url", "Enlace", "string"],
          ["pdf_url", "PDF", "string"],
          ["embed_url", "Incrustación", "string"],
          ["featured", "Destacar", "boolean"],
        ], true),
        group("publications", "03 Publicaciones", [
          ["title", "Título original", "string"],
          ["year", "Año", "number"],
          ["kind", "Tipo de publicación", "string"],
          ["citation", "Referencia bibliográfica", "text"],
          ["doi", "DOI", "string"],
          ["url", "Enlace web", "string"],
          ["pdf_url", "PDF en línea", "string"],
          ["embed_url", "URL incrustable", "string"],
          ["featured", "Destacar en portada", "boolean"],
        ], true),
        group("teaching", "04 Docencia", [
          ["title", "Asignatura original", "string"],
          ["year", "Período", "string"],
          ["kind", "Tipo de docencia", "string"],
          ["institution", "Institución", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
        ], true),
        group("talks", "05 Conferencias", [
          ["title", "Título original de ponencia", "string"],
          ["date", "Fecha", "string"],
          ["year", "Año", "number"],
          ["event", "Nombre del evento", "string"],
          ["institution", "Organización", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
          ["video_url", "YouTube", "string"],
          ["slides_url", "Presentación", "string"],
          ["pdf_url", "PDF", "string"],
        ], true),
        group("education", "06 Formación", [
          ["year", "Período", "string"],
          ["title_es", "Formación ES", "string"],
          ["title_en", "Education EN", "string"],
          ["institution", "Institución", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
        ], true),
        group("recognitions", "07 Becas y reconocimientos", [
          ["title", "Nombre", "string"],
          ["year", "Período", "string"],
          ["kind", "Tipo", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
        ], true),
        group("languages", "08 Idiomas", [
          ["name_es", "Idioma ES", "string"],
          ["name_en", "Language EN", "string"],
          ["level_es", "Nivel ES", "string"],
          ["level_en", "Level EN", "string"],
        ], true),
        group("gallery", "09 Galería de portadas", [
          ["title", "Título original", "string"],
          ["year", "Año", "string"],
          ["image", "Imagen de publicación", "image"],
          ["url", "Enlace para leer o comprar", "string"],
          ["kind", "Leer o comprar", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
        ], true),
        group("media", "10 Materiales y videos", [
          ["title", "Título original", "string"],
          ["year", "Año", "string"],
          ["kind", "Tipo", "string"],
          ["description_es", "Descripción ES", "text"],
          ["description_en", "Description EN", "text"],
          ["url", "Enlace", "string"],
          ["video_url", "Video YouTube", "string"],
          ["slides_url", "Presentación", "string"],
          ["pdf_url", "PDF", "string"],
          ["embed_url", "URL incrustable", "string"],
        ], true),
      ],
    }],
  },
});
