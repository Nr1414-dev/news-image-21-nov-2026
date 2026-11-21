# The World in One Day — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Nr1414-dev/news-image-21-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Nr1414-dev/news-image-21-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261121)

A newspaper front page that sums up the world's news of **Saturday 21 November 2026** in one image: Russian missiles landing in Poland, Wall Street sliding into correction, the US detailing $12bn in Venezuelan oil revenue, a fourth weekend of cost-of-living protests in France, deadly strikes on Kryvyi Rih, and the Palisades Fire conviction in Los Angeles.

## The six stories

1. **Russian missiles hit Poland** — Two missiles and a suspected drone come down in south-east Poland during a huge Russian attack on Ukraine. Prime Minister Donald Tusk calls it an intentional provocation; NATO Secretary-General Mark Rutte calls it a grave violation of allied airspace. No one in Poland is hurt.
2. **Wall Street slides into correction** — US stocks fall sharply, with the S&P 500 down about 3.7% and into correction territory as AI shares sell off and Anthropic shares slide.
3. **US details $12bn in Venezuelan oil cash** — The US State Department publishes a report tracking more than $12bn in revenue from Venezuelan oil and mineral resources, nearly a year after US forces captured Nicolás Maduro.
4. **Fourth weekend of cost-of-living protests** — France sees a fourth consecutive weekend of nationwide demonstrations against rising prices.
5. **Kryvyi Rih: 2 dead, 42 hurt in strikes** — Russian strikes hit the Ukrainian city of Kryvyi Rih, killing two people and injuring 42, including four children.
6. **Palisades Fire: man found guilty** — A Los Angeles jury convicts Jonathan Rinderknecht of starting the Palisades Fire.

## How it is made

`draw.py` draws the front page from scratch with PIL (1024×1024, deterministic) and saves it as `entry.png`. `main.ts` copies that image to `/output/entry.png`, which is all the graded program does — no network, no randomness, so both runs write identical bytes.

## Run it

```sh
python3 draw.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Competition

Entry for [news-image-20261121](https://make.fun/bounty/news-image-20261121) on [make.fun](https://make.fun).
