// gta6-meme-x-01 entry (Node 22, standard library only): it copies POST.json
// from the repository root to /output/POST.json, where the gate reads it.
// That is all the program has to do. The entry is the post itself: an AI
// agent made a GTA 6 meme, it is posted on X from a public account with
// make.fun (a link) and @makefunai and the play code in its text, POST.json
// names the post, and the house reads the post from X (its first picture
// and its text) and hands that to the judge. Nothing this program writes
// about the post is judged.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
const postPath = join(BOT_DIR, 'POST.json');
// Fail fast with a clear error when POST.json is not a JSON object naming
// an X post, instead of copying a broken file the gate would refuse.
let post;
try {
  post = JSON.parse(readFileSync(postPath, 'utf8'));
} catch (err) {
  console.error(`POST.json could not be read as JSON from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof post !== 'object' || post === null || typeof post.url !== 'string') {
  console.error('POST.json must be a JSON object with a string "url" naming an X post.');
  process.exit(1);
}
try {
  copyFileSync(postPath, join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
