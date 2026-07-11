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
    ];

    function scanDir(dirPath: string, rootCategory: string) {
      if (!fs.existsSync(dirPath)) return;
      const entries = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dirPath, entry.name);
        
        if (entry.isDirectory()) {
          // Excludes standard dev and config folders
          if (['node_modules', '.next', '.git', '.turbo', 'dist', 'build', 'public', 'packages', 'brain', 'pnj photos'].includes(entry.name)) {
            continue;
          }
          scanDir(fullPath, rootCategory);
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          try {
            const rawContent = fs.readFileSync(fullPath, 'utf8');
            const stats = fs.statSync(fullPath);
            const { frontmatter, markdownContent } = parseFrontMatter(rawContent);

            // Outlines parsing
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

            const title = frontmatter.title || fileName.replace(/\.md$/, '').replace(/-/g, ' ');
            const slug = frontmatter.slug || slugify(title);
            const tags = Array.isArray(frontmatter.tags) ? frontmatter.tags : [];
            
            const words = markdownContent.split(/\s+/).filter(w => w.length > 0);
            const wordCount = words.length;
            const readingTime = Math.max(1, Math.ceil(wordCount / 200));

            const createdDate = frontmatter.date || new Date(stats.birthtimeMs).toISOString().split('T')[0];
            const updatedDate = new Date(stats.mtimeMs).toISOString().split('T')[0];
            const status = frontmatter.status || 'active';
            const description = frontmatter.description || frontmatter.summary || '';

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
            const rawContent = fs.readFileSync(fullPath, 'utf8');
            const stats = fs.statSync(fullPath);
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
              tags: Array.isArray(frontmatter.tags) ? frontmatter.tags : [],
              wordCount,
              readingTime: Math.max(1, Math.ceil(wordCount / 200)),
              createdDate: frontmatter.date || new Date(stats.birthtimeMs).toISOString().split('T')[0],
              updatedDate: new Date(stats.mtimeMs).toISOString().split('T')[0],
              status: frontmatter.status || 'active',
              description: frontmatter.description || frontmatter.summary || ''
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
