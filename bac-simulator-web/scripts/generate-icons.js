#!/usr/bin/env node
/**
 * Generate all required icon sizes from the master SVG
 * Uses sharp for high-quality SVG to PNG conversion
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '..', 'public');
const svgPath = path.join(publicDir, 'icon.svg');

// All required icon sizes
const sizes = [
  // iOS App Icons
  { size: 1024, name: 'icon-1024.png' },   // App Store
  { size: 180, name: 'icon-180.png' },     // iPhone (3x)
  { size: 167, name: 'icon-167.png' },     // iPad Pro
  { size: 152, name: 'icon-152.png' },     // iPad
  { size: 120, name: 'icon-120.png' },     // iPhone (2x), Spotlight (3x)
  { size: 80, name: 'icon-80.png' },       // Spotlight (2x)
  { size: 76, name: 'icon-76.png' },       // iPad (1x)
  { size: 60, name: 'icon-60.png' },       // iPhone Notification (3x)
  { size: 58, name: 'icon-58.png' },       // Settings (3x)
  { size: 40, name: 'icon-40.png' },       // Spotlight (2x), Settings
  { size: 29, name: 'icon-29.png' },       // Settings (1x)
  { size: 20, name: 'icon-20.png' },       // Notification (2x)

  // PWA / Web Icons
  { size: 512, name: 'icon-512.png' },     // PWA
  { size: 192, name: 'icon-192.png' },     // PWA, Android

  // Favicons
  { size: 32, name: 'favicon-32.png' },    // Favicon
  { size: 16, name: 'favicon-16.png' },    // Favicon

  // Apple Touch Icons
  { size: 180, name: 'apple-touch-icon.png' },
];

async function generateIcons() {
  console.log('🎨 Generating icons from SVG...\n');

  const svgBuffer = fs.readFileSync(svgPath);

  for (const { size, name } of sizes) {
    const finalPath = path.join(publicDir, name);

    try {
      // Use appropriate density for the target size
      // Lower density for larger images to avoid pixel limit
      const density = size >= 512 ? 72 : Math.min(300, size * 3);

      await sharp(svgBuffer, { density })
        .resize(size, size, {
          fit: 'cover',
          background: { r: 0, g: 191, b: 174, alpha: 1 } // Primary Teal
        })
        .png({ compressionLevel: 9 })
        .toFile(finalPath);

      console.log(`  ✓ ${name} (${size}×${size})`);
    } catch (err) {
      console.error(`  ✗ ${name} - Error: ${err.message}`);
    }
  }

  console.log('\n✅ Icon generation complete!');
}

generateIcons().catch(console.error);
