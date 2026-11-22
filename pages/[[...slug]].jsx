import { useTina } from 'tinacms/dist/react';
import client from '../tina/__generated__/client';
import Site from '../components/Site';
import { ALL_ROUTES } from '../components/routes';

export default function SitePage(props) {
  // Tina actualiza data.site en el navegador según lo editado en el panel.
  const { data } = useTina({ query: props.query, variables: props.variables, data: props.data });
  return <Site content={data?.site || props.data?.site} lang={props.lang} section={props.section} />;
}

export async function getStaticPaths() {
  return { paths: ALL_ROUTES.map((r) => ({ params: { slug: r.route ? r.route.split('/') : [] } })), fallback: false };
}
export async function getStaticProps({ params }) {
  const route = (params?.slug || []).join('/');
  const entry = ALL_ROUTES.find((x) => x.route === route);
  if (!entry) return { notFound: true };
  const response = await client.queries.site({ relativePath: 'site.json' });
  return { props: { ...response, lang: entry.lang, section: entry.section } };
}
