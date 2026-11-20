#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster (1024x1024 PNG).

Illustrated broadsheet, not text-only (postmortem news-image-20261118):
a hero tier of 4 big stories, each with a custom procedural vector
illustration (Kyiv map, ICJ court, GTA/market chart, Channel map); a
numbered world map with dots; a 6-beat UTC timeline; 10 numbered
medium stories; and 30 numbered "also on" stories -- 50 stories in
all, every one reported on Friday 20 November 2026. Each story carries
a confidence tag (CONFIRMED 2+ outlets / OFFICIAL / REPORTED 1 outlet)
and the footer DATE CHECK box lists the big stories deliberately left
out (with their real dates) plus what had not happened yet.

Flat colours and procedural drawing only, so the PNG stays small. No
network, no clock, no randomness: the same input always draws the
same bytes. Pillow is the only dependency (build step).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
CARD = (255, 253, 247)
INK = (22, 22, 22)
NAVY = (15, 42, 68)
RED = (139, 26, 26)
GREEN = (34, 110, 45)
MUTED = (90, 100, 115)
RULE = (180, 172, 150)
TIMELINE_BG = (226, 232, 238)
MAP_BG = (214, 230, 240)
MAP_LAND = (216, 208, 188)
MAP_LINE = (150, 142, 120)
GOLD = (255, 205, 90)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CONF_COLOR = {
    "CONFIRMED": GREEN,
    "OFFICIAL": NAVY,
    "REPORTED": MUTED,
    "CLAIM": (176, 120, 0),
    "FORECAST": (110, 60, 140),
}


def font(path, size):
    return ImageFont.truetype(path, size)


# (headline, summary, confidence, sources, illustration)
HEROES = [
    (
        "Russia hits Kyiv bridges in overnight air attack",
        "Overnight 19\u201320 Nov, Ukraine reports 110+ missiles, 400+ "
        "drones; 3 Dnipro bridges damaged, 9 killed, 28 hurt. Debris "
        "lands in Poland; NATO jets scramble.",
        "CONFIRMED",
        "AL JAZEERA \u00b7 CNN \u00b7 REUTERS",
        "kyiv",
    ),
    (
        "Governments welcome ICJ genocide ruling; Myanmar rejects it",
        "A day after the 9\u20136 genocide verdict on the Rohingya "
        "campaign \u2014 the first against a state \u2014 capitals welcome "
        "it; reparations ordered. Myanmar rejects it.",
        "CONFIRMED",
        "AL JAZEERA \u00b7 CNN \u00b7 BBC",
        "icj",
    ),
    (
        "Rockstar reports $3.79bn in first-day GTA VI sales",
        "First-day retail sales, per Rockstar; 32.5m GTA VI units sold "
        "before release. Also: Anthropic \u22128.5% to $88.91.",
        "OFFICIAL",
        "ROCKSTAR VIA REUTERS",
        "gta",
    ),
    (
        "UK and EU seal reset deal at Brussels summit",
        "Deal to ease food checks, link carbon markets, open youth "
        "mobility for up to 100,000 a year. Andy Burnham claims "
        "+0.5% GDP.",
        "CONFIRMED",
        "AL JAZEERA \u00b7 NPR",
        "channel",
    ),
]

# (when, headline, sources, confidence) -- stories 5-10.
TIMELINE = [
    ("12:33 UTC", "Amnesty: Spanish police used excessive force in strike",
     "REUTERS", "REPORTED"),
    ("15:00 UTC", "Florida: Cocoa gauge hits record 18.7 ft",
     "FOX WEATHER \u00b7 NWS", "CONFIRMED"),
    ("17:00 UTC", "Trump defends \u2018friend\u2019 Putin after Xi talks",
     "REUTERS \u00b7 AP", "CONFIRMED"),
    ("17:12 UTC", "Blast on Iran\u2019s Qeshm Island from munitions disposal",
     "REUTERS", "REPORTED"),
    ("TIME NOT STATED", "Somalia expels UAE ambassador over sovereignty",
     "AFRICANEWS \u00b7 AP", "CONFIRMED"),
    ("TIME NOT STATED", "581 women killed in South Africa in three months",
     "BBC", "CONFIRMED"),
]

# (headline, sources, confidence) -- stories 11-20, medium tier.
MEDIUM = [
    ("Vance declines to say he would have ordered Iran strikes",
     "REUTERS", "REPORTED"),
    ("Liverpool fan cleared in Semenyo abuse case",
     "SKY SPORTS", "CONFIRMED"),
    ("Cyclone Akvan hits Odisha; no deaths reported Friday",
     "THE HINDU \u00b7 NDTV", "CONFIRMED"),
    ("France seeks UN council meeting after Kyiv strikes",
     "REUTERS", "REPORTED"),
    ("Saudi coalition intercepts Houthi missile, hits Hodeida",
     "REUTERS \u00b7 GULF NEWS", "CONFIRMED"),
    ("Iraqi forces enter Jurf al-Sakhar stronghold",
     "AP \u00b7 AFP", "CONFIRMED"),
    ("China tells Japan to change attitude over Taiwan",
     "STRAITS TIMES \u00b7 AFP", "CONFIRMED"),
    ("South Korea confirms first cholera case in 10 years",
     "AP", "CONFIRMED"),
    ("Bukele registers for third term in El Salvador",
     "AL JAZEERA \u00b7 AP", "CONFIRMED"),
    ("Mamdani unveils plan to close Rikers by 2032",
     "REUTERS \u00b7 CNN \u00b7 AP", "CONFIRMED"),
]

# (headline, sources, confidence) -- stories 21-50, "also on" tier.
ALSO = [
    ("House Judiciary releases warning letters over document destruction",
     "CNN", "REPORTED"),
    ("Judge Brinkema to issue indefinite Arch injunction",
     "NY POST \u00b7 AP", "CONFIRMED"),
    ("Student protests in 25+ nations over funding, climate",
     "REUTERS", "CONFIRMED"),
    ("Dominique de Villepin launches French presidential bid",
     "AP \u00b7 AFP", "CONFIRMED"),
    ("Florida State routs Green Bay 87-63 in Friday matinee",
     "REUTERS", "CONFIRMED"),
    ("UN talks on regulating \u2018killer robots\u2019 drag past deadline",
     "REUTERS", "REPORTED"),
    ("Tanker hit by projectile off Oman, fire reported aboard",
     "REUTERS \u00b7 UKMTO", "CONFIRMED"),
    ("Report: Israel, US weigh renewed Iran strikes, Democrats seek ban",
     "CBS", "REPORTED"),
    ("Two permanent members oppose Grynspan in UN poll",
     "REUTERS", "REPORTED"),
    ("Milky Way bar shock births stars, Norma arm in doubt",
     "PHYS.ORG", "REPORTED"),
    ("Inner ear rewrites low-frequency hearing rule",
     "MEDICALXPRESS", "REPORTED"),
    ("Immune ageing blueprint points to cancer fight",
     "MEDICALXPRESS", "REPORTED"),
    ("Savara: FDA to miss rare lung drug deadline",
     "REUTERS", "CONFIRMED"),
    ("SEC probes Nvidia accounting, sources say",
     "REUTERS", "REPORTED"),
    ("Yale finds excitons move like light in atom sheet",
     "PHYS.ORG", "CONFIRMED"),
    ("Cairns Taipans sink Perth 98-90 in NBL home win",
     "AAP \u00b7 NBL", "CONFIRMED"),
    ("Etihad extends Saudi flight halt to Nov 30",
     "GULF NEWS", "REPORTED"),
    ("Mongolia bids farewell to outgoing president Khurelsukh",
     "MONTSAME", "OFFICIAL"),
    ("Japan core inflation +2.2% in Oct, above BoJ target",
     "JAPAN TIMES \u00b7 CNBC", "CONFIRMED"),
    ("Sydney man charged with car bomb plot, Daesh material",
     "AP", "REPORTED"),
    ("Xi, Prabowo launch China-Indonesia trade talks",
     "CGTN \u00b7 STRAITS TIMES", "CONFIRMED"),
    ("South Korean court orders retrial of ex-PM Han",
     "JAPAN TIMES \u00b7 CBC", "CONFIRMED"),
    ("Tunisian activist Ben Sedrine sentenced to 5 years",
     "PANA", "REPORTED"),
    ("Zimbabwe destroys 250,000 landmines, funding gaps remain",
     "AFRICANEWS", "REPORTED"),
    ("Drone, artillery strikes reported near Badme border",
     "ALLAFRICA", "REPORTED"),
    ("Drone strike kills 10 at gold mine in South Kordofan",
     "ALLAFRICA", "REPORTED"),
    ("Dozens missing after migrant boat capsizes off Senegal",
     "BBC \u00b7 AL JAZEERA", "CONFIRMED"),
    ("Brazil central bank sells $1bn to curb dollar slide",
     "MERCOPRESS", "REPORTED"),
    ("Brazil recognises ancestral land of chief Raoni",
     "AL JAZEERA \u00b7 LE MONDE", "CONFIRMED"),
    ("Nikkei falls about 5% as AI sell-off spreads in Asia",
     "CNBC TV18 \u00b7 REUTERS", "CONFIRMED"),
]

# Big stories deliberately left out, with their real dates.
EXCLUSIONS = [
    ("Kerch Bridge arch collapse", "17 Nov"),
    ("ICJ ruling read out", "19 Nov"),
    ("Shenzhen summit + peace declaration", "19 Nov"),
    ("Anthropic IPO debut", "19 Nov"),
    ("GTA VI launch", "19 Nov"),
    ("Kenya\u2019s last Ebola patient sent home", "11 Nov"),
]

# Big events that had not happened yet on 20 Nov.
NOTYET = [
    ("BepiColombo reaches Mercury", "21 Nov"),
    ("COP31 talks continue into weekend", "21\u201322 Nov"),
    ("NFL Mexico City game", "22 Nov"),
]

# (story number, lon, lat) for the numbered world-map dots.
DOTS = [
    (1, 30.5, 50.4),    # Kyiv
    (2, 1.0, 53.0),     # The Hague (nudged west so 2 and 4 do not overlap)
    (3, -74.0, 40.7),   # New York (Rockstar / Take-Two)
    (4, 7.5, 49.5),     # Brussels (nudged east so 2 and 4 do not overlap)
    (13, 85.0, 19.8),   # Gopalpur, Odisha (Cyclone Akvan landfall)
    (15, 42.9, 14.8),   # Hodeida
    (18, 127.0, 37.5),  # Seoul
    (40, 151.2, -33.9), # Sydney
    (43, 10.2, 36.8),   # Tunis
    (49, -60.0, -5.0),  # Amazon / Raoni land
]

# Rough continent outlines as (lon, lat) polygons -- schematic only.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
     (-65, 45), (-80, 32), (-90, 21), (-105, 20), (-120, 34), (-125, 49),
     (-150, 60), (-168, 66)],
    [(-80, 10), (-60, 5), (-35, -5), (-40, -20), (-55, -35), (-70, -50),
     (-75, -30), (-80, -15), (-80, 10)],
    [(-17, 15), (-10, 30), (10, 37), (20, 32), (35, 28), (43, 12),
     (51, 10), (40, -5), (35, -20), (20, -35), (15, -25), (12, 5),
     (0, 5), (-10, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (10, 57),
     (18, 56), (28, 60), (28, 68), (32, 66), (32, 58), (30, 50),
     (30, 45), (23, 40), (18, 40), (12, 44), (8, 38), (0, 36), (-10, 36)],
    [(35, 68), (60, 70), (90, 75), (120, 73), (150, 70), (170, 66),
     (162, 60), (158, 52), (140, 40), (127, 35), (120, 25), (108, 12),
     (100, 8), (95, 15), (90, 22), (80, 8), (75, 20), (65, 25),
     (55, 26), (50, 30), (45, 30), (40, 36), (40, 50), (40, 68)],
    [(113, -22), (114, -30), (125, -32), (135, -35), (145, -38),
     (150, -37), (153, -27), (146, -19), (142, -11), (135, -12),
     (130, -13), (122, -17), (114, -22)],
]


def shrink(d, text, path, size, max_w, floor=10):
    """Largest font size <= size at which text fits max_w."""
    while size > floor and d.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_kyiv(d, x0, y0, w, h):
    """Night sky, the Dnipro river, three bridges under attack."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 32, 58))
    for bx in (x0 + 14, x0 + 52, x0 + 96, x0 + 126):
        d.rectangle([bx, y0 + h - 26, bx + 12, y0 + h - 6], fill=(40, 58, 92))
    d.polygon([(x0 + 58, y0), (x0 + 92, y0), (x0 + 72, y0 + h),
               (x0 + 38, y0 + h)], fill=(64, 128, 190))
    for by in (y0 + 26, y0 + 58, y0 + 90):
        d.line([x0 + 8, by, x0 + w - 8, by - 6], fill=(230, 230, 230), width=4)
        d.line([x0 + 40, by - 10, x0 + 52, by + 2], fill=RED, width=3)
        d.line([x0 + 40, by + 2, x0 + 52, by - 10], fill=RED, width=3)
    for cx, cy, r in ((x0 + 118, y0 + 18, 7), (x0 + 30, y0 + 66, 5),
                      (x0 + 96, y0 + 100, 6)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 170, 40))
        d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3],
                  outline=(255, 205, 90), width=1)
    d.text((x0 + 8, y0 + 3), "DNIPRO \u00b7 3 BRIDGES HIT",
           font=font(FONT_BOLD, 10), fill=(255, 255, 255))


def draw_icj(d, x0, y0, w, h):
    """Peace Palace pediment and columns, with the 9-6 vote bar."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210))
    d.polygon([(x0 + 20, y0 + 30), (x0 + w - 20, y0 + 30),
               (x0 + w // 2, y0 + 6)], fill=NAVY)
    for cx in (x0 + 30, x0 + 58, x0 + 86, x0 + 114):
        d.rectangle([cx, y0 + 34, cx + 10, y0 + 64], fill=(120, 112, 96))
    d.rectangle([x0 + 16, y0 + 64, x0 + w - 16, y0 + 70], fill=NAVY)
    d.rectangle([x0 + 10, y0 + 70, x0 + w - 10, y0 + 76], fill=(120, 112, 96))
    d.text((x0 + 8, y0 + 80), "VOTE  9 \u2013 6",
           font=font(FONT_BOLD, 12), fill=RED)
    d.rectangle([x0 + 8, y0 + 96, x0 + 8 + 78, y0 + 104], fill=GREEN)
    d.rectangle([x0 + 90, y0 + 96, x0 + 90 + 52, y0 + 104],
                fill=MUTED)


def draw_gta(d, x0, y0, w, h):
    """Two independent tiles: one GTA sales bar; one Anthropic down-mark.

    No line series: a single bar stands for the one aggregate sales
    figure, and a down-triangle marks the one-day fall. Neither tile
    implies a trend or a relationship between the two facts.
    """
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 24, 20))
    mid = y0 + h // 2
    d.line([x0, mid, x0 + w, mid], fill=(90, 100, 90), width=1)
    d.text((x0 + 8, y0 + 4), "$3.79bn FIRST-DAY SALES",
           font=font(FONT_BOLD, 10), fill=(80, 200, 110))
    d.line([x0 + 40, mid - 6, x0 + 106, mid - 6],
           fill=(120, 130, 120), width=1)
    d.rectangle([x0 + 58, mid - 34, x0 + 88, mid - 6],
                fill=(80, 200, 110))
    d.text((x0 + 8, mid + 4), "ANTHROPIC \u22128.5%",
           font=font(FONT_BOLD, 10), fill=(255, 120, 110))
    d.polygon([(x0 + 73, mid + 48), (x0 + 58, mid + 24),
               (x0 + 88, mid + 24)], fill=RED)


def draw_channel(d, x0, y0, w, h):
    """The Channel: Britain and Europe, three deal icons."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 230, 240))
    d.text((x0 + 8, y0 + 3), "TRADE \u00b7 CARBON \u00b7 YOUTH",
           font=font(FONT_BOLD, 9), fill=NAVY)
    d.polygon([(x0 + 8, y0 + 24), (x0 + 44, y0 + 20), (x0 + 52, y0 + 56),
               (x0 + 40, y0 + 86), (x0 + 14, y0 + 78), (x0 + 6, y0 + 48)],
              fill=MAP_LAND, outline=MAP_LINE)
    d.polygon([(x0 + 66, y0 + 22), (x0 + 138, y0 + 18), (x0 + 144, y0 + 86),
               (x0 + 96, y0 + 90), (x0 + 64, y0 + 64)],
              fill=MAP_LAND, outline=MAP_LINE)
    d.text((x0 + 16, y0 + 46), "UK", font=font(FONT_BOLD, 10), fill=NAVY)
    d.text((x0 + 100, y0 + 46), "EU", font=font(FONT_BOLD, 10), fill=NAVY)
    for cx, label in ((x0 + 10, "TRADE"), (x0 + 58, "CARBON"),
                      (x0 + 110, "YOUTH")):
        d.rectangle([cx, y0 + 96, cx + 7, y0 + 103], fill=NAVY)
        d.text((cx + 10, y0 + 94), label, font=font(FONT_BOLD, 8),
               fill=NAVY)


ILLUSTRATIONS = {
    "kyiv": draw_kyiv,
    "icj": draw_icj,
    "gta": draw_gta,
    "channel": draw_channel,
}


def draw_map(d, x0, y0, w, h):
    """Schematic world map with numbered story dots."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG)

    def px(lon, lat):
        return (x0 + int((lon + 170) / 360.0 * w),
                y0 + int((75 - lat) / 135.0 * h))

    for poly in CONTINENTS:
        d.polygon([px(lon, lat) for lon, lat in poly],
                  fill=MAP_LAND, outline=MAP_LINE)
    for num, lon, lat in DOTS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED,
                  outline=(255, 255, 255), width=2)
        label = str(num)
        tw = d.textlength(label, font=font(FONT_BOLD, 11))
        d.text((cx - tw / 2, cy - 8), label, font=font(FONT_BOLD, 11),
               fill=(255, 255, 255))


def draw_poster(path):
    total = len(HEROES) + len(TIMELINE) + len(MEDIUM) + len(ALSO)
    assert total == 50, f"story count is {total}, must be 50"
    assert len(HEROES) == 4 and len(TIMELINE) == 6
    assert len(MEDIUM) == 10 and len(ALSO) == 30
    heads = ([h[0] for h in HEROES] + [t[1] for t in TIMELINE]
             + [m[0] for m in MEDIUM] + [a[0] for a in ALSO])
    assert len(set(heads)) == 50, "duplicate headline"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # ---- Header -------------------------------------------------
    d.rectangle([0, 0, W, 60], fill=NAVY)
    d.text((24, 8), "WORLD NEWS", font=font(FONT_BOLD, 30),
           fill=(255, 255, 255))
    d.text((24, 40), "FRIDAY 20 NOVEMBER 2026",
           font=font(FONT_BOLD, 15), fill=GOLD)
    right = "50 STORIES \u00b7 7 REGIONS \u00b7 12 FIELDS"
    d.text((W - 24 - d.textlength(right, font=font(FONT_BOLD, 18)), 10),
           right, font=font(FONT_BOLD, 18), fill=(255, 255, 255))
    d.text((W - 24 - d.textlength("DEVELOPMENTS OF 20 NOV 2026",
                                  font=font(FONT_REG, 12)), 38),
           "DEVELOPMENTS OF 20 NOV 2026", font=font(FONT_REG, 12),
           fill=(200, 210, 220))
    y = 66

    # ---- Hero tier: 4 illustrated features ----------------------
    card_w, card_h, gap = 484, 112, 8
    for idx, (head, summ, conf, src, art) in enumerate(HEROES):
        cx = 24 + (idx % 2) * (card_w + gap)
        cy = y + (idx // 2) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD,
                    outline=RULE, width=1)
        ILLUSTRATIONS[art](d, cx + 1, cy + 1, 146, card_h - 2)
        tx = cx + 158
        tw = card_w - 158 - 10
        d.text((tx, cy + 6), f"{idx + 1}", font=font(FONT_BOLD, 18),
               fill=RED)
        num_w = d.textlength(f"{idx + 1}", font=font(FONT_BOLD, 18))
        hl = wrap(d, head, font(FONT_BOLD, 15), tw - num_w - 8)[:2]
        hy = cy + 6
        for line in hl:
            d.text((tx + num_w + 8, hy), line, font=font(FONT_BOLD, 15),
                   fill=INK)
            hy += 18
        lines = wrap(d, summ, font(FONT_REG, 11), tw)[:3]
        ly = cy + 46
        for line in lines:
            d.text((tx, ly), line, font=font(FONT_REG, 11), fill=INK)
            ly += 14
        tag = f"{conf} \u00b7 {src}"
        tf = shrink(d, tag, FONT_BOLD, 10, tw)
        d.text((tx, cy + card_h - 15), tag, font=tf,
               fill=CONF_COLOR[conf])
    y += 2 * card_h + gap

    # ---- Numbered world map --------------------------------------
    y += 6
    d.text((24, y), "WHERE IT HAPPENED \u2014 DOTS MARK STORIES "
           "1\u20134, 13, 15, 18, 40, 43, 49",
           font=font(FONT_BOLD, 11), fill=NAVY)
    y += 16
    draw_map(d, 24, y, W - 48, 90)
    y += 90

    # ---- UTC timeline strip --------------------------------------
    y += 6
    d.text((24, y), "THE DAY AS REPORTED \u00b7 UTC",
           font=font(FONT_BOLD, 12), fill=NAVY)
    y += 18
    d.rectangle([0, y, W, y + 80], fill=TIMELINE_BG)
    col_w = (W - 48) // 3
    for idx, (when, what, src, conf) in enumerate(TIMELINE):
        ccx = 24 + (idx % 3) * col_w
        ccy = y + 4 + (idx // 3) * 38
        d.ellipse([ccx, ccy + 2, ccx + 8, ccy + 10],
                  fill=CONF_COLOR[conf])
        d.text((ccx + 12, ccy), when, font=font(FONT_BOLD, 12), fill=RED)
        wf = shrink(d, what, FONT_REG, 12, col_w - 16, floor=10)
        d.text((ccx, ccy + 14), what, font=wf, fill=INK)
        d.text((ccx, ccy + 27), f"{idx + 5:02d} \u00b7 {src}",
               font=font(FONT_BOLD, 9), fill=MUTED)
    y += 80

    # ---- Medium stories, numbered 11-20 -------------------------
    y += 8
    d.text((24, y), "THE DAY IN TEN",
           font=font(FONT_BOLD, 13), fill=RED)
    y += 18
    col_x = [24, W // 2 + 12]
    col_w = W // 2 - 36
    for idx, (head, src, conf) in enumerate(MEDIUM):
        ci = idx // 5
        cy = y + (idx % 5) * 22
        num = str(11 + idx)
        d.text((col_x[ci], cy), num, font=font(FONT_BOLD, 14), fill=RED)
        nw = d.textlength(num, font=font(FONT_BOLD, 14))
        src_fnt = font(FONT_BOLD, 10)
        src_w = d.textlength(src, font=src_fnt)
        hf = shrink(d, head, FONT_REG, 14,
                    col_w - nw - src_w - 22, floor=11)
        d.text((col_x[ci] + nw + 8, cy + 1), head, font=hf, fill=INK)
        d.ellipse([col_x[ci] + col_w - src_w - 12, cy + 5,
                   col_x[ci] + col_w - src_w - 4, cy + 13],
                  fill=CONF_COLOR[conf])
        d.text((col_x[ci] + col_w - src_w, cy + 2), src, font=src_fnt,
               fill=MUTED)
    y += 5 * 22

    # ---- Also on, numbered 21-50 ---------------------------------
    y += 6
    d.text((24, y), "ALSO ON \u2014 FRIDAY 20 NOVEMBER",
           font=font(FONT_BOLD, 13), fill=RED)
    y += 16
    for idx, (head, src, conf) in enumerate(ALSO):
        ci = idx // 15
        cy = y + (idx % 15) * 15
        num = str(21 + idx)
        d.text((col_x[ci], cy), num, font=font(FONT_BOLD, 11), fill=RED)
        nw = d.textlength(num, font=font(FONT_BOLD, 11))
        src_fnt = font(FONT_BOLD, 9)
        src_w = d.textlength(src, font=src_fnt)
        hf = shrink(d, head, FONT_REG, 12,
                    col_w - nw - src_w - 20, floor=9)
        d.text((col_x[ci] + nw + 6, cy), head, font=hf, fill=INK)
        d.ellipse([col_x[ci] + col_w - src_w - 10, cy + 3,
                   col_x[ci] + col_w - src_w - 3, cy + 10],
                  fill=CONF_COLOR[conf])
        d.text((col_x[ci] + col_w - src_w, cy + 1), src, font=src_fnt,
               fill=MUTED)
    y += 15 * 15

    # ---- Footer: date check + how sure ---------------------------
    y += 6
    d.line([24, y, W - 24, y], fill=RULE, width=2)
    y += 6
    check = ("DATE CHECK \u2713  Friday 20 November 2026  \u00b7  "
             "50 developments of 20 Nov  \u00b7  "
             "earlier events only as dated context")
    d.text((24, y), check, font=font(FONT_BOLD, 13), fill=NAVY)
    y += 18
    d.text((24, y), "NOT 20 NOV \u2014 LEFT OUT:",
           font=font(FONT_BOLD, 10), fill=RED)
    y += 13
    ex_cols = [[], []]
    for i, (what, when) in enumerate(EXCLUSIONS):
        ex_cols[i % 2].append(f"{what} ({when})")
    for ci, items in enumerate(ex_cols):
        ex = "  \u00b7  ".join(items)
        ef = shrink(d, ex, FONT_REG, 10, W // 2 - 24, floor=8)
        d.text((24 + ci * (W // 2), y), ex, font=ef, fill=MUTED)
    y += 13
    ny = "SCHEDULED NEXT:  " + "  \u00b7  ".join(f"{w} ({d_})" for w, d_ in NOTYET)
    nyf = shrink(d, ny, FONT_REG, 10, W - 48, floor=8)
    d.text((24, y), ny, font=nyf, fill=MUTED)
    y += 13
    lx = 24
    d.text((lx, y), "HOW SURE:", font=font(FONT_BOLD, 10), fill=NAVY)
    lx += d.textlength("HOW SURE: ", font=font(FONT_BOLD, 10))
    for conf, meaning in (("CONFIRMED", "2+ outlets"),
                          ("OFFICIAL", "announced"),
                          ("REPORTED", "1 outlet")):
        d.ellipse([lx, y + 2, lx + 7, y + 9], fill=CONF_COLOR[conf])
        lx += 11
        seg = f"{conf} = {meaning}   "
        d.text((lx, y), seg, font=font(FONT_BOLD, 10), fill=INK)
        lx += d.textlength(seg, font=font(FONT_BOLD, 10))
    d.text((lx, y), "\u2014 no CLAIM or FORECAST stories used.",
           font=font(FONT_REG, 10), fill=MUTED)
    y += 14

    assert y <= H - 4, f"poster overflow: final y={y}"
    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    out = os.environ.get("POSTER_OUT", "/tmp/ni20.png")
    draw_poster(out)
    n = os.path.getsize(out)
    print(f"wrote {out}: {n} bytes ({n / 1048576:.2f} MiB), limit 1048576")
    print("stories:", len(HEROES) + len(TIMELINE) + len(MEDIUM) + len(ALSO))
