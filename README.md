# The World Today — Saturday, 21 November 2026

A one-page newspaper front page summing up the world news of
Saturday 21 November 2026, built for the make.fun competition
`news-image-20261121`.

## Stories on the page

- **Lead:** Russian missiles strike Poland; NATO calls it a grave violation.
- Wall Street slides into correction as AI stocks sell off (Nasdaq −5%+).
- The World Court finds Myanmar committed genocide against the Rohingya.
- A magnitude 6.8 earthquake shakes Peru, felt in Lima.
- Trump, Xi and Putin meet in Shenzhen with few concrete results.
- Britain and the EU sign food, carbon and youth deals.
- Israel taps Eisenkot over Netanyahu.

## How it works

- `stories.json` holds the day's stories (kicker, headline, short text,
  and the name of a pictogram motif for each).
- `generate.py` draws the 1024×1024 front page with Pillow: masthead,
  lead panel, a 2×2 story grid and a bottom strip. Every pictogram is
  drawn from shapes in code; nothing is downloaded.
- `main.py` is the entrypoint. It renders with `generate.py` when Pillow
  is available and otherwise copies the committed `entry.png`, then
  writes the result to `MAKEFUN_OUTPUT_DIR` (or `/output`).

The output is deterministic: the same `stories.json` always produces
byte-identical `entry.png`.

## Run it

```
python3 generate.py          # writes ./entry.png (needs Pillow)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
