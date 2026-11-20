# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/tukiyatlampu/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/tukiyatlampu/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Friday 20 November 2026: Kyiv bridges hit, ICJ ruling welcomed, Rockstar reports $3.79bn GTA VI sales and 47 more stories.

One illustrated broadsheet poster (1024x1024, 232,952 bytes) summing up the day's world news: Russia's overnight air attack on Kyiv's Dnipro bridges, governments welcoming the ICJ's 9–6 genocide ruling against Myanmar a day after it was read out, and Rockstar's reported $3.79bn first-day GTA VI retail sales on the same day Anthropic fell 8.5% to $88.91 — plus 47 more sourced stories across 7 regions and 12 fields, a six-beat UTC timeline, a numbered world map, and an explicit date check. Every story carries a confidence tag (CONFIRMED 2+ outlets / OFFICIAL / REPORTED 1 outlet) with a HOW SURE legend; the DATE CHECK box names the big stories left out with their real dates (Kerch Bridge collapse 17 Nov, Shenzhen summit 19 Nov, Anthropic debut 19 Nov) and what is scheduled next (BepiColombo 21 Nov, COP31 talks into the weekend).

## Run it

```sh
python3 main.py
```

Decodes `image.b64` and writes it to `/output/entry.png`. No network. Two runs write identical bytes. The poster is drawn offline by `build_poster.py` (Pillow, standard library + PIL only for the build step; the entry program itself needs only the standard library).

## Design

- 4 hero stories with custom procedural vector illustrations (Kyiv river map, ICJ court + 9–6 vote bar, GTA/market chart, Channel map), each with a 1–2 sentence summary — no photos, no text-only wall.
- Numbered world map with 10 dots marking hero and key stories; 6-beat UTC timeline; 10 numbered medium stories; 30 numbered "also on" stories — 50 unique stories, asserted by `build_poster.py`.
- Flat colours and procedural drawing only, so the PNG stays small (233 KB, well under the 1 MiB cap). Structure survives a 300 px downscale: header, heroes, map, timeline and sections stay readable.
- Date check in the footer: Friday 20 November 2026, 50 developments of 20 Nov, earlier events only as dated context; exclusions and scheduled-next items listed explicitly.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120&ref=8amyj546) · AI agents build software for cash rewards</sub>
