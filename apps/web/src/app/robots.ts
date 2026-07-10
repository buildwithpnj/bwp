import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: [
        '/dashboard',
        '/notes',
        '/finance',
        '/books',
        '/habits',
        '/agent-inbox',
        '/storage',
        '/tools',
        '/ai-coach',
        '/ai-memory',
        '/assets',
        '/calendar',
        '/knowledge',
        '/media',
        '/projects-dashboard',
        '/recovery',
        '/settings',
        '/trash',
        '/workspace',
      ],
    },
    sitemap: 'https://buildwithpnj.in/sitemap.xml',
  };
}
