"""
Comparative Scoring Simulation
Climate Intervention Approaches vs Master's Direct Planetary Cooling / Natural Complementary Science

Usage:
    python scripts/run_comparison_simulation.py

Outputs:
    results/comparison_scores.csv
    results/comparison_rankings.md
    results/comparison_rankings_ja.md

Requirements: Python standard library only (json, csv, os, pathlib)
"""

import json
import csv
import os
from pathlib import Path

# ── Path resolution ──────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "data" / "comparison_methods.json"
RESULTS_DIR = REPO_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ── Load data ────────────────────────────────────────────────────
with open(DATA_FILE, encoding="utf-8") as f:
    data = json.load(f)

BENEFIT_AXES = data["scoring_axes"]["benefit"]
RISK_AXES = data["scoring_axes"]["risk"]
SCENARIOS = data["scenarios"]
METHODS = data["methods"]

# ── Score calculation ─────────────────────────────────────────────
def compute_scores(method):
    s = method["scores"]
    benefit = sum(s[ax] for ax in BENEFIT_AXES)
    risk    = sum(s[ax] for ax in RISK_AXES)
    net     = benefit - risk
    return benefit, risk, net

def compute_weighted_score(method, weights):
    s = method["scores"]
    score = 0.0
    for ax in BENEFIT_AXES:
        score += s[ax] * weights.get(ax, 1.0)
    for ax in RISK_AXES:
        score -= s[ax] * weights.get(ax, 1.0)
    return round(score, 2)

# ── Build full score table ────────────────────────────────────────
rows = []
for m in METHODS:
    benefit, risk, net = compute_scores(m)
    row = {
        "id":            m["id"],
        "name":          m["name"],
        "category":      m["category"],
        "category_label": m["category_label"],
        "benefit_score": benefit,
        "risk_score":    risk,
        "net_score":     net,
        "uncertainty":   m["uncertainty"],
    }
    for sc_key, sc_val in SCENARIOS.items():
        row[sc_key] = compute_weighted_score(m, sc_val["weights"])
    rows.append(row)

# ── Write CSV ─────────────────────────────────────────────────────
csv_path = RESULTS_DIR / "comparison_scores.csv"
fieldnames = ["id", "name", "category", "category_label",
              "benefit_score", "risk_score", "net_score", "uncertainty"] + list(SCENARIOS.keys())

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] Wrote {csv_path}")

# ── Ranking helpers ───────────────────────────────────────────────
def ranked(rows, key, reverse=True):
    return sorted(rows, key=lambda r: r[key], reverse=reverse)

def category_badge(cat):
    badges = {"A": "Conventional Mitigation",
              "B": "Carbon Dioxide Removal",
              "C": "SRM / Albedo",
              "D": "Master DPC/NCS"}
    return badges.get(cat, cat)

def category_badge_ja(cat):
    badges = {"A": "従来型緩和策",
              "B": "炭素除去（CDR）",
              "C": "太陽放射改変/アルベド",
              "D": "マスターDPC/NCS"}
    return badges.get(cat, cat)

# ── Generate English rankings markdown ───────────────────────────
def make_rankings_en(rows):
    lines = []
    lines.append("# Comparative Simulation — Ranking Results")
    lines.append("")
    lines.append("> **Scientific caution:** These rankings are derived from a conceptual scoring simulation, not a physical climate model.")
    lines.append("> Scores reflect the author's qualitative judgment based on published literature and the Natural Complementary Science framework.")
    lines.append("> They should not be cited as quantitative climate projections.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Net score ranking
    lines.append("## Overall Net Score Ranking")
    lines.append("")
    lines.append("| Rank | ID | Name | Category | Benefit | Risk | Net Score | Uncertainty |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(ranked(rows, "net_score"), 1):
        lines.append(
            f"| {i} | {r['id']} | {r['name']} | {category_badge(r['category'])} "
            f"| {r['benefit_score']} | {r['risk_score']} | **{r['net_score']}** | {r['uncertainty']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Scenario rankings
    for sc_key, sc_val in SCENARIOS.items():
        lines.append(f"## Scenario: {sc_val['name']}")
        lines.append("")
        lines.append(f"*{sc_val['description']}*")
        lines.append("")
        lines.append("| Rank | ID | Name | Category | Weighted Score | Uncertainty |")
        lines.append("|---|---|---|---|---|---|")
        for i, r in enumerate(ranked(rows, sc_key), 1):
            lines.append(
                f"| {i} | {r['id']} | {r['name']} | {category_badge(r['category'])} "
                f"| **{r[sc_key]}** | {r['uncertainty']} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")

    # Individual scores table
    lines.append("## Full Scores by Method")
    lines.append("")
    axis_headers = " | ".join(BENEFIT_AXES + RISK_AXES)
    lines.append(f"| ID | Name | {axis_headers} |")
    lines.append("|---|---" + "|---" * (len(BENEFIT_AXES) + len(RISK_AXES)) + "|")
    for m in METHODS:
        s = m["scores"]
        vals = " | ".join(str(s[ax]) for ax in BENEFIT_AXES + RISK_AXES)
        lines.append(f"| {m['id']} | {m['name']} | {vals} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Interpretation Notes")
    lines.append("")
    lines.append("- **SRM / Stratospheric Aerosol Injection** scores high on fast cooling and heat-input suppression, but has the highest governance and ecological risk, zero accumulated-heat pathway restoration, and zero civilization fit.")
    lines.append("- **CDR methods** (especially afforestation, soil carbon) score well on carbon fixation and ecosystem co-benefits, but most do not address accumulated ocean heat or water/ocean cycle recovery directly.")
    lines.append("- **Conventional mitigation** is essential as a foundation but scores low on accumulated heat restoration and natural cycle recovery.")
    lines.append("- **Master's DPC/NCS framework** is evaluated here as an *integrated restoration hypothesis*. Its unique strength is simultaneously addressing water cycle, ocean vertical circulation, soil-microbe recovery, and carbon fixation. Its lower scores on technology readiness and speed reflect the honest fact that this is a research-stage framework, not a deployed technology.")
    lines.append("- **Master's framework is not presented as a proven replacement for mitigation or CDR.** It is evaluated as an integrated restoration hypothesis that attempts to reconnect the cooling functions of water, ocean, soil, microorganisms, vegetation, and carbon fixation.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by scripts/run_comparison_simulation.py*")
    lines.append("*Version 0.1 — 2026-06-07*")
    return "\n".join(lines)

# ── Generate Japanese rankings markdown ──────────────────────────
def make_rankings_ja(rows):
    lines = []
    lines.append("# 比較シミュレーション — ランキング結果")
    lines.append("")
    lines.append("> **科学的注意：** このランキングは、物理的な気候モデルではなく、概念的なスコアリングシミュレーションから導かれたものです。")
    lines.append("> スコアは、公開文献と自然補完科学フレームワークに基づく著者の定性的評価を反映しています。")
    lines.append("> 定量的な気候予測として引用しないでください。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Net score ranking
    lines.append("## 総合ネットスコアランキング")
    lines.append("")
    lines.append("| 順位 | ID | 手法名 | カテゴリ | ベネフィット | リスク | ネットスコア | 不確実性 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(ranked(rows, "net_score"), 1):
        m_data = next(m for m in METHODS if m["id"] == r["id"])
        name_ja = m_data.get("name_ja", r["name"])
        lines.append(
            f"| {i} | {r['id']} | {name_ja} | {category_badge_ja(r['category'])} "
            f"| {r['benefit_score']} | {r['risk_score']} | **{r['net_score']}** | {r['uncertainty']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Scenario rankings
    for sc_key, sc_val in SCENARIOS.items():
        lines.append(f"## シナリオ：{sc_val['name_ja']}")
        lines.append("")
        lines.append(f"*{sc_val['description']}*")
        lines.append("")
        lines.append("| 順位 | ID | 手法名 | カテゴリ | 重み付きスコア | 不確実性 |")
        lines.append("|---|---|---|---|---|---|")
        for i, r in enumerate(ranked(rows, sc_key), 1):
            m_data = next(m for m in METHODS if m["id"] == r["id"])
            name_ja = m_data.get("name_ja", r["name"])
            lines.append(
                f"| {i} | {r['id']} | {name_ja} | {category_badge_ja(r['category'])} "
                f"| **{r[sc_key]}** | {r['uncertainty']} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## 解釈ノート")
    lines.append("")
    lines.append("- **SRM / 成層圏エアロゾル散布** は、冷却速度と熱入力抑制で高得点だが、ガバナンスと生態系リスクが最高で、蓄積熱経路回復はゼロ、文明整合性もゼロである。")
    lines.append("- **CDR手法**（植林、土壌炭素等）は炭素固定と生態系副次効果で良好なスコアだが、蓄積した海洋熱や水循環・海洋循環の直接回復には効果が限定的である。")
    lines.append("- **従来型緩和策**は基盤として不可欠だが、蓄積熱回復と自然循環回復ではスコアが低い。")
    lines.append("- **マスターのDPC/NCSフレームワーク**は、ここでは*統合的回復仮説*として評価される。その独自の強みは、水循環、海洋鉛直循環、土壌微生物回復、炭素固定を同時に扱う点にある。技術成熟度と速度のスコアが低いのは、これが展開済み技術ではなく研究段階のフレームワークであるという誠実な評価を反映している。")
    lines.append("- **マスターの構想は、排出削減やCDRを置き換える実証済み代替策として提示するものではない。** ここでは、水、海洋、土壌、微生物、植生、炭素固定という冷却機能を再接続する統合的回復仮説として評価する。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*scripts/run_comparison_simulation.py によって生成*")
    lines.append("*Version 0.1 — 2026-06-07*")
    return "\n".join(lines)

# ── Write rankings ────────────────────────────────────────────────
en_path = RESULTS_DIR / "comparison_rankings.md"
ja_path = RESULTS_DIR / "comparison_rankings_ja.md"

with open(en_path, "w", encoding="utf-8") as f:
    f.write(make_rankings_en(rows))
print(f"[OK] Wrote {en_path}")

with open(ja_path, "w", encoding="utf-8") as f:
    f.write(make_rankings_ja(rows))
print(f"[OK] Wrote {ja_path}")

# ── Console summary ───────────────────────────────────────────────
print("\n=== Top 5 by Net Score ===")
for i, r in enumerate(ranked(rows, "net_score")[:5], 1):
    print(f"  {i}. [{r['id']}] {r['name']:50s}  net={r['net_score']:>3}  "
          f"benefit={r['benefit_score']:>2}  risk={r['risk_score']:>2}")

for sc_key, sc_val in SCENARIOS.items():
    print(f"\n=== Top 5 — {sc_val['name']} ===")
    for i, r in enumerate(ranked(rows, sc_key)[:5], 1):
        print(f"  {i}. [{r['id']}] {r['name']:50s}  weighted={r[sc_key]:>6}")

print("\n[DONE] All results written to results/")
