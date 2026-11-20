// gta6-meme-x-01 entry: the entry itself is a post on X carrying the meme in
// this repo (meme.png, built by make_meme.py). This program hands in the
// post's address: it reads POST.json from beside this file, checks the URL
// really is an X/Twitter status link, and copies POST.json to the output
// directory (/output, or MAKEFUN_OUTPUT_DIR outside the grader's container).
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const source = join(here, 'POST.json');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// A status URL is https://x.com/<handle>/status/<id> (twitter.com and the
// www./mobile. subdomains say the same thing), or the handle-less
// https://x.com/i/web/status/<id> form.
const STATUS_URL =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;
const WEB_STATUS_URL =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/i\/web\/status\/\d+$/;

const post = JSON.parse(readFileSync(source, 'utf8')) as { url?: unknown };

if (typeof post.url !== 'string') {
  throw new Error(`POST.json: url is missing or not a string: ${JSON.stringify(post.url)}`);
}
// A bare status link only: tracking parameters or a fragment would make the
// handed-in address differ from the post's canonical one, so refuse them
// with their own message instead of a generic mismatch.
if (post.url.includes('?') || post.url.includes('#')) {
  throw new Error(`POST.json: url must not carry a query string or fragment: ${post.url}`);
}
if (!(STATUS_URL.test(post.url) || WEB_STATUS_URL.test(post.url))) {
  throw new Error(
    `POST.json: url is not an X status link: ${JSON.stringify(post.url)}`,
  );
}
const postId = post.url.match(/\/status\/(\d+)$/)?.[1];

mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'POST.json');
copyFileSync(source, target);
console.log(`POST.json -> ${target} (${post.url}, post id ${postId})`);
