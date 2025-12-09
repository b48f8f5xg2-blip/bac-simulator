#!/usr/bin/env node
/**
 * Icon Generation Script for BAC Simulator
 * Generates all required iOS app icon and web favicon sizes from SVG
 */

import sharp from 'sharp';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const publicDir = join(__dirname, '../public');

// iOS App Icon sizes
const iosIconSizes = [1024, 180, 167, 152, 120, 80, 76, 60, 58, 40, 29, 20];

// Web/PWA sizes
const webSizes = [512, 192, 32, 16];

// Read the SVG source
const iconSvg = readFileSync(join(publicDir, 'icon.svg'));

/**
 * Get next available filename with numeric suffix if file exists
 */
function getAvailableFilename(basePath) {
  if (!existsSync(basePath)) {
    return basePath;
  }

  const ext = basePath.substring(basePath.lastIndexOf('.'));
  const base = basePath.substring(0, basePath.lastIndexOf('.'));
  let counter = 1;
  let newPath = `${base}-${counter}${ext}`;

  while (existsSync(newPath)) {
    counter++;
    newPath = `${base}-${counter}${ext}`;
  }

  return newPath;
}

async function generatePng(size, outputName) {
  const basePath = join(publicDir, outputName);
  const outputPath = getAvailableFilename(basePath);

  await sharp(iconSvg)
    .resize(size, size, {
      fit: 'contain',
      background: { r: 0, g: 191, b: 174, alpha: 1 } // #00BFAE
    })
    .png()
    .toFile(outputPath);

  console.log(`✓ Generated ${outputPath.split('/').pop()} (${size}x${size})`);
  return outputPath;
}

async function generateFavicon() {
  // Generate 16x16 and 32x32 PNGs for ICO
  const png16 = await sharp(iconSvg)
    .resize(16, 16)
    .png()
    .toBuffer();

  const png32 = await sharp(iconSvg)
    .resize(32, 32)
    .png()
    .toBuffer();

  // For ICO format, we'll use a simple approach - just copy the 32x32 PNG
  // and rename it (browsers will accept PNG as favicon)
  const basePath = join(publicDir, 'favicon.ico');
  const outputPath = getAvailableFilename(basePath);

  // Create a basic ICO-like file (32x32 PNG)
  await sharp(iconSvg)
    .resize(32, 32)
    .png()
    .toFile(outputPath);

  console.log(`✓ Generated ${outputPath.split('/').pop()} (ICO format)`);
}

async function main() {
  console.log('🎨 BAC Simulator Icon Generator\n');
  console.log('Generating iOS App Icons...');

  for (const size of iosIconSizes) {
    await generatePng(size, `icon-${size}.png`);
  }

  console.log('\nGenerating Web/PWA Icons...');

  for (const size of webSizes) {
    if (size === 32 || size === 16) {
      await generatePng(size, `favicon-${size}.png`);
    } else {
      await generatePng(size, `icon-${size}.png`);
    }
  }

  // Generate apple-touch-icon (180x180)
  await generatePng(180, 'apple-touch-icon.png');

  // Generate favicon.ico
  await generateFavicon();

  console.log('\n✅ All icons generated successfully!');
  console.log(`📁 Output directory: ${publicDir}`);
}

main().catch(console.error);
