# Página web académica personal (ES / EN)

Este proyecto está preparado para publicar gratuitamente el CV académico en **GitHub Pages** y modificarlo visualmente con **Pages CMS**. No necesitas pagar alojamiento ni aprender a programar para actualizar las secciones habituales.

La página usa una estética inspirada en el azul Oxford (`#002147`), fondos claros y **Times New Roman**, pero **no representa ni pertenece a la Universidad de Oxford**. No utiliza su escudo ni sus logotipos.

## Qué incluye

- Portada con presentación breve, formación doctoral y trabajos destacados.
- Secciones completas: **Investigación**, **Publicaciones**, **Docencia**, **Conferencias**, **Formación**, **Becas y distinciones**, **Recursos**, **Galería** y **Perfil y contacto**.
- Dos idiomas en rutas independientes: español e inglés. Los títulos de las obras y ponencias se muestran en su idioma original.
- Un espacio para subir fotografía, escribir una biografía en cada idioma, agregar contacto, enlaces académicos y cargar un CV PDF.
- Un gestor de publicaciones, investigaciones, docencia, conferencias, becas y recursos, con entradas editables desde Pages CMS.
- **Galería visual de publicaciones** (español e inglés): puedes subir una portada o imagen y enlazarla a la página donde se puede leer o comprar. Las imágenes se vuelven enlaces clicables; la sección queda inicialmente vacía hasta que incorpores las tuyas.
- Integración de videos públicos de YouTube, enlaces a PDFs y URL de presentaciones externas. La incrustación puede depender de las restricciones impuestas por cada plataforma.
- Diseño adaptable a móvil y ordenador, búsqueda de publicaciones y publicación automática de actualizaciones.

**Datos iniciales:** transcripción del CV proporcionado por la usuaria: 16 publicaciones y entradas de prensa, 16 participaciones en eventos académicos, 9 registros docentes, 8 de investigación, 3 de estudios y 7 de becas y reconocimientos. Las fechas y referencias se han preservado como aparecen en el documento, incluidas posibles erratas del CV que conviene revisar antes de publicar.

## Antes de publicar: ver la vista previa sin Internet

Abre la carpeta `vista-previa` y haz doble clic en **`inicio.html`**. Podrás navegar por las versiones española e inglesa y por todas las secciones sin subir nada a Internet. Esta carpeta **no se publicará** en GitHub: se excluye mediante `.gitignore`. La versión pública se construye desde los datos editables.

## PRIMER PASO: preparar una cuenta GitHub

1. Abre [https://github.com](https://github.com) y crea una cuenta si no tienes.
2. Anota tu **nombre de usuario exacto de GitHub**.
3. Descarga y descomprime el ZIP de este proyecto, conservando todas sus carpetas y archivos.
4. **No compres aún el dominio**. Primero publicaremos la página con la dirección gratuita `https://TUUSUARIO.github.io/`.

**Recomendación:** antes de ponerla en línea, revisa las secciones y confirma que quieres hacer públicos los antecedentes personales y académicos. Un repositorio gratuito de GitHub Pages suele ser público. No incluyas información privada que no quieras mostrar.

## SEGUNDO PASO: subir los archivos con GitHub Desktop

Esta vía evita comandos de terminal.

1. Descarga [GitHub Desktop](https://desktop.github.com/) y accede con tu cuenta GitHub.
2. En **File → Add local repository**, elige la carpeta descomprimida del proyecto. Si ofrece **Create a repository here**, acepta para inicializarla localmente.
3. Realiza un **commit** de los archivos con un mensaje como `Primera versión de mi web académica`.
4. Haz clic en **Publish repository** y establece como nombre **`TUUSUARIO.github.io`**, reemplazando `TUUSUARIO` por tu usuario real. Asegúrate de que el repositorio sea **público** (no marques **Keep this code private**).
5. Verifica en la página web de GitHub que aparecen las carpetas `src`, `scripts`, `public` y `.github`, además del archivo `.pages.yml`.
6. En el repositorio, abre **Settings → Pages**, y en **Build and deployment → Source** selecciona **GitHub Actions**.
7. En la pestaña **Actions**, el flujo llamado **Publicar sitio en GitHub Pages** genera y publica las páginas. Cuando indique éxito, abre `https://TUUSUARIO.github.io/`.

Si creaste previamente el repositorio desde el navegador, puedes clonarlo primero con GitHub Desktop y copiar los archivos del ZIP a la carpeta clonada antes de hacer el commit. **No crees dos repositorios con el mismo nombre.**

### Archivos ocultos en macOS

El proyecto incluye `.pages.yml` y `.github`, esenciales para edición y publicación. Si no los ves en Finder, utiliza **Comando + Mayúsculas + punto** para mostrar archivos ocultos. No borres esos archivos.

## TERCER PASO: editar visualmente, sin programar

1. Entra en [https://app.pagescms.org](https://app.pagescms.org).
2. Selecciona **Sign in with GitHub** e instala/autoriza Pages CMS en la cuenta dueña del repositorio. Puedes conceder acceso **solo** al repositorio `TUUSUARIO.github.io`.
3. Selecciona el repositorio y la rama `main`. El sistema utilizará la configuración `.pages.yml` que ya está preparada.
4. Encontrarás estas diez áreas editables:
   - **01 Perfil, foto y contacto**
   - **02 Publicaciones**
   - **03 Investigación y proyectos**
   - **04 Experiencia docente**
   - **05 Conferencias y eventos**
   - **06 Formación**
   - **07 Becas y distinciones**
   - **08 Idiomas**
   - **09 Material didáctico y divulgación**
   - **10 Galería de portadas y publicaciones**
5. Abre un registro, cambia un campo y pulsa **Save**. Pages CMS guarda el cambio en GitHub y GitHub Actions vuelve a generar el sitio. Tras una publicación exitosa, la modificación se ve en la página.

No hemos verificado el acceso de Pages CMS con tu cuenta todavía; ese paso requiere que tú autorices su aplicación en GitHub.

### Para colocar tu foto, biografía y datos de contacto

En Pages CMS, abre **01 Perfil, foto y contacto**. Aquí podrás completar los campos **Foto de perfil** (seleccionar y subir imagen), **Resumen biográfico ES**, **Biography EN**, **Correo electrónico público**, **ORCID**, **Google Scholar**, **PhilPapers** y **CV descargable en PDF**. Guarda los cambios: el recuadro de fotografía se sustituirá por tu imagen y los textos nuevos aparecerán en la web. La biografía y el contacto están vacíos deliberadamente.

### Para agregar una publicación

En **02 Publicaciones** añade una entrada. Rellena el título original, año, tipo de publicación y referencia bibliográfica completa. Si tienes DOI, URL del artículo, PDF en línea o URL incrustable, puedes añadirlos. Marca **Destacar en inicio** si quieres que aparezca entre las obras seleccionadas de la portada.

### Para añadir imágenes de publicaciones que enlacen a lecturas o compras

En Pages CMS abre **10 Galería de portadas y publicaciones** y pulsa **New**. Completa **Título original**, **Año**, **Fotografía o portada** (sube una imagen) y **Enlace donde leer o comprar la obra** (pega la dirección completa `https://...`). Elige **Leer**, **Comprar** o **Ver publicación**. Si quieres, completa las descripciones ES y EN; deja el título de la obra sin traducir. Guarda la nueva entrada. El sitio se publicará automáticamente y mostrará la imagen, que se podrá pulsar para abrir el enlace en una pestaña nueva.

Esta galería es **independiente** del listado bibliográfico, para que puedas mostrar portadas de libros, capítulos, números de revista o imágenes de artículos sin duplicar ni eliminar referencias del CV. No necesita contenido de ejemplo: aparecerá el primer elemento en cuanto lo agregues. Usa imágenes propias o con permiso de uso/publicación.

**Cambio solicitado en portada:** `Decolonizing environmental politics: sumak kawsay as a possible moral foundation for green policies` está marcado en **02 Publicaciones → Destacar en inicio** en lugar de `La physiología de los deseos frente a las hypolépseis pseudeîs sobre la ilimitada avidez humana. Dos conceptos epicúreos para un diálogo entre la ética hedonista y la ecosofía de Arne Naess`. Ambas obras siguen figurando en el listado bibliográfico.

### Para añadir un video, una presentación o PDF

En **09 Material didáctico y divulgación** crea una entrada nueva:

- **Video de YouTube:** pega un enlace público de YouTube en `Video YouTube` para mostrarlo en un reproductor integrado.
- **PDF:** pega una URL pública en `PDF en línea`; también puedes subir un PDF desde el gestor de documentos y usar su dirección `/uploads/docs/nombre.pdf`.
- **Presentación:** utiliza la URL de incrustación o de publicación facilitada por Google Slides, Canva, Genially u otra plataforma en `Presentación/PDF incrustable`. Los enlaces normales de edición no siempre funcionan para incrustar.
- **Enlace web:** el campo `Enlace web` agrega una vía alternativa para abrir el contenido.

**Limitación externa:** algunos artículos, revistas y plataformas no autorizan mostrarse dentro de un iframe. En ese caso, el enlace externo permitirá abrir el documento; no es posible forzar la incrustación.

## CUARTO PASO: vincular el dominio propio (cuando la web ya esté funcionando)

1. Compra el dominio que prefieras, solo cuando hayas elegido uno.
2. Configura los registros DNS según las instrucciones de GitHub Pages para tu registrador de dominios.
3. En GitHub abre **Settings → Pages → Custom domain** e introduce tu dominio.
4. Crea un archivo `CNAME` dentro de `public/` con solo el dominio, sin `https://`.
5. En `.github/workflows/deploy.yml`, reemplaza la línea de `SITE_URL` por `SITE_URL: https://tudominio.com`.
6. Publica esos cambios y activa **Enforce HTTPS** cuando GitHub habilite la opción.

Esta última configuración puedo hacerla contigo cuando llegue el momento. No es necesaria para publicar gratuitamente.

## Organización técnica (para saber qué pertenece a cada cosa)

| Archivo/carpeta | Para qué sirve |
| --- | --- |
| `src/data/profile.json` | Nombre, presentación, biografía, foto, contacto y PDF del CV |
| `src/data/publications/` | Publicaciones individuales |
| `src/data/research/` | Tesis, proyectos, estancias, supervisión y otras investigaciones |
| `src/data/teaching/` | Docencia y ayudantías |
| `src/data/talks/` | Ponencias, congresos, seminarios |
| `src/data/education/` | Estudios y titulaciones |
| `src/data/recognitions/` | Becas, premios, asociaciones y distinciones |
| `src/data/media/` | Videos y materiales que agregues después |
| `src/data/gallery/` | Galería de portadas, imágenes y enlaces para leer o comprar |
| `src/data/languages.json` | Idiomas y nivel |
| `.pages.yml` | Formularios visuales de Pages CMS |
| `scripts/build.py` | Generador de páginas; usa **solo Python estándar**, sin instalaciones adicionales en el servidor |
| `src/styles/site.css` | Diseño y colores |
| `.github/workflows/deploy.yml` | Publicación automática gratuita |
| `dist/` | Sitio generado, incluido en el ZIP para consulta pero regenerable |

**Para desarrolladores (opcional):** ejecuta `python3 scripts/build.py` desde la carpeta del proyecto. Si necesitas verlo en tu ordenador antes de publicarlo, desde la misma carpeta ejecuta `python3 -m http.server 8000 --directory dist` y abre `http://localhost:8000/` (esto requiere tener Python 3 instalado). En GitHub Actions Python ya está disponible.

## Revisión de contenidos

He conservado los títulos de trabajos, ponencias y libros en su idioma original. Las referencias bibliográficas se reproducen de acuerdo con el CV, mientras que las descripciones auxiliares de las secciones inglesas se han redactado en inglés. Antes de hacer pública la web, revisa especialmente las fechas y los nombres propios del documento original. Por ejemplo, el seminario de Pisa aparece con fecha **15/01/2024** en el CV proporcionado, y se ha mantenido sin corregirla automáticamente.

La web es estática: no necesita base de datos, cuenta de alojamiento ni servidor de correo. Los materiales pesados, como videos, conviene mantenerlos en plataformas externas. Las fotografías y PDFs que subas a GitHub serán públicos una vez publicados. 
