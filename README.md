# Migración del CV académico a TinaCMS con edición visual

**ESTADO: PROYECTO DE MIGRACIÓN, NO PUBLICAR AÚN SOBRE TU WEB PRINCIPAL.**

Esta carpeta contiene un **nuevo sitio Next.js**, no una actualización de `scripts/build.py`. Conserva el contenido original del CV en `content/site.json`, en español e inglés, con los títulos de las obras y ponencias en su idioma original. Combina **Investigación y publicaciones** en una sola pestaña, y mantiene galería, docencia, conferencias, formación, becas, recursos y contacto.

## Qué hace el editor

TinaCMS ofrece dos paneles: formulario y previsualización de la página. Los cambios de contenido de `content/site.json` aparecen en tiempo real en la vista previa utilizando `useTina()`, antes de pulsar Guardar. También hay marcas para hacer clic sobre los campos visibles y enfocarlos en el editor. Para cambiar la distribución de página o el CSS todavía es necesario editar código.

**El plan gratuito de TinaCloud permite probar la edición visual**, pero tendrás que autorizar tú personalmente la conexión con GitHub. No introduzcas tokens de TinaCloud en la web pública ni envíes tus secretos por chat.

## Requisito previo: no sobrescribir el sitio que ya funciona

No subas todavía este ZIP completo al repositorio publicado. Es una migración de tecnología y exige pruebas de funcionamiento antes de sustituir el antiguo generador Python.

## Preparación, con GitHub y TinaCloud

1. Conserva el repositorio actual tal como está. Haz una copia de seguridad o crea una rama separada antes de sustituir ningún archivo.
2. Entra en https://app.tina.io/ y crea un proyecto gratuito vinculado con tu repositorio `ValeriaVRodriguezMorales/ValeriaVRodriguezMorales.github.io` (o, preferiblemente para probar, con un repositorio nuevo de pruebas). Autoriza únicamente el repositorio que hayas escogido.
3. Obtén en TinaCloud `NEXT_PUBLIC_TINA_CLIENT_ID` (identificador público) y `TINA_TOKEN` (token de lectura para compilación). `TINA_TOKEN` se guarda **solo** como GitHub Actions Secret, nunca en un archivo del repositorio.
4. Para probar en tu ordenador necesitas Node.js; ejecuta `npm install`. Crea tu propio `.env` local copiando `.env.example`, agrega las credenciales y ejecuta `npm run dev`. Accede a `http://localhost:3000/admin/index.html` para editar en dos paneles.
5. Para publicar automáticamente en GitHub Pages, la carpeta `.github/workflows` incluye `deploy-tina.yml`. Guarda ambos valores en **Settings → Secrets and variables → Actions**; el token como secreto. Revisa **Settings → Pages → Source: GitHub Actions**. Solo habilita el flujo de Tina después de desactivar el antiguo `deploy.yml` para evitar que ambas publicaciones se pisen.
6. Cuando la compilación termine correctamente, entra en `https://valeriavrodriguezmorales.github.io/admin/index.html`, autentícate en TinaCloud y edita el archivo `site.json` de la colección «CV académico completo». Pulsa Guardar para registrar los cambios en GitHub.

**Importante:** No se ha ejecutado una compilación Next.js ni una prueba de conexión con TinaCloud en este entorno porque no hay acceso a los paquetes NPM ni a tus credenciales. El proyecto es una **primera migración de código**, no una versión probada en producción. La estructura de la API sigue la documentación de TinaCMS para Next.js y exportación estática. Puede requerir ajustes de dependencias o esquema al compilar.

## Contenidos existentes

- 3 títulos académicos.
- 8 registros de investigación.
- 16 publicaciones bibliográficas (incluido el capítulo *Decolonizing environmental politics: sumak kawsay as a possible moral foundation for green policies* destacado en la portada).
- 9 registros docentes.
- 16 ponencias y participaciones académicas.
- 7 becas y reconocimientos.
- 3 idiomas.
- Galería y recursos preparados para añadir imágenes, videos, PDF y enlaces.

El nombre, los datos bibliográficos, los títulos y las fechas se han mantenido como estaban en los archivos de la versión anterior. No se han corregido erratas ni traducido títulos originales.

## Dónde se cambia cada parte

- `content/site.json`: todas las entradas y textos editables. TinaCMS gestiona este archivo mediante formularios.
- `tina/config.ts`: definición de campos del panel.
- `components/Site.jsx`: presentación visual y secciones.
- `components/routes.js`: las rutas bilingües.
- `styles/site.css`: tipografía, colores Oxford, diseño adaptable.
- `pages/[[...slug]].jsx`: consulta de TinaCMS, exportación estática y sincronización de la vista previa.
- `.github/workflows/deploy-tina.yml`: compilación y despliegue estático a GitHub Pages.

Los títulos de obras aparecen tal cual en `title`. Las descripciones de apoyo usan `description_es` y `description_en`. Para cargar una portada o foto utiliza los campos `image`/`photo`. Para un PDF utiliza una URL externa o súbelo a `public/uploads/docs` y enlaza `/uploads/docs/archivo.pdf` desde el editor.

## Referencias oficiales

- https://tina.io/docs/contextual-editing/react
- https://tina.io/docs/tinacloud/deployment-options/cloudflare-pages
- https://tina.io/pricing
- https://tina.io/docs/reference/types/object
- https://tina.io/docs/tinacloud/overview

## Revisión automática sin tocar la página pública

Si creas una rama **`tina-pruebas`** en tu repositorio y agregas allí los archivos de esta migración, el archivo `.github/workflows/probar-tina.yml` intentará compilarla y verificar su contenido, **sin publicar nada**. Es la manera recomendada de comprobar por primera vez los paquetes, el esquema y las credenciales de TinaCloud antes de sustituir el sitio público.

La rama `main` debe conservar el sitio actual hasta que la prueba termine correctamente. Si la compilación de prueba falla, la web publicada permanecerá intacta.
