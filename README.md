# 20 November 2026 — The World in One Day

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/adelbudi88-crypto/news-image-20-nov/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/adelbudi88-crypto/news-image-20-nov/reward.svg)](https://make.fun/bounty/news-image-20261120)

A one-image front page summing up the world's news of Friday 20 November 2026, built for the [make.fun bounty](https://make.fun/bounty/news-image-20261120).

The image is a newspaper-style poster (1024x1024): a big navy header names the day, **20 November 2026**, and ten stories cover the day across regions and fields:

1. **Anthropic closes up 17% on its Nasdaq debut** (Tech, hero panel) — opened +34% at $111.50, closed $97.17; record $81.3bn IPO priced at $83 a share.
2. **Senate rejects Iran war-powers vote** (US Politics) — 51–48 against ending the war; the House-passed measure falls.
3. **UK sends 1,000 drones to Ukraine** (Europe) — £260m package; long-range drones fly 1,000 km.
4. **Taiwan plunges 2,394 points** (Markets) — Taiex −6.2% to 36,033; worst week since 1990, down 18%.
5. **Houthi missile hits Riyadh tower** (Middle East) — PIF Tower, the tallest in Riyadh, damaged; no injuries.
6. **North Korea fires ballistic missile** (Asia) — launch from Wonsan toward the East Sea after allied drills.
7. **Van Gogh sells for $190.4 million** (Culture) — Blossoming Chestnut Trees sets a record for the artist.
8. **US sanctions Comancheros, 'Ndrangheta** — US assets frozen in cartel crackdown.
9. **Trump pardons Pete Rose** — posthumous pardon for the late hit king, 4,256 hits.
10. **UK–EU youth mobility deal** — provisionally agree 100,000 places a year.

## How the image was made

`entry.png` was drawn from scratch with Python + Pillow (`tools/draw.py`): flat geometric illustrations (a Nasdaq board with the gold ANT ticker, the Capitol dome, a long-range drone, a plunging market chart, the PIF Tower, a missile over the sea, a framed Van Gogh) on an off-white newsprint background, navy ink, brick red and gold. No AI image generation, no downloaded images. Every number on the poster was verified against live news reports before drawing.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`. Running it twice writes byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
