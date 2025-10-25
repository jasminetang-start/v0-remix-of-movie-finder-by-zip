/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // static export
  basePath: '/movie-finder-by-city',
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
