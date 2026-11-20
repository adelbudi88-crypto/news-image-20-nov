// News-image entry for 20 November 2026 (Node 22, standard library only).
//
// The poster itself is entry.png next to this file. It was drawn from
// scratch with Python + Pillow by tools/draw.py: a front page naming the
// day, 20 November 2026, with the Anthropic IPO debut as the hero story,
// six more top stories in a grid, and a short "MORE TODAY" strip.
//
// This program does nothing but place that finished image where the
// grader expects it. There is no network, no randomness and no clock
// involved, so running it twice writes exactly the same bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const fileName = 'entry.png';

mkdirSync(destination, { recursive: true });
const png = readFileSync(join(here, fileName));
writeFileSync(join(destination, fileName), png);
