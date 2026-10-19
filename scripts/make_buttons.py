#!/usr/bin/env python3
"""Render the README "frosted glass" buttons as transparent PNGs.

    python scripts/make_buttons.py

GitHub strips custom CSS and fonts from a README, so the rounded translucent
buttons are drawn here (Chromium via Playwright) and embedded as images, with a
light and a dark variant each. Output: assets/buttons/<key>_{light,dark}.png
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "buttons"

ARROW = ('<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 11 11 5M6 5h5v5"/></svg>')
BOOK = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 3.2c1.9-.4 3.9-.2 5.5 1 1.6-1.2 3.6-1.4 5.5-1v8.6'
        'c-1.9-.4-3.9-.2-5.5 1-1.6-1.2-3.6-1.4-5.5-1z M8 4.2v8.6"/></svg>')

# key: (label, kind, icon)   kind: primary | secondary | active | tag
BUTTONS = {
    "report_en": ("Interactive report", "primary", ARROW),
    "report_fr": ("Rapport interactif", "primary", ARROW),
    "other_report_en": ("Interactive report (EN)", "secondary", ARROW),
    "other_report_fr": ("Rapport interactif (FR)", "secondary", ARROW),
    "notebook": ("Notebook", "secondary", BOOK),
    "lang_en_on": ("English", "active", ""),
    "lang_en_off": ("English", "secondary", ""),
    "lang_fr_on": ("Français", "active", ""),
    "lang_fr_off": ("Français", "secondary", ""),
    "tag_python": ("Python 3", "tag", ""),
    "tag_sklearn": ("scikit-learn", "tag", ""),
    "tag_xgboost": ("XGBoost", "tag", ""),
    "tag_shap_en": ("SHAP", "tag", ""),
    "tag_mit_en": ("MIT license", "tag", ""),
    "tag_mit_fr": ("Licence MIT", "tag", ""),
}

THEMES = {
    "light": dict(
        text="#1d1d1f", sec_text="#1d1d1f", tag_text="#515154",
        fill="linear-gradient(180deg, rgba(255,255,255,.95) 0%, rgba(226,233,248,.62) 100%)",
        ring="rgba(60,72,110,.16)", hi="rgba(255,255,255,.95)", shadow="rgba(40,56,110,.13)",
        p_fill="linear-gradient(180deg, rgba(120,170,255,.34) 0%, rgba(0,122,255,.20) 100%)",
        p_text="#0b4aa8", p_ring="rgba(0,100,230,.30)", p_hi="rgba(255,255,255,.75)", p_shadow="rgba(0,90,220,.20)",
        a_fill="linear-gradient(180deg, rgba(60,70,100,.20) 0%, rgba(60,70,100,.12) 100%)", a_text="#1d1d1f",
        t_fill="linear-gradient(180deg, rgba(255,255,255,.80) 0%, rgba(232,237,247,.50) 100%)",
    ),
    "dark": dict(
        text="#f5f5f7", sec_text="#f5f5f7", tag_text="#b4b9c4",
        fill="linear-gradient(180deg, rgba(255,255,255,.17) 0%, rgba(255,255,255,.07) 100%)",
        ring="rgba(255,255,255,.20)", hi="rgba(255,255,255,.30)", shadow="rgba(0,0,0,.45)",
        p_fill="linear-gradient(180deg, rgba(90,160,255,.42) 0%, rgba(10,110,255,.26) 100%)",
        p_text="#cfe3ff", p_ring="rgba(120,175,255,.42)", p_hi="rgba(255,255,255,.34)", p_shadow="rgba(10,100,255,.30)",
        a_fill="linear-gradient(180deg, rgba(255,255,255,.30) 0%, rgba(255,255,255,.16) 100%)", a_text="#ffffff",
        t_fill="linear-gradient(180deg, rgba(255,255,255,.11) 0%, rgba(255,255,255,.04) 100%)",
    ),
}


def page(label, kind, icon, th):
    c = THEMES[th]
    fill, color, ring, hi, shadow = c["fill"], c["sec_text"], c["ring"], c["hi"], c["shadow"]
    size, pad_x, h, weight = 15, 20, 40, 560
    if kind == "primary":
        fill, color, ring, hi, shadow = c["p_fill"], c["p_text"], c["p_ring"], c["p_hi"], c["p_shadow"]
        weight = 600
    elif kind == "active":
        fill, color, weight = c["a_fill"], c["a_text"], 600
    elif kind == "tag":
        fill, color = c["t_fill"], c["tag_text"]
        size, pad_x, h, weight = 12.5, 14, 30, 520
        shadow = "rgba(0,0,0,0)"
    return f"""<!doctype html><meta charset=utf-8><style>
html,body{{margin:0;background:transparent}}
body{{padding:14px;display:inline-block}}
.b{{display:inline-flex;align-items:center;gap:8px;height:{h}px;box-sizing:border-box;padding:0 {pad_x}px;
 border-radius:999px;font:{weight} {size}px/1 Inter,'Helvetica Neue',Arial,sans-serif;letter-spacing:-.005em;
 color:{color};background:{fill};white-space:nowrap;
 box-shadow:0 0 0 1px {ring}, inset 0 1px 0 {hi}, inset 0 -1px 0 rgba(255,255,255,.06), 0 6px 16px -4px {shadow}}}
.b svg{{display:block;opacity:.85}}
</style><span class=b id=b>{label}{icon}</span>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(device_scale_factor=3, viewport={"width": 600, "height": 200})
        pg = ctx.new_page()
        for key, (label, kind, icon) in BUTTONS.items():
            for th in THEMES:
                pg.set_content(page(label, kind, icon, th))
                pg.wait_for_timeout(60)
                pg.locator("body").screenshot(path=str(OUT / f"{key}_{th}.png"), omit_background=True)
        browser.close()
    print(f"wrote {len(BUTTONS) * len(THEMES)} images to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
