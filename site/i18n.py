# -*- coding: utf-8 -*-
"""All user-facing strings of the web report, in English and French.

The page is written for decision-makers first: plain wording up front, technical terms
kept in short notes ("For specialists"), in brackets, or in the glossary.

Strings may contain {placeholders} (filled by build_site.py with locale-formatted numbers)
and a little inline HTML (<b>, <code>). Keys starting with "js_" are also exposed to the charts.
"""

EN = {
    # --- meta / chrome
    "html_title": "Credit Card Fraud Detection · Analysis",
    "meta_desc": "How well can a model spot credit card fraud when only 1 payment in 600 is fraudulent? "
                 "A plain-language analysis with the figures, the trade-offs and the decision it leaves to management. "
                 "Interactive, bilingual, light and dark.",
    "skip": "Skip to content",
    "nav_summary": "Summary", "nav_problem": "Problem", "nav_eda": "Data", "nav_models": "Models", "nav_threshold": "Alert level",
    "nav_explain": "Explanations", "nav_takeaways": "Takeaways",
    "lang_other_label": "Français", "lang_other_short": "FR", "lang_this_short": "EN",
    "theme_toggle": "Toggle light / dark theme",
    "lang_switch": "Switch to French",
    "github": "View on GitHub",
    "brand": "Fraud Detection",

    # --- hero
    "hero_eyebrow": "Case study · Card fraud detection",
    "hero_h1": "Catching the 1 in {one_in}",
    "hero_lead": "Out of {one_in} card payments, only one is a fraud. This study shows how well a model can find it, "
                 "what it costs in false alarms, and which decision it leaves to management.",
    "cta_read": "Read the analysis",
    "stat_tx": "card payments analysed",
    "stat_fraud": "frauds, i.e. {fraud_rate_pct} of payments",
    "stat_recall": "of frauds caught, on {n_test} payments the model had never seen",
    "stat_cut": "of fraud losses avoided, assuming {fa_cost_eur} per false alarm",
    "waffle_caption": "Each dot is a payment: {one_in} dots, one fraud.",
    "waffle_alt": "A grid of {one_in} dots with a single red dot representing one fraudulent payment",

    # --- summary
    "sum_h": "The short version",
    "sum1_k": "The problem", "sum1_t": "A needle in a haystack",
    "sum1_p": "Out of {one_in} card payments, one is a fraud. A check that let everything through would be right {baseline_acc_pct} of the time "
              "and would stop no fraud at all.",
    "sum2_k": "The result", "sum2_t": "Most frauds caught, very few false alarms",
    "sum2_p": "The model gives each payment a risk score. On {n_test} payments it had never seen, it catches {cost_tp} of {fraud_test} frauds "
              "({cost_recall_pct}) with only {cost_fp} {cost_fa_word}. Fraud losses fall from {loss_none} to {loss_model}, which is {loss_cut_pct} less.",
    "sum3_k": "The decision", "sum3_t": "How many alerts are you willing to handle?",
    "sum3_p": "Where to set the alert level is a management choice, not a technical one. If a false alarm costs you {fa_cost_eur}, the standard setting is enough. "
              "If it costs only €1, a more sensitive setting pays off: {sens1_tp} frauds caught instead of {def_tp}, at the price of {sens1_fp} false alarms instead of {def_fp}.",
    "sum_caveat_t": "Keep in mind:",
    "sum_caveat": "these results come from a public dataset of two days of card payments, with only {fraud_test} frauds in the test. "
                  "It is a demonstration of method, not a promise of performance. Before any roll-out, the analysis should be repeated on your own data, "
                  "with your real costs, and checked over time.",

    # --- problem
    "problem_h": "Why “{baseline_acc_pct} correct” proves nothing",
    "problem_p": "Out of {rows_clean} payments, only {fraud_n} are frauds. A system that approved every payment would be "
                 "right {baseline_acc_pct} of the time and would stop <b>none</b> of the fraud. So the share of correct answers is a poor yardstick here. "
                 "Two concrete questions matter instead: how many frauds do we catch, and how many of our alerts are justified?",
    "problem_tech": "Accuracy is replaced by recall, precision and PR-AUC (area under the precision–recall curve), the right family of metrics for rare events. "
                    "The decision threshold is treated as a business choice rather than a default of 0.5.",
    "tech_label": "For specialists",
    "cmp_h": "Same test, two verdicts",
    "cmp_metric": "Measure", "cmp_baseline": "Approve everything", "cmp_model": "{final_name} model",
    "cmp_acc": "Share of correct answers", "cmp_recall": "Frauds caught", "cmp_prec": "Alerts that are justified",
    "cmp_pr": "Overall quality score, 0 to 1 (PR-AUC)",
    "cmp_note": "The share of correct answers barely moves ({baseline_acc_pct} vs {model_acc_pct}), while the share of frauds caught goes from 0 to {model_recall_pct}.",

    # --- workflow
    "flow_h": "How the study was done",
    "flow1_t": "Clean", "flow1_p": "Check for gaps and remove {dups} exact duplicates, so the model is never tested on a payment it has already seen.",
    "flow2_t": "Explore", "flow2_p": "Look at when, at what amounts and with which characteristics fraud differs from normal payments.",
    "flow3_t": "Prepare", "flow3_p": "Prepare the amount and the time of day, and set aside 20% of payments that the model never sees, to grade it fairly at the end.",
    "flow4_t": "Compare", "flow4_p": "Put four approaches in competition, from the simplest to the most powerful, on the same data and under the same rules.",
    "flow5_t": "Measure", "flow5_p": "Count frauds caught, false alarms and total cost, then explain why the model decides what it decides.",

    # --- EDA
    "eda_h": "What the data shows",
    "eda_intro": "{rows_clean} payments over about {hours_span} hours. Each payment is described by {n_features} pieces of information: "
                 "28 are anonymised by the bank to protect customers, plus the amount and the time of day. Nothing is missing.",
    "eda1_h": "Fraud hides in small amounts",
    "eda1_p": "The typical fraud is {med_fraud}, against {med_legit} for a normal payment, and {le1_fraud} of frauds are "
              "€1 or less (versus {le1_legit} of normal payments). That looks like thieves testing a stolen card, though the data cannot confirm it. "
              "Either way, the amount alone cannot tell the two apart.",
    "eda1_chart": "Spread of amounts (log scale: small amounts are stretched so they can be read)",
    "eda2_h": "Fraud peaks in the small hours",
    "eda2_p": "Around hour {hour1} there are {rate1} frauds per 10,000 payments, and {rate2} around hour {hour2}, "
              "against {avg_rate} on average. Caution: the data gives time elapsed since the start, not a clock time, so the hour of day is an approximation, "
              "and {fraud_n} frauds over two days is a small sample.",
    "eda2_chart_a": "Share of all payments, by hour", "eda2_chart_b": "Frauds per 10,000 payments, by hour",
    "eda3_h": "A few anonymised signals carry most of the information",
    "eda3_p": "Each bar shows how strongly a piece of information is linked to fraud (its correlation). {top_feats} stand out, yet none reaches "
              "{max_r} (out of 1): no single signal is enough, which is why a model that combines them is needed.",
    "eda3_chart": "Link with fraud (top 12)",
    "eda4_h": "Frauds stand apart, but not cleanly",
    "eda4_p": "On the four signals most linked to fraud, frauds sit in a different zone from normal payments, "
              "but the two groups partly overlap. That is where models able to spot combinations have an edge.",
    "eda4_chart": "Spread of the four signals most linked to fraud",

    # --- models
    "models_h": "Four approaches, one fair test",
    "models_p": "Each approach learns from the same {n_train} payments ({fraud_train} frauds), then is graded on {n_test} payments it has never seen ({fraud_test} frauds). "
                "The final model was chosen before that test, never on it, so the grade is honest. The approaches range from logistic regression (the simplest) "
                "to random forest and XGBoost (more powerful, built from many small decision trees). Each is graded with the same score, "
                "from 0 to 1 (higher is better).",
    "models_tech": "Score = PR-AUC. Models are compared by 5-fold stratified cross-validation, then tuned with a randomized search (3-fold) on PR-AUC. "
                   "Class weighting is used to handle the imbalance, and the intervals are 95% bootstrap intervals (300 resamples) on the test PR-AUC.",
    "tbl_model": "Approach", "tbl_cv_default": "Average grade in training<br><small>standard settings</small>",
    "tbl_cv_tuned": "Average grade in training<br><small>after fine-tuning</small>", "tbl_test": "Final grade on the test<br><small>95% range</small>",
    "tbl_chosen": "chosen",
    "models_tbl_h": "Grades by approach",
    "pr_h": "Which model finds frauds best?",
    "pr_p": "{final_name} gets the best grade: <b>{pr_final}</b> out of 1 (95% range {ci_final}), against {pr_rf} for the random forest and "
            "{pr_lr} for logistic regression. Each curve shows the trade-off: the more frauds we want to catch (horizontal axis), the lower the share of justified alerts (vertical axis). "
            "The dashed line is pure chance ({prevalence_pct}). {overlap_note}",
    "overlap_yes": "With only {fraud_test} frauds in the test, the ranges of the top two models overlap: the gap between them is not proven and should be read with caution.",
    "overlap_no": "The range of the top model does not overlap with the runner-up.",
    "params_h": "Technical settings kept",
    "params_p": "For the curious: XGBoost also tested how much extra weight to give frauds while learning. The search kept a factor of {spw_best} (<code>scale_pos_weight</code>), far below full rebalancing (about {spw_full}). Winning settings below.",

    # --- threshold
    "thr_h": "How many alerts to accept? A management decision",
    "thr_p": "The model gives each payment a risk score between 0 and 1. You then choose the score from which an alert is raised: this is the “threshold”. "
             "A low threshold catches more frauds but raises more false alarms (honest customers disturbed, analysts kept busy); a high threshold does the opposite. "
             "Move the slider to see the best choice for what a false alarm costs you. Every figure is measured on payments the model has never seen.",
    "thr_tech": "Thresholds are always chosen on out-of-fold predictions of the training set, then applied once to the untouched test set. "
                "Three options are compared: the default 0.5, the F1-optimal threshold, and the cost-optimal threshold.",
    "thr_assump": "Assumptions: a fraud that goes undetected costs the payment amount; a false alarm costs a flat fee (analysis time, customer annoyance). "
                  "{fa_cost_eur} is a starting value I chose, not a measurement: replace it with your real costs.",
    "thr_slider": "Cost of one false alarm",
    "thr_chart_h": "Total cost (undetected frauds + false alarms), by threshold",
    "thr_live": "At <b>{c}</b> per false alarm, the best threshold is <b>{t}</b>: it catches <b>{tp}</b> of {fraud_test} frauds "
                "with <b>{fp}</b> {fa_word}. Total cost: <b>{cost}</b>, against {nomodel} with no model.",
    "op_default": "Standard", "op_f1": "Balanced (F1)", "op_cost": "Lowest cost",
    "op_threshold": "Threshold", "op_caught": "Frauds caught", "op_fp": "False alarms", "op_alerts": "Alerts per 100,000 payments",
    "op_missed": "Undetected frauds (amount lost)", "op_total": "Total cost", "op_best": "Cheapest",
    "cm_legit": "Normal", "cm_fraud": "Fraud", "cm_pred": "Predicted", "cm_actual": "Actual",
    "cm_hint": "How to read the small tables: columns are what the model announces, rows are reality. Bottom right: frauds caught. Top right: false alarms. Bottom left: frauds missed.",
    "thr_same": "At this cost the three settings make exactly the same decisions on the test: the model separates the two groups well enough that a wide range of thresholds gives the same result. Slide towards €1 to see when the choice starts to matter.",
    "thr_caveat": "The test holds only {fraud_test} frauds ({test_fraud_amt} in total), so these figures would change noticeably with another split. "
                  "They illustrate the trade-off, they do not guarantee future performance.",

    # --- explainability
    "xai_h": "Why the model raises an alert",
    "xai_p": "A model that blocks payments must be able to justify itself. Two views: the <b>weight of each piece of information</b> (what the model relies on most) "
             "and a method called <b>SHAP</b>, which measures, for each payment, how much every piece of information raised or lowered the risk score. "
             "Computed on a test sample ({sample_frauds} frauds plus {sample_legit} normal payments drawn at random).",
    "imp_native": "What the model relies on most (measure: {imp_type})", "imp_shap": "Average influence on the score (SHAP)",
    "bee_h": "In which direction each signal pushes the score",
    "bee_p": "Each dot is a payment. Right: the score moves towards fraud. Left: it moves away. Colour tells whether the signal's value is low or high.",
    "bee_x": "Effect on the score (towards fraud →)", "bee_low": "low", "bee_high": "high", "bee_value": "value of the signal",
    "cases_h": "Why was this payment flagged (or missed)?",
    "cases_p": "Three individual decisions. Bars show the six signals that weigh most: red pushes towards fraud, blue towards a normal payment.",
    "case_true_positive": "A typical fraud, correctly caught", "case_false_alarm": "The most confident false alarm", "case_missed_fraud": "The missed fraud that came closest to being caught",
    "case_score": "risk score", "case_amount": "amount", "case_hour": "hour",
    "xai_caveat": "Signals <code>V1</code> to <code>V28</code> are anonymised (the public dataset hides their meaning to protect customers): we know <i>which</i> one weighed, not <i>what it stands for</i>. "
                  "In a company, the same analysis would run on named information (country, type of merchant, usual amount…), which makes a decision explainable to a customer or an auditor.",

    # --- takeaways
    "take_h": "Key takeaways",
    "take1_t": "The share of correct answers is misleading", "take1_p": "Approving everything scores {baseline_acc_pct} and catches no fraud. What counts is the share of frauds caught and the share of justified alerts.",
    "take2_t": "Tree-based models spot more", "take2_p": "Random forest and XGBoost reach {pr_rf} and {pr_xgb}, against {pr_lr} for logistic regression (the simplest): fraud follows complex patterns, not one simple dividing line.",
    "take3_t": "The alert level is a management decision", "take3_p": "At €1 per false alarm the best threshold drops to {sens1_thr}: {sens1_tp} frauds caught instead of {def_tp}, but {sens1_fp} false alarms instead of {def_fp}. From about {fa_cost_eur} upwards the result changes little from one threshold to the next. The right setting depends on what a false alarm and a missed fraud really cost you.",
    "take4_t": "A decision must be explainable", "take4_p": "When a model blocks a real customer's payment, being able to say why is part of the product.",
    "next_h": "Limits and next steps",
    "next1_t": "Test over time", "next1_p": "Here, learning and testing both draw from the same two days, which is optimistic. In production the model learns from the past and must predict the future: that is what to simulate next (time-based validation).",
    "next2_t": "Try other rebalancing methods", "next2_p": "Here frauds are given more weight while learning. It could be compared with creating artificial frauds (SMOTE).",
    "next3_t": "Make scores easier to read", "next3_p": "Calibrate the model so that a score of 0.8 really means “about 8 frauds out of 10”, which makes it easier to keep a stable threshold over time.",
    "next4_t": "More frauds to validate", "next4_p": "Only {fraud_test} frauds in the test: treat the results as an order of magnitude. More data, or repeated splits, would narrow the ranges.",

    # --- glossary
    "gl_h": "Plain-language glossary",
    "gl_intro": "The technical terms used in this report, in everyday words.",
    "gl1_t": "False alarm (false positive)", "gl1_p": "A normal payment flagged as fraud. Cost: analyst time and an annoyed customer.",
    "gl2_t": "Undetected fraud (false negative)", "gl2_p": "A fraud that goes through. Cost: the amount of the payment.",
    "gl3_t": "Frauds caught (recall)", "gl3_p": "Out of all real frauds, the share the model flags.",
    "gl4_t": "Justified alerts (precision)", "gl4_p": "Out of all alerts raised, the share that are real frauds.",
    "gl5_t": "Threshold", "gl5_p": "The risk score from which an alert is raised. Lower means more alerts, higher means fewer.",
    "gl6_t": "Overall quality score (PR-AUC)", "gl6_p": "A grade from 0 to 1 that sums up the trade-off between frauds caught and justified alerts. Better suited than “share of correct answers” when fraud is rare.",
    "gl7_t": "Cross-validation", "gl7_p": "Learning and grading several times on different slices of the training data, to check that a result is not a coincidence.",
    "gl8_t": "95% range", "gl8_p": "The zone in which the true grade very likely lies. A wide range means few cases, so more uncertainty.",
    "gl9_t": "SHAP", "gl9_p": "A method that tells, for one payment, how much each piece of information raised or lowered the risk score.",
    "gl10_t": "Anonymised data (PCA)", "gl10_p": "The 28 signals V1 to V28 are mathematical combinations of the original data, scrambled to protect customers.",
    "gl11_t": "Class imbalance", "gl11_p": "When one case is far rarer than the other (here 1 fraud in 600). It makes naive measures misleading.",
    "gl12_t": "Settings (hyperparameters)", "gl12_p": "Adjustments made before learning, such as how deep the decision trees can go. They are tuned by trial and error.",

    # --- run it
    "run_h": "Reproduce the analysis",
    "run_p": "For technical readers: the notebook reads <code>data/creditcard.csv</code> if present and otherwise downloads the dataset with <code>kagglehub</code>.",
    "copy": "Copy", "copied": "Copied",
    "stack_h": "Tools used",
    "footer_data": "Dataset: Credit Card Fraud Detection, ULB Machine Learning Group, published on Kaggle. Check its page for licence terms.",
    "footer_by": "Built by",
    "noscript": "This report draws its charts with JavaScript. The code and results are available in the GitHub repository.",
    "table_view": "View as table",

    # --- chart strings
    "js_legit": "Normal", "js_fraud": "Fraud", "js_share_class": "Share of the group",
    "js_hour": "hour", "js_rate": "per 10,000", "js_share_tx": "of payments",
    "js_recall": "Frauds caught (recall)", "js_precision": "Alerts that are justified (precision)",
    "js_baseline": "Reference", "js_threshold": "Alert threshold", "js_cost_eur": "Total cost (€)", "js_no_model": "No model",
    "js_alerts": "alerts", "js_caught": "caught", "js_fa": "false alarms", "js_cost": "cost",
    "js_f1_marker": "F1", "js_cost_marker": "lowest cost", "js_default_marker": "0.5",
    "js_pct_range": "range", "js_corr": "link with fraud", "js_shap_axis": "Effect on the score",
    "js_pushes_fraud": "pushes towards fraud", "js_pushes_legit": "pushes towards normal",
    "js_true_class": "reality", "js_percentile": "value of the signal (from low to high)",
    "js_tbl_feature": "Signal", "js_tbl_value": "Value", "js_tbl_hour": "Hour", "js_tbl_tx": "Payments", "js_tbl_fraud": "Frauds",
    "js_tbl_rate": "Frauds per 10k", "js_tbl_bin": "Amount range", "js_tbl_legit": "Share of normal", "js_tbl_fraudshare": "Share of fraud",
    "js_tbl_model": "Approach", "js_tbl_recall": "Frauds caught", "js_tbl_prec": "Justified alerts", "js_tbl_t": "Threshold", "js_tbl_tp": "Caught",
    "js_tbl_fp": "False alarms", "js_tbl_cost": "Total cost",
    "js_models": {"logreg": "Logistic Regression", "rf": "Random Forest", "xgb": "XGBoost"},
    "js_cases": {"true_positive": "A typical fraud, correctly caught", "false_alarm": "The most confident false alarm", "missed_fraud": "The missed fraud that came closest to being caught"},
    "js_amount_log": "amount",
    "js_fa_one": "false alarm", "js_fa_many": "false alarms", "js_neg_corr": "lower when fraud", "js_pos_corr": "higher when fraud",
}

FR = {
    "html_title": "Détection de fraude à la carte bancaire · Analyse",
    "meta_desc": "Dans quelle mesure un modèle sait-il repérer la fraude à la carte quand un seul paiement sur 600 est frauduleux ? "
                 "Une analyse en langage simple, avec les chiffres, les compromis et la décision qu'elle laisse à la direction. "
                 "Interactive, bilingue, mode clair et sombre.",
    "skip": "Aller au contenu",
    "nav_summary": "Essentiel", "nav_problem": "Problème", "nav_eda": "Données", "nav_models": "Modèles", "nav_threshold": "Réglage",
    "nav_explain": "Explications", "nav_takeaways": "Conclusions",
    "lang_other_label": "English", "lang_other_short": "EN", "lang_this_short": "FR",
    "theme_toggle": "Basculer entre thème clair et sombre",
    "lang_switch": "Passer en anglais",
    "github": "Voir sur GitHub",
    "brand": "Détection de fraude",

    "hero_eyebrow": "Étude de cas · Fraude à la carte bancaire",
    "hero_h1": "Repérer 1 transaction sur {one_in}",
    "hero_lead": "Sur {one_in} paiements par carte, un seul est une fraude. Cette étude montre dans quelle mesure un modèle sait le retrouver, "
                 "ce que cela coûte en fausses alertes, et quelle décision elle laisse à la direction.",
    "cta_read": "Lire l'analyse",
    "stat_tx": "paiements par carte analysés",
    "stat_fraud": "fraudes, soit {fraud_rate_pct} des paiements",
    "stat_recall": "des fraudes détectées, sur {n_test} paiements que le modèle n'avait jamais vus",
    "stat_cut": "de pertes évitées, en supposant {fa_cost_eur} par fausse alerte",
    "waffle_caption": "Chaque point est un paiement : {one_in} points, une seule fraude.",
    "waffle_alt": "Une grille de {one_in} points dont un seul point rouge représente un paiement frauduleux",

    "sum_h": "L'essentiel en une minute",
    "sum1_k": "Le problème", "sum1_t": "Une aiguille dans une botte de foin",
    "sum1_p": "Sur {one_in} paiements par carte, un seul est une fraude. Un contrôle qui laisserait tout passer aurait raison {baseline_acc_pct} du temps "
              "sans arrêter la moindre fraude.",
    "sum2_k": "Le résultat", "sum2_t": "La plupart des fraudes détectées, très peu de fausses alertes",
    "sum2_p": "Le modèle donne à chaque paiement un score de risque. Sur {n_test} paiements qu'il n'avait jamais vus, il détecte {cost_tp} des {fraud_test} fraudes "
              "({cost_recall_pct}) en ne déclenchant que {cost_fp} {cost_fa_word}. Les pertes liées à la fraude passent de {loss_none} à {loss_model}, soit {loss_cut_pct} de moins.",
    "sum3_k": "La décision", "sum3_t": "Combien d'alertes êtes-vous prêt à traiter ?",
    "sum3_p": "Le niveau de l'alerte est un choix de gestion, pas un choix technique. Si une fausse alerte vous coûte {fa_cost_eur}, le réglage standard suffit. "
              "Si elle ne coûte que 1 €, un réglage plus sensible devient rentable : {sens1_tp} fraudes détectées au lieu de {def_tp}, au prix de {sens1_fp} fausses alertes au lieu de {def_fp}.",
    "sum_caveat_t": "À garder en tête :",
    "sum_caveat": "ces résultats viennent d'un jeu de données public de deux jours de paiements par carte, avec seulement {fraud_test} fraudes dans le test. "
                  "C'est une démonstration de méthode, pas une promesse de performance. Avant tout déploiement, il faudrait refaire l'analyse sur vos propres données, "
                  "avec vos coûts réels, et la valider dans le temps.",

    "problem_h": "Pourquoi « {baseline_acc_pct} de bonnes réponses » ne prouve rien",
    "problem_p": "Sur {rows_clean} paiements, seuls {fraud_n} sont des fraudes. Un système qui accepterait tous les paiements aurait raison "
                 "dans {baseline_acc_pct} des cas et n'arrêterait <b>aucune</b> fraude. Le taux de bonnes réponses est donc un mauvais critère ici. "
                 "Deux questions concrètes comptent davantage : combien de fraudes attrape-t-on, et quelle part de nos alertes est justifiée ?",
    "problem_tech": "L'accuracy est remplacée par le rappel, la précision et la PR-AUC (aire sous la courbe précision–rappel), la bonne famille de métriques pour les événements rares. "
                    "Le seuil de décision est traité comme un choix métier plutôt que comme une valeur par défaut de 0,5.",
    "tech_label": "Pour les spécialistes",
    "cmp_h": "Même test, deux verdicts",
    "cmp_metric": "Mesure", "cmp_baseline": "Tout accepter", "cmp_model": "Modèle {final_name}",
    "cmp_acc": "Part de bonnes réponses", "cmp_recall": "Fraudes détectées", "cmp_prec": "Alertes justifiées",
    "cmp_pr": "Note globale de qualité, de 0 à 1 (PR-AUC)",
    "cmp_note": "La part de bonnes réponses bouge à peine ({baseline_acc_pct} contre {model_acc_pct}), alors que la part de fraudes détectées passe de 0 à {model_recall_pct}.",

    "flow_h": "Comment l'étude a été menée",
    "flow1_t": "Nettoyer", "flow1_p": "Vérifier qu'il ne manque rien et retirer {dups} doublons exacts, pour ne jamais tester le modèle sur un paiement qu'il a déjà vu.",
    "flow2_t": "Explorer", "flow2_p": "Regarder quand, à quels montants et avec quelles caractéristiques la fraude se distingue des paiements normaux.",
    "flow3_t": "Préparer", "flow3_p": "Préparer le montant et l'heure, et mettre de côté 20 % des paiements, jamais montrés au modèle, pour le noter équitablement à la fin.",
    "flow4_t": "Comparer", "flow4_p": "Mettre quatre approches en concurrence, de la plus simple à la plus puissante, sur les mêmes données et selon les mêmes règles.",
    "flow5_t": "Mesurer", "flow5_p": "Compter les fraudes détectées, les fausses alertes et le coût total, puis expliquer pourquoi le modèle décide ce qu'il décide.",

    "eda_h": "Ce que montrent les données",
    "eda_intro": "{rows_clean} paiements sur environ {hours_span} heures. Chaque paiement est décrit par {n_features} informations : "
                 "28 sont anonymisées par la banque pour protéger les clients, plus le montant et l'heure. Aucune donnée manquante.",
    "eda1_h": "La fraude se cache dans les petits montants",
    "eda1_p": "La fraude typique porte sur {med_fraud}, contre {med_legit} pour un paiement normal, et {le1_fraud} des fraudes sont de "
              "1 € ou moins (contre {le1_legit} des paiements normaux). Cela ressemble à des voleurs qui testent une carte volée, sans que les données puissent le confirmer. "
              "Dans tous les cas, le montant seul ne suffit pas à distinguer les deux.",
    "eda1_chart": "Répartition des montants (échelle logarithmique : les petits montants sont étirés pour être lisibles)",
    "eda2_h": "La fraude culmine au petit matin",
    "eda2_p": "Vers {hour1} h, on compte {rate1} fraudes pour 10 000 paiements, et {rate2} vers {hour2} h, "
              "contre {avg_rate} en moyenne. Prudence : les données donnent un temps écoulé depuis le début, pas une heure réelle ; l'heure de la journée est donc une approximation, "
              "et {fraud_n} fraudes sur deux jours, c'est peu.",
    "eda2_chart_a": "Part de l'ensemble des paiements, par heure", "eda2_chart_b": "Fraudes pour 10 000 paiements, par heure",
    "eda3_h": "Quelques signaux anonymisés portent l'essentiel de l'information",
    "eda3_p": "Chaque barre indique à quel point une information est liée à la fraude (sa corrélation). {top_feats} ressortent, mais aucune n'atteint "
              "{max_r} (sur 1) : aucun signal ne suffit seul, d'où l'intérêt d'un modèle qui les combine.",
    "eda3_chart": "Lien avec la fraude (top 12)",
    "eda4_h": "Les fraudes se distinguent, mais pas nettement",
    "eda4_p": "Sur les quatre signaux les plus liés à la fraude, les fraudes occupent une zone différente de celle des paiements normaux, "
              "mais les deux groupes se chevauchent en partie. C'est là que les modèles capables de repérer des combinaisons ont l'avantage.",
    "eda4_chart": "Répartition des quatre signaux les plus liés à la fraude",

    "models_h": "Quatre approches, un test équitable",
    "models_p": "Chaque approche apprend sur les mêmes {n_train} paiements ({fraud_train} fraudes), puis est notée sur {n_test} paiements qu'elle n'a jamais vus ({fraud_test} fraudes). "
                "Le modèle final a été choisi avant ce test, jamais dessus, pour que la note soit honnête. Les approches vont de la régression logistique (la plus simple) "
                "à la forêt aléatoire et XGBoost (plus puissants, construits à partir de nombreux petits arbres de décision). Toutes sont notées avec le même score, "
                "de 0 à 1 (plus c'est haut, mieux c'est).",
    "models_tech": "Score = PR-AUC. Les modèles sont comparés par validation croisée stratifiée à 5 plis, puis réglés par une recherche aléatoire (3 plis) sur la PR-AUC. "
                   "La pondération des classes gère le déséquilibre, et les intervalles sont des intervalles bootstrap à 95 % (300 rééchantillonnages) sur la PR-AUC du test.",
    "tbl_model": "Approche", "tbl_cv_default": "Note moyenne à l'entraînement<br><small>réglages standard</small>",
    "tbl_cv_tuned": "Note moyenne à l'entraînement<br><small>après réglages fins</small>", "tbl_test": "Note finale sur le test<br><small>fourchette à 95 %</small>",
    "tbl_chosen": "retenu",
    "models_tbl_h": "Notes par approche",
    "pr_h": "Quel modèle repère le mieux les fraudes ?",
    "pr_p": "{final_name} obtient la meilleure note : <b>{pr_final}</b> sur 1 (fourchette à 95 % : {ci_final}), contre {pr_rf} pour la forêt aléatoire et "
            "{pr_lr} pour la régression logistique. Chaque courbe montre le compromis : plus on veut attraper de fraudes (axe horizontal), plus la part d'alertes justifiées baisse (axe vertical). "
            "La ligne pointillée correspond au pur hasard ({prevalence_pct}). {overlap_note}",
    "overlap_yes": "Avec seulement {fraud_test} fraudes dans le test, les fourchettes des deux meilleurs modèles se chevauchent : l'écart entre eux n'est pas démontré et se lit avec prudence.",
    "overlap_no": "La fourchette du meilleur modèle ne chevauche pas celle du suivant.",
    "params_h": "Réglages techniques retenus",
    "params_p": "Pour les curieux : XGBoost a aussi testé le poids supplémentaire à donner aux fraudes pendant l'apprentissage. La recherche a retenu un facteur de {spw_best} (<code>scale_pos_weight</code>), bien en dessous d'un rééquilibrage complet (environ {spw_full}). Réglages retenus ci-dessous.",

    "thr_h": "Combien d'alertes accepter ? Une décision de gestion",
    "thr_p": "Le modèle donne à chaque paiement un score de risque entre 0 et 1. On choisit ensuite à partir de quel score une alerte est déclenchée : c'est le « seuil ». "
             "Un seuil bas attrape plus de fraudes mais crée plus de fausses alertes (clients honnêtes dérangés, analystes mobilisés) ; un seuil élevé fait l'inverse. "
             "Déplacez le curseur pour voir le meilleur choix selon ce que vous coûte une fausse alerte. Tous les chiffres sont mesurés sur des paiements que le modèle n'a jamais vus.",
    "thr_tech": "Les seuils sont toujours choisis sur les prédictions out-of-fold de l'entraînement, puis appliqués une seule fois au jeu de test, resté intact. "
                "Trois options sont comparées : le seuil par défaut 0,5, le seuil optimal pour le F1 et le seuil optimal sur le coût.",
    "thr_assump": "Hypothèses : une fraude non détectée coûte le montant du paiement ; une fausse alerte coûte un forfait (temps d'analyse, désagrément client). "
                  "{fa_cost_eur} est une valeur de départ que j'ai posée, pas une mesure : à remplacer par vos coûts réels.",
    "thr_slider": "Coût d'une fausse alerte",
    "thr_chart_h": "Coût total (fraudes non détectées + fausses alertes), selon le seuil",
    "thr_live": "À <b>{c}</b> par fausse alerte, le meilleur seuil est <b>{t}</b> : il détecte <b>{tp}</b> fraudes sur {fraud_test} "
                "avec <b>{fp}</b> {fa_word}. Coût total : <b>{cost}</b>, contre {nomodel} sans modèle.",
    "op_default": "Standard", "op_f1": "Équilibré (F1)", "op_cost": "Coût minimal",
    "op_threshold": "Seuil", "op_caught": "Fraudes détectées", "op_fp": "Fausses alertes", "op_alerts": "Alertes pour 100 000 paiements",
    "op_missed": "Fraudes non détectées (montant perdu)", "op_total": "Coût total", "op_best": "Le moins cher",
    "cm_legit": "Normal", "cm_fraud": "Fraude", "cm_pred": "Annoncé", "cm_actual": "Réel",
    "cm_hint": "Lecture des petits tableaux : les colonnes sont ce que le modèle annonce, les lignes la réalité. En bas à droite : les fraudes détectées. En haut à droite : les fausses alertes. En bas à gauche : les fraudes manquées.",
    "thr_same": "À ce coût, les trois réglages prennent exactement les mêmes décisions sur le test : le modèle sépare assez bien les deux groupes pour qu'une large plage de seuils donne le même résultat. Glissez vers 1 € pour voir quand le choix commence à compter.",
    "thr_caveat": "Le test ne contient que {fraud_test} fraudes ({test_fraud_amt} au total) : ces chiffres changeraient sensiblement avec un autre découpage. "
                  "Ils illustrent le compromis, ils ne garantissent pas une performance future.",

    "xai_h": "Pourquoi le modèle déclenche une alerte",
    "xai_p": "Un modèle qui bloque des paiements doit pouvoir se justifier. Deux angles : le <b>poids de chaque information</b> (ce sur quoi le modèle s'appuie le plus) "
             "et une méthode appelée <b>SHAP</b>, qui mesure, pour chaque paiement, de combien chaque information a fait monter ou baisser le score de risque. "
             "Calculé sur un échantillon du test ({sample_frauds} fraudes et {sample_legit} paiements normaux tirés au hasard).",
    "imp_native": "Ce sur quoi le modèle s'appuie le plus (mesure : {imp_type})", "imp_shap": "Influence moyenne sur le score (SHAP)",
    "bee_h": "Dans quel sens chaque signal pousse le score",
    "bee_p": "Chaque point est un paiement. À droite : le score monte vers la fraude. À gauche : il s'en éloigne. La couleur indique si la valeur du signal est faible ou élevée.",
    "bee_x": "Effet sur le score (vers la fraude →)", "bee_low": "faible", "bee_high": "élevée", "bee_value": "valeur du signal",
    "cases_h": "Pourquoi ce paiement a-t-il été signalé (ou manqué) ?",
    "cases_p": "Trois décisions individuelles. Les barres montrent les six signaux qui pèsent le plus : le rouge pousse vers la fraude, le bleu vers un paiement normal.",
    "case_true_positive": "Une fraude typique, bien détectée", "case_false_alarm": "La fausse alerte la plus affirmée", "case_missed_fraud": "La fraude manquée qui est passée le plus près d'être détectée",
    "case_score": "score de risque", "case_amount": "montant", "case_hour": "heure",
    "xai_caveat": "Les signaux <code>V1</code> à <code>V28</code> sont anonymisés (le jeu de données public cache leur sens pour protéger les clients) : on sait <i>lequel</i> a pesé, pas <i>ce qu'il représente</i>. "
                  "En entreprise, la même analyse porterait sur des informations nommées (pays, type de commerçant, montant habituel…), ce qui permet d'expliquer une décision à un client ou à un auditeur.",

    "take_h": "Conclusions",
    "take1_t": "La part de bonnes réponses est trompeuse", "take1_p": "Tout accepter donne {baseline_acc_pct} et n'attrape aucune fraude. Ce qui compte, c'est la part de fraudes détectées et la part d'alertes justifiées.",
    "take2_t": "Les modèles « en arbres » repèrent davantage", "take2_p": "La forêt aléatoire et XGBoost obtiennent {pr_rf} et {pr_xgb}, contre {pr_lr} pour la régression logistique (la plus simple) : la fraude suit des schémas complexes, pas une simple ligne de partage.",
    "take3_t": "Le niveau d'alerte est une décision de gestion", "take3_p": "À 1 € par fausse alerte, le meilleur seuil descend à {sens1_thr} : {sens1_tp} fraudes détectées au lieu de {def_tp}, mais {sens1_fp} fausses alertes au lieu de {def_fp}. À partir d'environ {fa_cost_eur}, le résultat change peu d'un seuil à l'autre. Le bon réglage dépend de ce que vous coûtent réellement une fausse alerte et une fraude manquée.",
    "take4_t": "Une décision doit pouvoir s'expliquer", "take4_p": "Quand un modèle bloque le paiement d'un vrai client, savoir dire pourquoi fait partie du produit.",
    "next_h": "Limites et prochaines étapes",
    "next1_t": "Tester dans le temps", "next1_p": "Ici, l'apprentissage et le test piochent dans les mêmes deux jours, ce qui est optimiste. En production, le modèle apprend sur le passé et doit prédire le futur : c'est ce qu'il faut simuler ensuite (validation temporelle).",
    "next2_t": "Essayer d'autres méthodes de rééquilibrage", "next2_p": "Ici, on donne plus de poids aux fraudes pendant l'apprentissage. On pourrait comparer avec la création de fraudes artificielles (SMOTE).",
    "next3_t": "Rendre les scores plus lisibles", "next3_p": "Calibrer le modèle pour qu'un score de 0,8 signifie vraiment « environ 8 fraudes sur 10 », ce qui facilite le maintien d'un seuil stable dans le temps.",
    "next4_t": "Plus de fraudes pour valider", "next4_p": "Seulement {fraud_test} fraudes dans le test : les résultats sont à prendre comme un ordre de grandeur. Plus de données, ou des découpages répétés, resserreraient les fourchettes.",

    "gl_h": "Petit lexique",
    "gl_intro": "Les termes techniques de ce rapport, en mots de tous les jours.",
    "gl1_t": "Fausse alerte (faux positif)", "gl1_p": "Un paiement normal signalé comme fraude. Coût : du temps d'analyse et un client dérangé.",
    "gl2_t": "Fraude non détectée (faux négatif)", "gl2_p": "Une fraude qui passe. Coût : le montant du paiement.",
    "gl3_t": "Fraudes détectées (rappel)", "gl3_p": "Sur l'ensemble des vraies fraudes, la part que le modèle signale.",
    "gl4_t": "Alertes justifiées (précision)", "gl4_p": "Sur l'ensemble des alertes déclenchées, la part qui sont de vraies fraudes.",
    "gl5_t": "Seuil", "gl5_p": "Le score de risque à partir duquel une alerte est déclenchée. Plus bas : plus d'alertes. Plus haut : moins d'alertes.",
    "gl6_t": "Note globale de qualité (PR-AUC)", "gl6_p": "Une note de 0 à 1 qui résume le compromis entre fraudes détectées et alertes justifiées. Plus adaptée que la « part de bonnes réponses » quand la fraude est rare.",
    "gl7_t": "Validation croisée", "gl7_p": "Apprendre et noter plusieurs fois sur des tranches différentes des données d'entraînement, pour vérifier qu'un résultat n'est pas un hasard.",
    "gl8_t": "Fourchette à 95 %", "gl8_p": "La zone dans laquelle se situe très probablement la vraie note. Une fourchette large signale peu de cas, donc plus d'incertitude.",
    "gl9_t": "SHAP", "gl9_p": "Une méthode qui indique, pour un paiement donné, de combien chaque information a fait monter ou baisser le score de risque.",
    "gl10_t": "Données anonymisées (PCA)", "gl10_p": "Les 28 signaux V1 à V28 sont des combinaisons mathématiques des données d'origine, brouillées pour protéger les clients.",
    "gl11_t": "Déséquilibre des classes", "gl11_p": "Quand un cas est bien plus rare que l'autre (ici 1 fraude pour 600). Cela rend les mesures naïves trompeuses.",
    "gl12_t": "Réglages (hyperparamètres)", "gl12_p": "Des ajustements faits avant l'apprentissage, comme la profondeur maximale des arbres de décision. On les règle par essais successifs.",

    "run_h": "Reproduire l'analyse",
    "run_p": "Pour les personnes techniques : le notebook lit <code>data/creditcard.csv</code> s'il existe, sinon il télécharge le jeu de données avec <code>kagglehub</code>.",
    "copy": "Copier", "copied": "Copié",
    "stack_h": "Outils utilisés",
    "footer_data": "Données : Credit Card Fraud Detection, ULB Machine Learning Group, publié sur Kaggle. Consultez sa page pour les conditions de licence.",
    "footer_by": "Réalisé par",
    "noscript": "Ce rapport dessine ses graphiques avec JavaScript. Le code et les résultats sont disponibles dans le dépôt GitHub.",
    "table_view": "Voir sous forme de tableau",

    "js_legit": "Normal", "js_fraud": "Fraude", "js_share_class": "Part du groupe",
    "js_hour": "heure", "js_rate": "pour 10 000", "js_share_tx": "des paiements",
    "js_recall": "Fraudes détectées (rappel)", "js_precision": "Alertes justifiées (précision)",
    "js_baseline": "Référence", "js_threshold": "Seuil d'alerte", "js_cost_eur": "Coût total (€)", "js_no_model": "Sans modèle",
    "js_alerts": "alertes", "js_caught": "détectées", "js_fa": "fausses alertes", "js_cost": "coût",
    "js_f1_marker": "F1", "js_cost_marker": "coût minimal", "js_default_marker": "0,5",
    "js_pct_range": "tranche", "js_corr": "lien avec la fraude", "js_shap_axis": "Effet sur le score",
    "js_pushes_fraud": "pousse vers la fraude", "js_pushes_legit": "pousse vers le normal",
    "js_true_class": "réalité", "js_percentile": "valeur du signal (de faible à élevée)",
    "js_tbl_feature": "Signal", "js_tbl_value": "Valeur", "js_tbl_hour": "Heure", "js_tbl_tx": "Paiements", "js_tbl_fraud": "Fraudes",
    "js_tbl_rate": "Fraudes / 10 000", "js_tbl_bin": "Tranche de montant", "js_tbl_legit": "Part des normaux", "js_tbl_fraudshare": "Part des fraudes",
    "js_tbl_model": "Approche", "js_tbl_recall": "Fraudes détectées", "js_tbl_prec": "Alertes justifiées", "js_tbl_t": "Seuil", "js_tbl_tp": "Détectées",
    "js_tbl_fp": "Fausses alertes", "js_tbl_cost": "Coût total",
    "js_models": {"logreg": "Régression logistique", "rf": "Forêt aléatoire", "xgb": "XGBoost"},
    "js_cases": {"true_positive": "Une fraude typique, bien détectée", "false_alarm": "La fausse alerte la plus affirmée", "missed_fraud": "La fraude manquée qui est passée le plus près d'être détectée"},
    "js_amount_log": "montant",
    "js_fa_one": "fausse alerte", "js_fa_many": "fausses alertes", "js_neg_corr": "plus faible en cas de fraude", "js_pos_corr": "plus élevée en cas de fraude",
}

STRINGS = {"en": EN, "fr": FR}
