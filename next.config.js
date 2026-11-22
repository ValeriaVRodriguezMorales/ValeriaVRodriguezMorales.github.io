/** Sitio estático, compatible con GitHub Pages. */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  reactStrictMode: true,
  images: { unoptimized: true },
};
module.exports = nextConfig;
