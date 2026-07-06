const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const SOURCE_DIR = path.join(__dirname, '../pnj photos');
const TARGET_DIR = path.join(__dirname, '../apps/web/public/assets/images');

// Ensure target directory exists
if (!fs.existsSync(TARGET_DIR)) {
  fs.mkdirSync(TARGET_DIR, { recursive: true });
}

async function processPortraits() {
  try {
    const files = fs.readdirSync(SOURCE_DIR);
    const jpegFiles = files.filter(f => f.toLowerCase().endsWith('.jpeg') || f.toLowerCase().endsWith('.jpg'));

    console.log(`Found ${jpegFiles.length} JPEGs to process...`);

    for (let i = 0; i < jpegFiles.length; i++) {
      const sourceFile = path.join(SOURCE_DIR, jpegFiles[i]);
      const targetFileName = `portrait-${i + 1}.webp`;
      const targetFile = path.join(TARGET_DIR, targetFileName);

      console.log(`Processing [${jpegFiles[i]}] -> [${targetFileName}]...`);

      await sharp(sourceFile)
        .resize({
          width: 800,
          height: 1000,
          fit: 'cover',
          position: 'center'
        })
        .webp({ quality: 85 })
        .toFile(targetFile);

      console.log(`Saved: ${targetFile}`);
    }

    console.log('All portraits successfully optimized and converted to WebP!');
  } catch (error) {
    console.error('Error processing portraits:', error);
    process.exit(1);
  }
}

processPortraits();
