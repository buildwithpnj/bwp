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
      ],
    },
    sitemap: 'https://buildwithpnj.in/sitemap.xml',
  };
}
