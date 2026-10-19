#!/usr/bin/env python3
"""Build the bilingual (EN / FR) web report from results/metrics.json.

    python scripts/build_site.py

Outputs two self-contained pages (no build step needed on GitHub Pages):
    docs/index.html     English
    docs/fr/index.html  French
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site"))
from i18n import STRINGS  # noqa: E402

REPO_URL = "https://github.com/AishwaryaMarkandu/credit-card-fraud-detection"
M = json.loads((ROOT / "results" / "metrics.json").read_text())


# ---------- locale-aware number formatting ----------
def ffloat(x, d, lang):
    s = f"{x:,.{d}f}"
    if lang == "fr":
        s = s.replace(",", " ").replace(".", ",")
    return s


def fint(n, lang):
    return ffloat(round(n), 0, lang)


def fpct(x, d, lang):
    return ffloat(x * 100, d, lang) + (" %" if lang == "fr" else "%")


def feur(x, d, lang):
    return (ffloat(x, d, lang) + " €") if lang == "fr" else "€" + ffloat(x, d, lang)


def fr_typo(s):
    s = re.sub(r" ([:;!?»])", " \\1", s)
    return s.replace("« ", "« ")


class SafeDict(dict):
    def __missing__(self, k):
        return "{" + k + "}"


def build_values(lang, L):
    d, sp, T = M["data"], M["split"], M["test_at_0.5"]
    fin = M["final"]
    key = fin["key"]
    names = L["js_models"]
    ops = fin["operating_points"]
    eda = M["eda"]
    hourly = sorted(eda["hourly"], key=lambda r: -r["rate_per_10k"])
    corr = eda["corr"]
    top_feats = [c["feature"] for c in corr[:4]]
    join_and = " et " if lang == "fr" else " and "
    ranked = sorted(["logreg", "rf", "xgb"], key=lambda k: -T[k]["pr_auc"])
    top, second = ranked[0], ranked[1]
    overlap = T[top]["pr_auc_ci"][0] <= T[second]["pr_auc_ci"][1]
    imp_type = M["importance"]["native_type"]
    if lang == "fr":
        imp_type = {"gain": "gain", "mean decrease in impurity": "baisse moyenne d'impureté"}.get(imp_type, imp_type)
    v = dict(
        lang=lang, one_in=fint(d["one_in"], lang), rows_clean=fint(d["rows_clean"], lang), fraud_n=fint(d["fraud_clean"], lang),
        dups=fint(d["duplicates"], lang), hours_span=fint(d["hours_span"], lang), n_features=sp["n_features"],
        fraud_rate_pct=fpct(d["fraud_rate"], 2, lang), baseline_acc_pct=fpct(1 - d["fraud_rate"], 2, lang),
        model_acc_pct=fpct(T[key]["accuracy"], 2, lang), model_recall_pct=fpct(T[key]["recall"], 0, lang),
        final_name=names[key], n_train=fint(sp["n_train"], lang), fraud_train=fint(sp["fraud_train"], lang),
        fraud_test=fint(sp["fraud_test"], lang), test_fraud_amt=feur(fin["test_fraud_amount"], 0, lang),
        med_fraud=feur(eda["amount_stats"]["fraud"]["median"], 2, lang), med_legit=feur(eda["amount_stats"]["legit"]["median"], 2, lang),
        le1_fraud=fpct(eda["amount_stats"]["fraud"]["share_le_1"], 0, lang), le1_legit=fpct(eda["amount_stats"]["legit"]["share_le_1"], 0, lang),
        rate1=ffloat(hourly[0]["rate_per_10k"], 0, lang), hour1=hourly[0]["hour"], rate2=ffloat(hourly[1]["rate_per_10k"], 0, lang), hour2=hourly[1]["hour"],
        avg_rate=ffloat(d["fraud_rate"] * 1e4, 1, lang),
        top_feats=", ".join(top_feats[:-1]) + join_and + top_feats[-1], max_r=ffloat(max(abs(c["r"]) for c in corr), 2, lang),
        pr_final=ffloat(T[key]["pr_auc"], 3, lang), pr_rf=ffloat(T["rf"]["pr_auc"], 3, lang), pr_lr=ffloat(T["logreg"]["pr_auc"], 3, lang),
        pr_xgb=ffloat(T["xgb"]["pr_auc"], 3, lang),
        ci_final=f"{ffloat(T[key]['pr_auc_ci'][0], 3, lang)}–{ffloat(T[key]['pr_auc_ci'][1], 3, lang)}",
        prevalence_pct=fpct(M["prevalence_test"], 2, lang),
        fa_cost=fint(fin["fp_cost_assumption"], lang), sample_frauds=M["importance"]["sample"]["frauds"],
        sample_legit=M["importance"]["sample"]["legit"], imp_type=imp_type,
    )
    sens = {r["fa_cost"]: r for r in M["cost_sensitivity"]}
    s1 = sens[1]
    dtest = ops["default"]
    xp = M["tuning"]["xgb"]["best_params"].get("scale_pos_weight")
    v.update(
        sens1_thr=ffloat(s1["threshold"], 3, lang), sens1_tp=s1["frauds_caught"], sens1_fp=fint(s1["false_alarms"], lang),
        def_tp=dtest["tp"], def_fp=fint(dtest["fp"], lang),
        spw_best=fint(xp, lang) if xp is not None else "–", spw_full=fint(M["split"]["neg_per_pos"], lang),
    )
    cop = ops["cost"]
    cut = 1 - cop["total_cost"] / fin["test_fraud_amount"]
    v.update(
        n_test=fint(sp["n_test"], lang), cost_tp=cop["tp"], cost_fp=fint(cop["fp"], lang),
        cost_fa_word=L["js_fa_one"] if cop["fp"] == 1 else L["js_fa_many"],
        cost_recall_pct=fpct(cop["recall"], 0, lang), loss_none=feur(fin["test_fraud_amount"], 0, lang),
        loss_model=feur(cop["total_cost"], 0, lang), loss_cut_pct=fpct(cut, 0, lang),
        fa_cost_eur=feur(fin["fp_cost_assumption"], 0, lang), _cut=cut,
    )
    v["overlap_note"] = L["overlap_yes" if overlap else "overlap_no"].format_map(SafeDict(v))
    v["_top"], v["_overlap"] = top, overlap
    return v, ops


def cmp_table(lang, L, v):
    T, key = M["test_at_0.5"], M["final"]["key"]
    b, m = T["baseline"], T[key]
    rows = [
        (L["cmp_acc"], fpct(b["accuracy"], 2, lang), fpct(m["accuracy"], 2, lang)),
        (L["cmp_recall"], fpct(b["recall"], 0, lang), fpct(m["recall"], 0, lang)),
        (L["cmp_prec"], "–", fpct(m["precision"], 0, lang)),
        (L["cmp_pr"], ffloat(b["pr_auc"], 4, lang), ffloat(m["pr_auc"], 3, lang)),
    ]
    head = f'<tr><th>{L["cmp_metric"]}</th><th>{L["cmp_baseline"]}</th><th>{L["cmp_model"].format_map(SafeDict(v))}</th></tr>'
    body = "".join(f"<tr><td>{a}</td><td>{x}</td><td><b>{y}</b></td></tr>" for a, x, y in rows)
    return f'<div class="tw"><table><thead>{head}</thead><tbody>{body}</tbody></table></div>'


def models_table(lang, L):
    cv, tun, T = M["cv_default"], M["tuning"], M["test_at_0.5"]
    key = M["final"]["key"]
    colors = {"baseline": "base", "logreg": "blue", "rf": "orange", "xgb": "aqua"}
    names = dict(L["js_models"], baseline=L["cmp_baseline"])
    rows = []
    for k in ["baseline", "logreg", "rf", "xgb"]:
        c = cv[k]
        dd = 4 if k == "baseline" else 3
        cvd = f'{ffloat(c["pr_auc_mean"], dd, lang)} <small>± {ffloat(c["pr_auc_std"], dd, lang)}</small>'
        cvt = ffloat(tun[k]["best_cv_pr_auc"], 3, lang) if k in tun else "–"
        lo, hi = T[k]["pr_auc_ci"]
        te = ffloat(T[k]["pr_auc"], dd, lang) + (f' <small>[{ffloat(lo, 3, lang)}–{ffloat(hi, 3, lang)}]</small>' if k != "baseline" else "")
        badge = f'<span class="badge">{L["tbl_chosen"]}</span>' if k == key else ""
        rows.append(f'<tr class="{"hl" if k == key else ""}"><td><span class="dot bg-{colors[k]}"></span>{names[k]}{badge}</td><td>{cvd}</td><td>{cvt}</td><td>{te}</td></tr>')
    head = f'<tr><th>{L["tbl_model"]}</th><th>{L["tbl_cv_default"]}</th><th>{L["tbl_cv_tuned"]}</th><th>{L["tbl_test"]}</th></tr>'
    return f'<div class="tw"><table class="wide"><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'


def params_html(lang, L):
    def fmt(x):
        return ffloat(x, 4, lang).rstrip("0").rstrip(",.") if isinstance(x, float) else str(x)
    names = L["js_models"]
    rows = []
    for k, t in M["tuning"].items():
        ps = ", ".join(f"{p}={fmt(x)}" for p, x in t["best_params"].items())
        rows.append(f"<tr><td>{names[k]}</td><td>{ps}</td></tr>")
    return f'<div class="tw"><table><tbody>{"".join(rows)}</tbody></table></div>'


def render(lang):
    L0 = STRINGS[lang]
    v, ops = build_values(lang, L0)
    fmtd = {}
    for k, s in L0.items():
        if isinstance(s, str):
            s = s.format_map(SafeDict(v))
            if lang == "fr":
                s = fr_typo(s)
        fmtd[k] = s
    if lang == "fr":  # model-name / case dicts are passed as-is
        pass
    fin = M["final"]
    cost_op = ops["cost"]
    page = dict(
        lang=lang, one_in=M["data"]["one_in"], fa_cost=int(fin["fp_cost_assumption"]),
    )
    tokens = dict(fmtd)
    tokens.update(
        lang=lang, other_lang="fr" if lang == "en" else "en",
        href_other="fr/" if lang == "en" else "../", href_en="./" if lang == "en" else "../", href_fr="fr/" if lang == "en" else "./",
        repo_url=REPO_URL, fa_cost=str(page["fa_cost"]),
        kpi_tx=fint(M["data"]["rows_clean"], lang), kpi_fraud=fint(M["data"]["fraud_clean"], lang),
        kpi_recall=fpct(cost_op["recall"], 0, lang), kpi_cut=fpct(v["_cut"], 0, lang),
        cmp_table=cmp_table(lang, L0, v), models_table=models_table(lang, L0), params_html=params_html(lang, L0),
        css=(ROOT / "site" / "style.css").read_text(), js=(ROOT / "site" / "app.js").read_text(),
        data_json=json.dumps(M, separators=(",", ":")).replace("</", "<\\/"),
        i18n_json=json.dumps(fmtd, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"),
        page_json=json.dumps(page),
    )
    tpl = (ROOT / "site" / "template.html").read_text()

    def sub(m):
        k = m.group(1)
        if k not in tokens:
            raise KeyError(f"template token [[{k}]] has no value")
        return str(tokens[k])

    html = re.sub(r"\[\[(\w+)\]\]", sub, tpl)
    out = ROOT / "docs" / ("index.html" if lang == "en" else "fr/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(html) / 1024:.0f} KB)  [best test PR-AUC: {v['_top']}, CIs overlap: {v['_overlap']}]")


if __name__ == "__main__":
    for lg in ("en", "fr"):
        render(lg)
    (ROOT / "docs" / ".nojekyll").write_text("")
