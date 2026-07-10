import React from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ArrowLeft, Calendar, Clock, Tag } from 'lucide-react';
import { getBlogPostBySlug, getBlogPosts } from '@/lib/content';
import { ReadingProgressBar } from '@/components/reading-progress';
import { ArticleShare } from '@/components/article-share';
import { NewsletterForm } from '@/components/newsletter-form';

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);
  if (!post) return { title: 'Article Not Found' };

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `/journal/${post.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `https://buildwithpnj.in/journal/${post.slug}`,
      type: 'article',
      publishedTime: post.publishDate,
      authors: ['Prakash Nandan Jha (PNJ)'],
      tags: post.tags,
      siteName: 'BuildWithPNJ',
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      creator: '@buildwithpnj',
    },
  };
}

// Helper to extract H2 headings for Table of Contents
function extractHeadings(html: string) {
  const h2Regex = /<h2>(.*?)<\/h2>/g;
  const headings = [];
  let match;
  while ((match = h2Regex.exec(html)) !== null) {
    const text = match[1].replace(/<[^>]*>?/gm, ''); // strip inline tags
    const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
    headings.push({ text, id });
  }
  return headings;
}

// Post-process HTML to inject slugified IDs into H2 headers for anchor scrolling
function injectHeadingIds(html: string) {
  return html.replace(/<h2>(.*?)<\/h2>/g, (match, title) => {
    const cleanTitle = title.replace(/<[^>]*>?/gm, '');
    const id = cleanTitle.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
    return `<h2 id="${id}">${title}</h2>`;
  });
}

export default async function PublicJournalDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);

  if (!post) {
    notFound();
  }

  // Pre-process HTML and extract headings
  const processedHtml = injectHeadingIds(post.contentHtml);
  const headings = extractHeadings(post.contentHtml);

  // Load related posts (up to 3, excluding current post)
  const relatedPosts = getBlogPosts()
    .filter(p => p.slug !== post.slug)
    .slice(0, 3);

  // Article URL for sharing
  const articleUrl = `https://buildwithpnj.in/journal/${post.slug}`;

  return (
    <div className="flex flex-col gap-10 text-left">
      
      {/* Dynamic reading progress bar */}
      <ReadingProgressBar />

      {/* Back button */}
      <div>
        <Link 
          href="/journal" 
          className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" /> Back to Journal
        </Link>
      </div>

      {/* Article Header */}
      <div className="flex flex-col gap-4 border-b border-border pb-8">
        <div className="flex flex-col gap-2">
          <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// ENGINEERING JOURNAL"}</div>
          <h1 className="text-3xl sm:text-4xl font-pixel text-foreground max-w-4xl leading-tight">{post.title}</h1>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1.5"><Calendar className="h-3.5 w-3.5" /> {post.publishDate}</span>
          <span>·</span>
          <span className="flex items-center gap-1.5"><Clock className="h-3.5 w-3.5" /> {post.readingTime} min read</span>
          <span>·</span>
          <span className="text-foreground">Prakash Nandan Jha (PNJ)</span>
        </div>

        <div className="flex flex-wrap gap-2 mt-2">
          {post.tags.map((tag) => (
            <span 
              key={tag} 
              className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-primary/5 text-primary"
            >
              <Tag className="h-2.5 w-2.5" /> #{tag}
            </span>
          ))}
        </div>
      </div>

      {/* Grid: TOC sidebar + Prose Content */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        
        {/* Table of Contents Sticky Sidebar */}
        <aside className="hidden lg:block lg:col-span-3 lg:sticky lg:top-24 h-fit max-w-[220px]">
          {headings.length > 0 && (
            <div className="p-5 rounded-2xl border border-border bg-card flex flex-col gap-4">
              <h3 className="font-pixel text-xs text-foreground uppercase tracking-wider">{"// ON THIS PAGE"}</h3>
              <nav className="flex flex-col gap-2.5 text-xs text-muted-foreground">
                {headings.map((h) => (
                  <a 
                    key={h.id} 
                    href={`#${h.id}`}
                    className="hover:text-foreground transition-colors leading-snug truncate"
                    title={h.text}
                  >
                    {h.text}
                  </a>
                ))}
              </nav>
            </div>
          )}
        </aside>

        {/* Prose Main Column */}
        <div className="lg:col-span-9 flex flex-col gap-10">
          
          {/* Post Markdown compiled Content */}
          <article 
            className="prose dark:prose-invert max-w-none text-foreground leading-relaxed 
                       prose-headings:font-pixel prose-headings:text-foreground 
                       prose-h2:text-xl prose-h2:border-b prose-h2:border-border prose-h2:pb-2 prose-h2:mt-8 
                       prose-code:text-primary prose-code:bg-secondary prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:border prose-code:border-border
                       prose-pre:bg-muted prose-pre:border prose-pre:border-border prose-pre:rounded-2xl prose-pre:p-5"
          >
            <div dangerouslySetInnerHTML={{ __html: processedHtml }} />
          </article>

          {/* Divider */}
          <div className="h-px bg-border" />

          {/* Dynamic Social Sharing Panel */}
          <ArticleShare url={articleUrl} title={post.title} />

          {/* Related Articles block */}
          {relatedPosts.length > 0 && (
            <div className="flex flex-col gap-6 border-t border-border pt-10 mt-6">
              <h3 className="font-pixel text-base text-foreground tracking-tight uppercase">{"// YOU MIGHT ALSO LIKE"}</h3>
              
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {relatedPosts.map((rPost) => (
                  <Link
                    key={rPost.slug}
                    href={`/journal/${rPost.slug}`}
                    className="group p-5 rounded-2xl border border-border bg-card hover:bg-accent flex flex-col justify-between gap-3 card-glow-hover"
                  >
                    <div className="flex flex-col gap-2">
                      <span className="text-[10px] text-muted-foreground">{rPost.publishDate}</span>
                      <h4 className="text-sm font-bold text-foreground group-hover:text-primary transition-colors line-clamp-2 leading-snug">
                        {rPost.title}
                      </h4>
                    </div>
                    <span className="text-[10px] text-primary group-hover:text-primary/80 font-semibold transition-colors mt-2">
                      Read Article →
                    </span>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* Newsletter Panel */}
          <div className="p-6 sm:p-8 rounded-2xl border border-border bg-card flex flex-col items-center text-center gap-6 mt-10">
            <div className="flex flex-col gap-1 max-w-sm">
              <h4 className="font-pixel text-base text-foreground">Subscribe to the Builder Crew</h4>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Enjoyed this article? Subscribe to receive new system design files.
              </p>
            </div>
            <NewsletterForm />
          </div>

        </div>

      </div>

    </div>
  );
}
