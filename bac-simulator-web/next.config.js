/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Static export for local development
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
