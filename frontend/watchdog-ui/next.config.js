/** @type {import('next').NextConfig} */
const nextConfig = {
  // Set a reasonable timeout for static page generation
  staticPageGenerationTimeout: 120,

  // Optimize image handling for faster builds
  images: {
    unoptimized: true,
  },

  // Use SWC minification for faster builds
  swcMinify: true,

  // Optionally disable React strict mode temporarily to troubleshoot build issues
  reactStrictMode: false,

  // Limit the amount of static optimization
  experimental: {
    // Disable certain optimizations that might be causing timeouts
    serverMinification: true,
    serverSourceMaps: false,
  }
};

module.exports = nextConfig; 