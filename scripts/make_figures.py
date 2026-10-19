#!/usr/bin/env python3
"""Render the README figures (EN/FR x light/dark) from results/metrics.json.

    python scripts/make_figures.py

Output: results/figures/readme/<name>_<lang>_<theme>.png
Used by README.md / README.fr.md through <picture> tags, so GitHub shows the variant that matches the reader's theme.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
M = json.loads((ROOT / "results" / "metrics.json").read_text())
OUT = ROOT / "results" / "figures" / "readme"
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "light": dict(bg="#ffffff", ink="#1f2328", ink2="#59636e", grid="#e6e8eb", axis="#c3c2b7",
                  blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", base="#898781", fraud="#e34948"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", ink2="#9198a1", grid="#262c36", axis="#3d444d",
                 blue="#3987e5", orange="#d95926", aqua="#199e70", base="#898781", fraud="#e66767"),
}
TXT = {
    "en": dict(models={"logreg": "Logistic Regression", "rf": "Random Forest", "xgb": "XGBoost"},
               recall="Recall (share of frauds caught)", precision="Precision (share of alerts that are real)",
               baseline="Baseline (fraud rate)", pr_title="Precision-recall curves on the test set",
               thr="Decision threshold", cost_title="Total cost on the test set", eur="Total cost (EUR)",
               no_model="No model", f1="F1-optimal", cost="Cost-based", default="Default",
               shap_title="What drives the fraud score (mean |SHAP|)", shap_x="Mean |SHAP value|", amount="amount (log)", hour="hour"),
    "fr": dict(models={"logreg": "Régression logistique", "rf": "Forêt aléatoire", "xgb": "XGBoost"},
               recall="Rappel (part des fraudes détectées)", precision="Précision (part des alertes justifiées)",
               baseline="Référence (taux de fraude)", pr_title="Courbes précision-rappel sur le jeu de test",
               thr="Seuil de décision", cost_title="Coût total sur le jeu de test", eur="Coût total (EUR)",
               no_model="Sans modèle", f1="Optimal F1", cost="Fondé sur le coût", default="Par défaut",
               shap_title="Ce qui pilote le score de fraude (|SHAP| moyen)", shap_x="Valeur SHAP absolue moyenne", amount="montant (log)", hour="heure"),
}


def style(ax, c):
    ax.set_facecolor(c["bg"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(c["axis"])
    ax.tick_params(colors=c["ink2"], labelsize=9)
    ax.grid(axis="y", color=c["grid"], lw=1)
    ax.set_axisbelow(True)


def fig_pr(lang, theme):
    c, t = THEMES[theme], TXT[lang]
    fig, ax = plt.subplots(figsize=(7.2, 4.6), facecolor=c["bg"])
    style(ax, c)
    col = {"logreg": c["blue"], "rf": c["orange"], "xgb": c["aqua"]}
    for k in ("logreg", "rf", "xgb"):
        r = np.array(M["pr_curves"][k]["recall"]); p = np.array(M["pr_curves"][k]["precision"])
        lab = f'{t["models"][k]}  ({M["test_at_0.5"][k]["pr_auc"]:.3f})'
        ax.plot(r, p, color=col[k], lw=2.8 if k == M["final"]["key"] else 1.8, label=lab)
    ax.axhline(M["prevalence_test"], color=c["base"], ls="--", lw=1.3, label=t["baseline"])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    ax.set_xlabel(t["recall"], color=c["ink2"]); ax.set_ylabel(t["precision"], color=c["ink2"])
    ax.set_title(t["pr_title"], color=c["ink"], fontsize=12, fontweight="bold", loc="left")
    leg = ax.legend(loc="lower left", frameon=False, fontsize=9)
    for tx in leg.get_texts():
        tx.set_color(c["ink"])
    fig.tight_layout()
    fig.savefig(OUT / f"pr_curves_{lang}_{theme}.png", dpi=170, facecolor=c["bg"])
    plt.close(fig)


def fig_cost(lang, theme):
    c, t = THEMES[theme], TXT[lang]
    sw, thr, fa = M["sweep"], M["final"]["thresholds"], M["final"]["fp_cost_assumption"]
    g = np.array(sw["grid"]); tst = sw["test"]
    cost = np.array(tst["missed"]) + fa * np.array(tst["fp"])
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=c["bg"])
    style(ax, c)
    ax.plot(g, cost, color=c["ink"], lw=2)
    ax.axhline(sw["fraud_amount_test"], color=c["base"], ls="--", lw=1.3)
    ax.text(0.99, sw["fraud_amount_test"] * 1.02, t["no_model"], color=c["ink2"], ha="right", va="bottom", fontsize=9)
    for k, colr in (("default", c["base"]), ("f1", c["orange"]), ("cost", c["aqua"])):
        i = int(np.argmin(np.abs(g - thr[k])))
        ax.axvline(g[i], color=colr, lw=1.4, ls=":" if k == "default" else "-")
        ax.scatter([g[i]], [cost[i]], color=colr, s=48, zorder=5, edgecolor=c["bg"], linewidth=1.5, label=f'{t[k]}  ({thr[k]:.2f})')
    ax.set_ylim(0, sw["fraud_amount_test"] * 1.3); ax.set_xlim(0, 1)
    ax.set_xlabel(t["thr"], color=c["ink2"]); ax.set_ylabel(t["eur"], color=c["ink2"])
    ax.set_title(f'{t["cost_title"]} (false alarm = {fa:.0f} EUR)' if lang == "en" else f'{t["cost_title"]} (fausse alerte = {fa:.0f} EUR)',
                 color=c["ink"], fontsize=12, fontweight="bold", loc="left")
    leg = ax.legend(loc="upper center", frameon=True, facecolor=c["bg"], edgecolor=c["bg"], framealpha=1, fontsize=9, ncol=3)
    for tx in leg.get_texts():
        tx.set_color(c["ink"])
    fig.tight_layout()
    fig.savefig(OUT / f"threshold_cost_{lang}_{theme}.png", dpi=170, facecolor=c["bg"])
    plt.close(fig)


def fig_shap(lang, theme):
    c, t = THEMES[theme], TXT[lang]
    items = M["importance"]["shap"][:10][::-1]
    names = [t["amount"] if i["feature"] == "log_amount" else t["hour"] if i["feature"] == "hour" else i["feature"] for i in items]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), facecolor=c["bg"])
    style(ax, c)
    ax.grid(axis="y", visible=False); ax.grid(axis="x", color=c["grid"], lw=1)
    col = {"logreg": c["blue"], "rf": c["orange"], "xgb": c["aqua"]}[M["final"]["key"]]
    ax.barh(names, [i["value"] for i in items], color=col, height=0.62)
    for y, i in enumerate(items):
        ax.text(i["value"] + 0.02 * max(v["value"] for v in items), y, f'{i["value"]:.2f}', va="center", color=c["ink"], fontsize=9)
    ax.set_xlabel(t["shap_x"], color=c["ink2"])
    ax.set_title(t["shap_title"], color=c["ink"], fontsize=12, fontweight="bold", loc="left")
    fig.tight_layout()
    fig.savefig(OUT / f"shap_{lang}_{theme}.png", dpi=170, facecolor=c["bg"])
    plt.close(fig)


if __name__ == "__main__":
    for lg in ("en", "fr"):
        for th in ("light", "dark"):
            fig_pr(lg, th); fig_cost(lg, th); fig_shap(lg, th)
    print("figures written to", OUT.relative_to(ROOT))
