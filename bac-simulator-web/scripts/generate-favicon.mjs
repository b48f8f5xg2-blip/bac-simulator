import pngToIco from 'png-to-ico';
import { writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const publicDir = join(__dirname, '..', 'public');

try {
  const buf = await pngToIco([
    join(publicDir, 'favicon-16.png'),
    join(publicDir, 'favicon-32.png')
  ]);
  writeFileSync(join(publicDir, 'favicon.ico'), buf);
  console.log('✓ favicon.ico created');
} catch (err) {
  console.error('Error:', err);
}
