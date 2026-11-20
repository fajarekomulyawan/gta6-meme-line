#!/usr/bin/env python3
"""Build the gta6-meme-x-01 entry picture: "In line for GTA 6 since 2013".

Composites three things into REPO/meme.png (1200x1200):
  1. assets/scene.png  - a flat cartoon dawn queue outside a game store
                         (Florida-style street, palms, pastel art-deco),
                         generated text-free on purpose.
  2. assets/ghost.png  - make.fun's official mascot (press kit mark-1024).
                         The press file is the full badge (ghost on a magenta
                         disc inside a black ring), so the ghost character is
                         cut out of the badge first: the disc is flood-filled
                         away (the coin survives - its black outline seals it)
                         and everything outside the disc's radius is dropped.
  3. Captions drawn here with PIL/DejaVu: a top bar, a storefront banner
     ("GTA 6 - LAUNCH DAY" style) and a two-line bottom bar, so every word
     in the picture is spelled by code, never by an image model.

Run:  python3 make_meme.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CANVAS = 1200
BAR = (12, 10, 14)          # near-black caption bars
MAGENTA = (196, 28, 131)    # make.fun disc/coin magenta, sampled from the mark
WHITE = (255, 255, 255)

TOP_TEXT = "IN LINE FOR GTA 6 SINCE 2013"
BANNER_TEXT = "GTA 6 \u00b7 LAUNCH DAY"
BOTTOM_LINES = [
    "GOOD THING MY AI AGENT GETS PAID",
    "ON make.fun WHILE I WAIT",
]

GHOST_HEIGHT = 470          # ~39% of the picture height
GHOST_CENTER_X = 395
GHOST_FEET_Y = 1052         # just above the bottom caption bar


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int,
             start: int) -> ImageFont.FreeTypeFont:
    """Largest DejaVu Bold at or below `start` px that fits `max_width`."""
    size = start
    while size > 10:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT_BOLD, 10)


def centered(draw: ImageDraw.ImageDraw, cx: int, cy: int, text: str,
             font: ImageFont.FreeTypeFont, fill) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text((cx - w / 2 - box[0], cy - h / 2 - box[1]), text,
              font=font, fill=fill)


def extract_ghost() -> Image.Image:
    """Cut the ghost character out of the circular press badge."""
    badge = Image.open(ASSETS / "ghost.png").convert("RGBA")
    rgb = badge.convert("RGB")
    w, h = badge.size
    cx, cy = w // 2, h // 2

    # Flood-fill the magenta disc with a sentinel colour. The fill stops at
    # black outlines, so the ghost's body and the (also magenta) coin it
    # holds - both sealed by their outlines - survive untouched.
    sentinel = (0, 255, 1)
    ImageDraw.floodfill(rgb, (cx, 95), sentinel, thresh=90)

    # Radius of the magenta disc: scan down the centre column for the first
    # sentinel pixel. Everything beyond that radius is badge ring/background.
    r_disc = 0
    for y in range(cy):
        if rgb.getpixel((cx, y)) == sentinel:
            r_disc = cy - y
            break

    px = rgb.load()
    alpha = Image.new("L", (w, h), 255)
    apx = alpha.load()
    r2 = (r_disc - 2) ** 2
    for y in range(h):
        for x in range(w):
            if px[x, y] == sentinel or (x - cx) ** 2 + (y - cy) ** 2 > r2:
                apx[x, y] = 0
    # Soften the cut edge a touch so the ghost sits in the scene, not on it.
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(
        ImageFilter.GaussianBlur(0.8))
    badge.putalpha(alpha)
    return badge.crop(badge.getbbox())


def main() -> None:
    scene = Image.open(ASSETS / "scene.png").convert("RGB")
    scene = scene.resize((CANVAS, CANVAS), Image.LANCZOS)
    img = scene.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # --- top caption bar -------------------------------------------------
    draw.rectangle([0, 0, CANVAS, 104], fill=BAR)
    font = fit_font(draw, TOP_TEXT, 1140, 62)
    centered(draw, CANVAS // 2, 52, TOP_TEXT, font, WHITE)

    # --- bottom caption bar (two lines) ----------------------------------
    draw.rectangle([0, 1068, CANVAS, CANVAS], fill=BAR)
    for i, line in enumerate(BOTTOM_LINES):
        font = fit_font(draw, line, 1140, 54)
        centered(draw, CANVAS // 2, 1110 + i * 52, line, font, WHITE)

    # --- storefront banner on the shop fascia ----------------------------
    banner = [716, 494, 1176, 562]
    draw.rounded_rectangle(banner, radius=10, fill=MAGENTA,
                           outline=BAR, width=4)
    font = fit_font(draw, BANNER_TEXT, banner[2] - banner[0] - 30, 48)
    centered(draw, (banner[0] + banner[2]) // 2,
             (banner[1] + banner[3]) // 2, BANNER_TEXT, font, WHITE)

    # --- the ghost, front of the line, standing on the ground ------------
    ghost = extract_ghost()
    scale = GHOST_HEIGHT / ghost.height
    ghost = ghost.resize((round(ghost.width * scale), GHOST_HEIGHT),
                         Image.LANCZOS)
    gx = GHOST_CENTER_X - ghost.width // 2
    gy = GHOST_FEET_Y - GHOST_HEIGHT

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([GHOST_CENTER_X - 215, GHOST_FEET_Y - 20,
                   GHOST_CENTER_X + 215, GHOST_FEET_Y + 24],
                  fill=(0, 0, 0, 100))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(6)))
    img.alpha_composite(ghost, (gx, gy))

    out = HERE / "meme.png"
    img.convert("RGB").save(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
