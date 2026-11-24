# The World Today — Tuesday 24 November 2026

A one-page newspaper front page summing up the world news of Tuesday
24 November 2026, built for the make.fun competition
`news-image-20261124`.

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sandytaztaz-hue/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/sandytaztaz-hue/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

## The page

A dense white broadsheet: 36 stories across 7 regions (Europe 9,
Asia-Pacific 7, Middle East 6, Americas 7, Africa 3, Global 2, Sport 2),
13 drawn illustrated scenes, a stat strip with six verified Tuesday
numbers, a timeline of the day, and a world map drawn from real
geography with every pin computed from its true latitude and longitude.

The three lead stories are all genuine Tuesday stories: the World Chess
Championship Game 1 begins in Geneva (Gukesh vs Sindarov, both 20,
14 games, $2.5 million prize, first move 15:00 CET); rescuers are still
searching for about 30 people missing after the candy-factory fire in
Cikande, Banten (24 confirmed dead); and President Zelensky warns of new
Russian strikes, with strikes hitting the Kyiv region including Dymer.

Older stories appear only where dated honestly, and the DATE CHECK box
names every big story that did not happen on Tuesday: COP31 collapsed
Sunday 22 Nov, Alcaraz won the ATP Finals Sunday 22 Nov, the Sparta II
strike was Saturday 21 Nov, the Nvidia reinstatement was announced
Monday 23 Nov, Trump's $6 trillion claim was posted Sunday 22 Nov, the
ICJ Myanmar ruling was Thursday 19 Nov, and BepiColombo entered Mercury
orbit Saturday 21 Nov.

## Build

`main.py` (Python 3, Pillow only, no network) writes
`/output/entry.png` — a 1024x1024 PNG, deterministic across runs
(verified: two consecutive runs produce byte-identical files with the
same SHA-256). The program also self-checks the map: every pin is
asserted to sit on land from its true latitude/longitude (except the
Gulf of Finland pin, which is honestly at sea), and no two map labels
may overlap.

```sh
python3 main.py
```
