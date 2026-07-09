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
    const files = fs.readdirSync(SOURCE_DIR)
      .filter((file) => /\.(png|jpe?g|webp|avif)$/i.test(file))
      .sort((a, b) => a.localeCompare(b));

    console.log(`Found ${files.length} source images to process...`);

    for (let i = 0; i < files.length; i++) {
      const sourceFile = path.join(SOURCE_DIR, files[i]);
      const targetFileName = `portrait-${i + 1}.webp`;
      const targetFile = path.join(TARGET_DIR, targetFileName);

      console.log(`Processing [${files[i]}] -> [${targetFileName}]...`);

      await sharp(sourceFile)
        .rotate()
        .resize({
          width: 1400,
          height: 1800,
          fit: 'cover',
          position: 'attention'
        })
        .sharpen({ sigma: 1.2, m1: 1.0, m2: 1.0 })
        .modulate({ brightness: 1.02, saturation: 1.04 })
        .webp({ quality: 92, effort: 6 })
        .toFile(targetFile);

      console.log(`Saved: ${targetFile}`);
    }

    console.log('All portraits successfully optimized and converted to sharper WebP assets!');
  } catch (error) {
    console.error('Error processing portraits:', error);
    process.exit(1);
  }
}

processPortraits();
