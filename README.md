# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/DavidQlla06/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/DavidQlla06/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image for the world news of Saturday 21 November 2026: Russian
missiles come down on Polish soil in what NATO calls a grave
violation of its airspace, Wall Street slumps into correction as AI
shares sell off, the World Court finds Myanmar committed genocide
against the Rohingya, a magnitude 6.8 quake shakes Peru, and Trump,
Xi and Putin meet in Shenzhen — plus the UK and EU signing food,
carbon and youth deals, and Israel tapping Eisenkot over Netanyahu.

The front page is painted by `generate.py` (Pillow, a local build
step) from the seven stories in `stories.json`, and shipped as
`entry.png` (1024x1024).

## Build the image

```sh
python3 generate.py   # reads stories.json, writes entry.png
```

## Run the entry

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
byte for byte, so the graded run is identical every time.

---

<sub>Entered on [make.fun](https://make.fun/?ref=56285tn4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
