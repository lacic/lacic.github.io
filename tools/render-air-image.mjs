#!/usr/bin/env node
/**
 * Regenerates public/air-areas.png from tools/air/compose.html.
 *
 * Why a rendered image rather than inline SVG: the tiles need Infobip's real
 * squircle shape (CSS `corner-shape`, not a border-radius approximation), the
 * icons come from research.infobip.com as masked SVGs, and the labels are set in
 * IBM Plex Sans — the same webfont as the page around it. Chrome already knows
 * how to do all three correctly, so we let it, once, and commit the result.
 *
 * Run: npm run image
 * Requires Google Chrome. It is only needed when the areas or their styling
 * change, which is roughly never — the committed PNG is what the site serves,
 * so a contributor without Chrome can still build the site.
 */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { existsSync } from 'node:fs';
import { readFile, rm, stat } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('.', import.meta.url));
const out = fileURLToPath(new URL('../public/air-areas.png', import.meta.url));

// The tiles are laid out 4x2 at this size; the device scale factor doubles it,
// so the committed PNG is 2480x1240 and stays sharp on a retina display.
const WIDTH = 1240;
const HEIGHT = 620;

const CHROME_CANDIDATES = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.css': 'text/css; charset=utf-8',
};

const chrome = process.env.CHROME_PATH ?? CHROME_CANDIDATES.find((path) => existsSync(path));
if (!chrome) {
  console.error(
    'Could not find Google Chrome. Install it, or set CHROME_PATH to the binary.\n' +
      'This script is only needed to regenerate the research-areas image; the site\n' +
      'builds fine without it because public/air-areas.png is committed.',
  );
  process.exit(1);
}

// A real server rather than a file:// URL, because webfonts and mask-image do
// not load reliably from the filesystem in headless Chrome.
const server = createServer(async (request, response) => {
  const url = new URL(request.url ?? '/', 'http://localhost');
  const path = join(root, normalize(decodeURIComponent(url.pathname)).replace(/^(\.\.[/\\])+/, ''));
  try {
    const info = await stat(path);
    if (info.isDirectory()) throw new Error('directory');
    response.writeHead(200, { 'content-type': MIME[extname(path)] ?? 'application/octet-stream' });
    response.end(await readFile(path));
  } catch {
    response.writeHead(404).end('not found');
  }
});

// Port 0: let the OS pick a free one, so a stray server from another session
// cannot break the render.
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const port = server.address().port;
console.log(`▶ serving tools/ on http://localhost:${port}`);

const args = [
  '--headless=new',
  '--disable-gpu',
  '--hide-scrollbars',
  '--no-sandbox',
  '--default-background-color=00000000',
  '--force-device-scale-factor=2',
  `--window-size=${WIDTH},${HEIGHT}`,
  // Generous, because the webfont has to arrive before the screenshot is taken.
  '--virtual-time-budget=8000',
  `--user-data-dir=${join(root, '.chrome-profile')}`,
  `--screenshot=${out}`,
  `http://localhost:${port}/air/compose.html`,
];

// Remove the old image first, so "the file exists" is proof of a fresh render
// rather than of the previous run.
await rm(out, { force: true });

console.log('▶ rendering with Chrome…');
const child = spawn(chrome, args, { stdio: ['ignore', 'ignore', 'pipe'] });
child.stderr.on('data', (chunk) => {
  const text = String(chunk);
  // Chrome is noisy on stderr even on success; only surface real failures.
  if (/error|fail/i.test(text) && !/DevTools|Fontconfig|GPU|dbus|Crashpad/i.test(text)) process.stderr.write(text);
});

/**
 * `--screenshot` writes the PNG and then, in this Chrome version, declines to
 * exit. So we watch for the file instead of waiting on the process: once its
 * size has stopped changing the image is complete, and we stop Chrome ourselves.
 */
const DEADLINE = Date.now() + 60_000;
let lastSize = -1;
let done = false;

while (Date.now() < DEADLINE) {
  await new Promise((resolve) => setTimeout(resolve, 500));
  if (!existsSync(out)) continue;
  const { size } = await stat(out);
  if (size > 0 && size === lastSize) {
    done = true;
    break;
  }
  lastSize = size;
}

child.kill('SIGTERM');
setTimeout(() => child.kill('SIGKILL'), 2000).unref();
server.close();

if (!done) {
  console.error('✗ Chrome did not produce an image within 60s.');
  console.error('  Try running the command in tools/air/compose.html\'s comment by hand to see what it says.');
  process.exit(1);
}

console.log(`✓ wrote public/air-areas.png (${(lastSize / 1024).toFixed(0)} kB, ${WIDTH * 2}×${HEIGHT * 2})`);
console.log('  Check it before committing: the labels must be IBM Plex Sans, not a fallback.');
process.exit(0);
