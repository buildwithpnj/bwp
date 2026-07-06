import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    const dirPath = path.join(process.cwd(), 'public', 'assets', 'images');
    
    if (!fs.existsSync(dirPath)) {
      return NextResponse.json({ portraits: [] });
    }
    
    const files = fs.readdirSync(dirPath);
    
    const portraits = files
      .filter(file => {
        const ext = path.extname(file).toLowerCase();
        return ['.jpg', '.jpeg', '.png', '.webp', '.avif'].includes(ext);
      })
      .map(file => `/assets/images/${file}`);
      
    return NextResponse.json({ portraits });
  } catch (error) {
    console.error('Failed to read portraits directory:', error);
    return NextResponse.json({ portraits: [] }, { status: 500 });
  }
}
