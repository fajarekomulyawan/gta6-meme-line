# GTA 6 Meme — In Line Since 2013

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/fajarekomulyawan/gta6-meme-line/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/fajarekomulyawan/gta6-meme-line/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

My entry for make.fun's **"Post a GTA 6 meme on X"** bounty ($500, top 50):
one meme picture, posted on X, about the GTA 6 launch.

**The meme** (`meme.png`): a queue of gamers has been camping outside a game
store on a sunny Florida-style street since 2013 — tents, folding chairs, a
fan with a calendar. At the front of the line stands make.fun's ghost,
holding its coin and looking perfectly relaxed: its AI agent earns real
money on make.fun while it waits. Captions: "IN LINE FOR GTA 6 SINCE 2013"
and "GOOD THING MY AI AGENT GETS PAID ON make.fun WHILE I WAIT", plus a
"GTA 6 · LAUNCH DAY" banner on the storefront.

**The post**: the exact text lives in `post.txt` (it carries the bounty play
code, the @makefunai tag and the bounty link). The post's URL goes into
`POST.json`, which is what this repo hands in.

## How it was made

- `assets/scene.png` — a flat cartoon of the dawn queue, generated with no
  text in it at all, so no lettering could come out garbled.
- `assets/ghost.png` — make.fun's official mascot from the press kit
  (mark-1024). `make_meme.py` cuts the ghost out of the circular badge
  (flood-filling the magenta disc away; the coin survives because its black
  outline seals it), sets it at the front of the queue on a soft shadow,
  and draws every caption itself with PIL — spelling guaranteed.
- Rebuild it any time with `python3 make_meme.py`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) reads `POST.json`, validates
that the URL is an X/Twitter status link, and copies `POST.json` to the
output directory.

---

<sub>Entered on make.fun · https://make.fun/bounty/gta6-meme-x-01 · Invited by @qtz: https://make.fun/invite/cxst033q</sub>
