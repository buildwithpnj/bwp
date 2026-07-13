import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

interface MarkdownRecord {
  title: string;
  slug: string;
  fileName: string;
  relativePath: string;
  category: string;
  content: string;
  excerpt: string;
  headings: { level: number; text: string; id: string }[];
  tags: string[];
  wordCount: number;
  readingTime: number;
  createdDate: string;
  updatedDate: string;
  status: string;
  description: string;
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

function parseFrontMatter(content: string) {
  const frontmatter: Record<string, any> = {};
  let markdownContent = content;

  if (content.startsWith('---')) {
    const parts = content.split('---');
    if (parts.length >= 3) {
      const rawYaml = parts[1];
      markdownContent = parts.slice(2).join('---').trim();

      const lines = rawYaml.split('\n');
      for (const line of lines) {
        const colonIndex = line.indexOf(':');
        if (colonIndex !== -1) {
          const key = line.slice(0, colonIndex).trim();
          let value = line.slice(colonIndex + 1).trim();

          // Remove surrounding quotes
          if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
            value = value.slice(1, -1);
          }

          // Parse arrays like [a, b, c]
          if (value.startsWith('[') && value.endsWith(']')) {
            frontmatter[key] = value.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
          } else {
            frontmatter[key] = value;
          }
        }
      }
    }
  }
  return { frontmatter, markdownContent };
}

export async function GET() {
  try {
    const rootPath = path.resolve(process.cwd(), '..', '..');
    const records: MarkdownRecord[] = [];

    const scanDirs = [
      { path: path.join(rootPath, 'content'), category: 'content' },
      { path: path.join(rootPath, 'docs'), category: 'docs' },
      { path: path.join(rootPath, 'scripts'), category: 'scripts' },
      { path: path.join(rootPath, 'packages'), category: 'packages' },
      { path: path.join(rootPath, 'apps/api/app/services'), category: 'backend-services' },
      { path: path.join(rootPath, 'apps/api/app/routers'), category: 'backend-routers' },
      { path: path.join(rootPath, 'apps/api/app/models'), category: 'backend-models' },
    ];

    const allowedExtensions = ['.md', '.txt', '.py', '.ts', '.tsx', '.json', '.yml', '.yaml'];
    const dirExclusions = ['node_modules', '.next', '.git', '.turbo', 'dist', 'build', 'public', 'brain', 'pnj photos', '__pycache__', '.venv', 'venv', 'cache'];

    function scanDir(dirPath: string, rootCategory: string) {
      if (!fs.existsSync(dirPath)) return;
      const entries = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        
        if (entry.isDirectory()) {
          if (dirExclusions.includes(entry.name)) {
            continue;
          }
          scanDir(fullPath, rootCategory);
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name).toLowerCase();
          if (!allowedExtensions.includes(ext)) {
            continue;
          }

          try {
            let rawContent = fs.readFileSync(fullPath, 'utf8');
            const stats = fs.statSync(fullPath);
            
            // Limit content size to keep payload scalable
            if (rawContent.length > 50000) {
              rawContent = rawContent.slice(0, 50000) + '\n\n... [Content truncated for scalability] ...';
            }

            let title = '';
            let slug = '';
            let markdownContent = rawContent;
            let frontmatter: Record<string, any> = {};
            let headings: { level: number; text: string; id: string }[] = [];
            let tags: string[] = [];

            if (ext === '.md') {
              const parsed = parseFrontMatter(rawContent);
              frontmatter = parsed.frontmatter;
              markdownContent = parsed.markdownContent;

              // Outlines parsing
              const lines = markdownContent.split('\n');
              for (const line of lines) {
                const match = line.match(/^(#{1,6})\s+(.+)$/);
                if (match) {
                  const level = match[1].length;
                  const text = match[2].trim();
                  headings.push({ level, text, id: slugify(text) });
                }
              }
              title = frontmatter.title || entry.name.replace(/\.md$/, '').replace(/-/g, ' ');
              slug = frontmatter.slug || slugify(title);
              tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
            } else {
              title = entry.name;
              slug = slugify(entry.name);
              const langTag = ext.slice(1);
              tags = ['code', langTag];
              if (rootCategory === 'packages') tags.push('shared-package');
              if (rootCategory.startsWith('backend-')) tags.push('backend-core');
            }

            // Excerpt extraction
            let excerpt = '';
            const paragraphs = markdownContent
              .split('\n\n')
              .map(p => p.trim())
              .filter(p => p && !p.startsWith('#') && !p.startsWith('>') && !p.startsWith('-') && !p.startsWith('*') && !p.startsWith('`'));
            if (paragraphs.length > 0) {
              excerpt = paragraphs[0].slice(0, 160);
              if (paragraphs[0].length > 160) excerpt += '...';
            }

            const relativePath = path.relative(rootPath, fullPath).replace(/\\/g, '/');
            const fileName = entry.name;
            const categoryFromFolder = path.dirname(relativePath);

            const words = markdownContent.split(/\s+/).filter(w => w.length > 0);
            const wordCount = words.length;
            const readingTime = Math.max(1, Math.ceil(wordCount / 200));

            const createdDate = frontmatter.date || new Date(stats.birthtimeMs).toISOString().split('T')[0];
            const updatedDate = new Date(stats.mtimeMs).toISOString().split('T')[0];
            const status = frontmatter.status || 'active';
            const description = frontmatter.description || frontmatter.summary || `${title} file from project structure.`;

            records.push({
              title,
              slug,
              fileName,
              relativePath,
              category: frontmatter.category || categoryFromFolder,
              content: markdownContent,
              excerpt,
              headings,
              tags,
              wordCount,
              readingTime,
              createdDate,
              updatedDate,
              status,
              description
            });
          } catch (fileErr) {
            console.error(`Failed to index file ${fullPath}:`, fileErr);
          }
        }
      }
    }

    // Run scanner
    for (const sDir of scanDirs) {
      scanDir(sDir.path, sDir.category);
    }

    // Also scan root directory for top-level markdown files (e.g. README.md)
    if (fs.existsSync(rootPath)) {
      const rootFiles = fs.readdirSync(rootPath, { withFileTypes: true });
      for (const entry of rootFiles) {
        if (entry.isFile() && entry.name.endsWith('.md')) {
          const fullPath = path.join(rootPath, entry.name);
          try {
            let rawContent = fs.readFileSync(fullPath, 'utf8');
            const stats = fs.statSync(fullPath);
            
            if (rawContent.length > 50000) {
              rawContent = rawContent.slice(0, 50000) + '\n\n... [Content truncated for scalability] ...';
            }

            const { frontmatter, markdownContent } = parseFrontMatter(rawContent);

            const headings: { level: number; text: string; id: string }[] = [];
            const lines = markdownContent.split('\n');
            for (const line of lines) {
              const match = line.match(/^(#{1,6})\s+(.+)$/);
              if (match) {
                const level = match[1].length;
                const text = match[2].trim();
                headings.push({ level, text, id: slugify(text) });
              }
            }

            let excerpt = '';
            const paragraphs = markdownContent
              .split('\n\n')
              .map(p => p.trim())
              .filter(p => p && !p.startsWith('#') && !p.startsWith('>') && !p.startsWith('-') && !p.startsWith('*') && !p.startsWith('`'));
            if (paragraphs.length > 0) {
              excerpt = paragraphs[0].slice(0, 160);
              if (paragraphs[0].length > 160) excerpt += '...';
            }

            const title = frontmatter.title || entry.name.replace(/\.md$/, '').replace(/-/g, ' ');
            const words = markdownContent.split(/\s+/).filter(w => w.length > 0);
            const wordCount = words.length;

            records.push({
              title,
              slug: frontmatter.slug || slugify(title),
              fileName: entry.name,
              relativePath: entry.name,
              category: 'root',
              content: markdownContent,
              excerpt,
              headings,
              tags: Array.isArray(frontmatter.tags) ? [...frontmatter.tags, 'root'] : ['root'],
              wordCount,
              readingTime: Math.max(1, Math.ceil(wordCount / 200)),
              createdDate: frontmatter.date || new Date(stats.birthtimeMs).toISOString().split('T')[0],
              updatedDate: new Date(stats.mtimeMs).toISOString().split('T')[0],
              status: frontmatter.status || 'active',
              description: frontmatter.description || frontmatter.summary || `${title} root document.`
            });
          } catch (fileErr) {
            console.error(`Failed to index root file ${entry.name}:`, fileErr);
          }
        }
      }
    }

    return NextResponse.json({ records });
  } catch (error) {
    console.error('Failed to run knowledge base indexer:', error);
    return NextResponse.json({ records: [], error: String(error) }, { status: 500 });
  }
}
