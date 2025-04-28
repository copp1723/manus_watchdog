const nextConfig = {
  /* config options here */
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  staticPageGenerationTimeout: 60,
  swcMinify: true,
  images: {
    // process.env is available in Node.js environment
    unoptimized: process.env.NODE_ENV === 'development',
  },
  reactStrictMode: false,
}

export default nextConfig
