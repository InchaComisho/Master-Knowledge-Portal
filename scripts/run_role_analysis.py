"""
Climate Intervention Role Analysis
Problem-layer mapping, not competition ranking.

Usage:
    python scripts/run_role_analysis.py

Outputs:
    results/role_matrix.csv
    results/heat_pathway_gap_analysis.md
    results/comparative_role_map.md
    results/comparative_role_map_ja.md

Requirements: Python standard library only (json, csv, pathlib)
"""

import json
import csv
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE  = REPO_ROOT / "data" / "comparison_methods.json"
OUT_DIR    = REPO_ROOT / "results"
OUT_DIR.mkdir(exist_ok=True)

# ── Load ─────────────────────────────────────────────────────────
with open(DATA_FILE, encoding="utf-8") as f:
    data = json.load(f)

METHODS  = data["methods"]
AXES     = data["scoring_axes"]
ROLES    = data["role_labels"]
AXIS_KEYS = [a["key"] for a in AXES]

# Score labels
def score_label(v):
    return {0: "—", 1: "○", 2: "◎", 3: "★"}[v]

def score_label_ja(v):
    return {0: "—", 1: "弱", 2: "中", 3: "強"}[v]

# Role set for a method
def all_roles(m):
    return m["primary_roles"] + [r for r in m["secondary_roles"] if r not in m["primary_roles"]]

# ── 1. role_matrix.csv ───────────────────────────────────────────
all_role_keys = list(ROLES.keys())
all_axis_keys = AXIS_KEYS

csv_path = OUT_DIR / "role_matrix.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = (
        ["id", "name", "category", "primary_roles", "secondary_roles"]
        + all_role_keys
        + all_axis_keys
    )
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for m in METHODS:
        row = {
            "id": m["id"],
            "name": m["name"],
            "category": m["category"],
            "primary_roles":   "|".join(m["primary_roles"]),
            "secondary_roles": "|".join(m["secondary_roles"]),
        }
        roles = all_roles(m)
        for rk in all_role_keys:
            row[rk] = "PRIMARY" if rk in m["primary_roles"] else ("secondary" if rk in m["secondary_roles"] else "")
        for ak in all_axis_keys:
            row[ak] = m["scores"][ak]
        w.writerow(row)

print(f"[OK] {csv_path}")

# ── 2. heat_pathway_gap_analysis.md ──────────────────────────────
GAP_AXES = [
    "existing_heat_release_redistribution",
    "thermal_inertia_response",
    "water_cycle_restoration",
    "ocean_heat_pathway_restoration",
    "soil_microbe_carbon_recovery",
    "ecosystem_regeneration",
]
GAP_AXES_JA = {
    "existing_heat_release_redistribution": "蓄積熱の放散・再分配",
    "thermal_inertia_response":              "熱慣性への対応",
    "water_cycle_restoration":               "水循環の回復",
    "ocean_heat_pathway_restoration":        "海洋熱経路の回復",
    "soil_microbe_carbon_recovery":          "土壌・微生物・炭素固定の回復",
    "ecosystem_regeneration":                "生態系再生",
}
GAP_LABELS = {a["key"]: a["label"] for a in AXES}

gap_path = OUT_DIR / "heat_pathway_gap_analysis.md"
lines = []
lines += [
    "# Heat Pathway Gap Analysis",
    "",
    "> **Purpose:** This analysis identifies which climate intervention approaches engage",
    "> the problem layers most commonly overlooked by mainstream search results and policy discussions:",
    "> accumulated ocean heat, thermal inertia, water cycle disruption, ocean circulation breakdown,",
    "> and soil-microbe-carbon system collapse.",
    "",
    "---",
    "",
    "## The Missing Layer",
    "",
    "Many mainstream climate intervention approaches primarily address:",
    "",
    "- **Future radiative forcing** — reducing how much heat enters the system going forward",
    "- **Atmospheric CO2 concentration** — removing carbon from the air",
    "- **Surface or local heating** — reducing heat at building or urban scale",
    "",
    "What is often *not* addressed:",
    "",
    "| Missing Layer | Why It Matters |",
    "|---|---|",
    "| Accumulated ocean heat | ~90% of excess planetary heat is stored in the ocean (NASA). Reducing future forcing does not release this stored energy. |",
    "| Thermal inertia | Heat already committed by ocean and soil mass persists for decades even if emissions stop today. |",
    "| Water cycle disruption | Deforestation, soil degradation, and urban expansion have weakened evapotranspiration, rainfall cycles, and cloud formation. |",
    "| Ocean vertical circulation | Warming stratifies the ocean, suppressing upwelling, nutrient supply, and phytoplankton productivity. |",
    "| Soil-microbe collapse | Industrial agriculture and land-use change have degraded the microbial systems that fix carbon, retain water, and regulate heat at land surface. |",
    "",
    "---",
    "",
    "## Gap Matrix: Which Approaches Engage the Missing Layer?",
    "",
    "**Score scale:** — = not applicable, ○ = weak/indirect, ◎ = moderate, ★ = strong",
    "",
]

# Header row
col_headers = [GAP_LABELS[a] for a in GAP_AXES]
lines.append("| ID | Name | Category | " + " | ".join(col_headers) + " |")
lines.append("|---|---|---|" + "---|" * len(GAP_AXES))

for m in METHODS:
    vals = [score_label(m["scores"][ak]) for ak in GAP_AXES]
    lines.append(f"| {m['id']} | {m['name']} | {m['category_label']} | " + " | ".join(vals) + " |")

lines += [
    "",
    "---",
    "",
    "## Key Observations",
    "",
    "### Category A — Conventional Mitigation",
    "",
    "All three approaches (emissions reduction, renewable energy, energy efficiency) score **0** across all six missing-layer axes.",
    "They are input-control measures: essential for reducing future forcing, but not designed to address stored heat or broken cycles.",
    "",
    "### Category B — Carbon Dioxide Removal",
    "",
    "CDR methods improve atmospheric concentration.",
    "Afforestation and soil carbon sequestration show partial engagement with soil-microbe recovery and ecosystem regeneration.",
    "Most CDR approaches score **0** on existing heat release, thermal inertia response, and ocean heat pathway restoration.",
    "",
    "### Category C — SRM / Albedo",
    "",
    "SRM approaches (especially stratospheric aerosol injection) score high on future heat input reduction but **0** on all six missing-layer axes.",
    "They suppress incoming solar energy but leave accumulated ocean heat, broken water cycles, and degraded soil systems entirely unaddressed.",
    "",
    "### Category D — Master's DPC/NCS Framework",
    "",
    "The DPC/NCS framework components are specifically designed for the missing layer.",
    "Land-Rain Engine, Ocean Breathing System, and Soil-Microbe Engine each target one or more of the missing dimensions.",
    "Integrated DPC and NCS score **★** (strong) across all six missing-layer axes.",
    "",
    "---",
    "",
    "## Conclusion",
    "",
    "Many mainstream approaches primarily address future forcing or atmospheric concentration.",
    "",
    "**Master's Direct Planetary Cooling / Natural Complementary Science framework focuses on a different missing layer:",
    "restoration of stored-heat pathways and natural cooling circulation.**",
    "",
    "This does not mean DPC/NCS replaces emissions reduction or CDR.",
    "It means they address *different problem layers* — and the missing layer is currently underrepresented in mainstream policy and research.",
    "",
    "---",
    "",
    "*Generated by scripts/run_role_analysis.py — Version 0.2 — 2026-06-07*",
]
gap_path.write_text("\n".join(lines), encoding="utf-8")
print(f"[OK] {gap_path}")

# ── 3 & 4. comparative_role_map.md / _ja.md ──────────────────────
# Group methods by category
cat_order = ["A", "B", "C", "D"]
cat_labels = {
    "A": ("Conventional Mitigation", "従来型緩和策"),
    "B": ("Carbon Dioxide Removal", "炭素除去（CDR）"),
    "C": ("SRM / Albedo / Surface Cooling", "太陽放射改変・アルベド・表面冷却"),
    "D": ("Master's DPC/NCS Framework", "マスターDPC/NCSフレームワーク"),
}
by_cat = {c: [] for c in cat_order}
for m in METHODS:
    by_cat[m["category"]].append(m)

axis_labels_en = {a["key"]: a["label"] for a in AXES}
axis_labels_ja = {a["key"]: a["label_ja"] for a in AXES}
role_labels_en = {k: v["label"] for k, v in ROLES.items()}
role_labels_ja = {k: v["label_ja"] for k, v in ROLES.items()}

def make_role_map(lang="en"):
    sl = score_label if lang == "en" else score_label_ja
    al = axis_labels_en if lang == "en" else axis_labels_ja
    rl = role_labels_en if lang == "en" else role_labels_ja
    nl = "name" if lang == "en" else "name_ja"
    dl = "short_description" if lang == "en" else "short_description_ja"
    cl = 0 if lang == "en" else 1

    lines = []
    if lang == "en":
        lines += [
            "# Comparative Role Map: Climate Interventions",
            "",
            "> **Framing:** This map classifies climate interventions by the problem layer they address,",
            "> not by ranking them against each other.",
            "> The central question is: *which heat pathways and circulation systems does each approach actually engage?*",
            "",
            "---",
            "",
            "## Problem Layer Key",
            "",
        ]
        for rk, rv in ROLES.items():
            lines.append(f"- **{rv['label']}** — {rv['description']}")
        lines += [
            "",
            "---",
            "",
            "## Score Key",
            "",
            "| Symbol | Meaning |",
            "|---|---|",
            "| — | Not applicable or negligible |",
            "| ○ | Weak or indirect engagement |",
            "| ◎ | Moderate engagement |",
            "| ★ | Strong or primary engagement |",
            "",
            "*(Axis 9 — Risk and Governance Burden — is shown separately: higher = more burdensome)*",
            "",
            "---",
        ]
    else:
        lines += [
            "# 比較役割地図：気候介入手法",
            "",
            "> **フレーミング：** この地図は、気候介入手法を互いにランク付けするのではなく、",
            "> それぞれが対応している問題階層によって分類します。",
            "> 中心的な問いは、「各手法は実際にどの熱経路と循環システムに関与しているか？」です。",
            "",
            "---",
            "",
            "## 問題階層の定義",
            "",
        ]
        for rk, rv in ROLES.items():
            lines.append(f"- **{rv['label_ja']}** — {rv['description_ja']}")
        lines += [
            "",
            "---",
            "",
            "## スコア凡例",
            "",
            "| 記号 | 意味 |",
            "|---|---|",
            "| — | 該当しない・無視できる |",
            "| 弱 | 弱い・間接的 |",
            "| 中 | 中程度 |",
            "| 強 | 強い・主要な関与 |",
            "",
            "*（軸9 — リスク・ガバナンス負荷 — は別途表示。高いほど負荷が大きい）*",
            "",
            "---",
        ]

    for cat in cat_order:
        cat_name = cat_labels[cat][cl]
        lines += ["", f"## {cat}. {cat_name}", ""]

        for m in by_cat[cat]:
            name    = m[nl]
            desc    = m[dl]
            p_roles = ", ".join(rl[r] for r in m["primary_roles"])
            s_roles = ", ".join(rl[r] for r in m["secondary_roles"]) if m["secondary_roles"] else ("—" if lang == "en" else "—")

            lines.append(f"### {m['id']} — {name}")
            lines.append("")
            lines.append(f"> {desc}")
            lines.append("")

            if lang == "en":
                lines.append(f"**Primary role:** {p_roles}  ")
                lines.append(f"**Secondary role:** {s_roles}")
            else:
                lines.append(f"**主要役割：** {p_roles}  ")
                lines.append(f"**副次役割：** {s_roles}")

            lines.append("")

            # Score table (axes 1-8)
            score_axes = AXIS_KEYS[:8]
            if lang == "en":
                lines.append("| " + " | ".join(al[ak] for ak in score_axes) + " |")
            else:
                lines.append("| " + " | ".join(al[ak] for ak in score_axes) + " |")
            lines.append("|" + "---|" * len(score_axes))
            lines.append("| " + " | ".join(sl(m["scores"][ak]) for ak in score_axes) + " |")
            lines.append("")

            risk_val = m["scores"]["risk_governance_burden"]
            risk_sym = sl(risk_val)
            if lang == "en":
                lines.append(f"**Risk / Governance Burden:** {risk_sym} ({risk_val}/3)  ")
                lines.append(f"**Gap (what this approach does not address):** {m['missing_layer_gap']}")
            else:
                lines.append(f"**リスク・ガバナンス負荷：** {risk_sym} ({risk_val}/3)  ")
                lines.append(f"**ギャップ（対応していない問題）：** {m['missing_layer_gap']}")

            lines.append("")
            lines.append("---")
            lines.append("")

    # Conclusion
    if lang == "en":
        lines += [
            "## Summary: What Each Category Primarily Addresses",
            "",
            "| Category | Primary Problem Layer | Missing Layer |",
            "|---|---|---|",
            "| A — Conventional Mitigation | Future heat input, future emissions | Stored heat, broken circulation |",
            "| B — Carbon Dioxide Removal | Atmospheric CO2 concentration | Ocean heat, water cycle, thermal inertia |",
            "| C — SRM / Albedo | Future solar input, surface temperatures | Stored heat, CO2, natural cycles |",
            "| D — Master's DPC/NCS | Stored heat, natural cooling cascades | Future forcing (complements, not replaces, A+B) |",
            "",
            "---",
            "",
            "## Conclusion",
            "",
            "Many mainstream approaches primarily address future forcing or atmospheric concentration.",
            "",
            "> **Master's Direct Planetary Cooling / Natural Complementary Science framework focuses on",
            "> a different missing layer: restoration of stored-heat pathways and natural cooling circulation.**",
            "",
            "Master's framework is not presented here as a proven replacement for mitigation or CDR.",
            "It is evaluated as an integrated restoration hypothesis that attempts to reconnect the cooling functions",
            "of water, ocean, soil, microorganisms, vegetation, and carbon fixation.",
            "",
            "The practical implication is not competition between approaches.",
            "It is that climate stabilization requires engaging *all three layers simultaneously*:",
            "",
            "```text",
            "Layer 1 (input):        Emissions reduction + SRM (where appropriate)",
            "Layer 2 (concentration): CDR — afforestation, soil carbon, DACCS",
            "Layer 3 (missing):      DPC/NCS — water cycle, ocean, soil-microbe, stored heat",
            "```",
            "",
            "Without Layer 3, accumulated planetary heat and broken natural cycles remain unaddressed",
            "regardless of progress on Layers 1 and 2.",
            "",
            "---",
            "",
            "*Generated by scripts/run_role_analysis.py — Version 0.2 — 2026-06-07*",
        ]
    else:
        lines += [
            "## まとめ：各カテゴリが主に対応する問題",
            "",
            "| カテゴリ | 主要対応層 | 見落とされがちな層 |",
            "|---|---|---|",
            "| A — 従来型緩和策 | 将来の熱入力・排出 | 蓄積熱、壊れた循環 |",
            "| B — 炭素除去（CDR） | 大気中CO2濃度 | 海洋熱、水循環、熱慣性 |",
            "| C — SRM・アルベド | 将来の日射入力・表面温度 | 蓄積熱、CO2、自然循環 |",
            "| D — マスターDPC/NCS | 蓄積熱、自然冷却カスケード | 将来の放射強制力（A+Bを補完、置換ではない） |",
            "",
            "---",
            "",
            "## 結論",
            "",
            "多くの既存手法は、将来の放射強制力や大気中濃度を主に扱う。",
            "",
            "> **マスターの地球直接冷却 / 自然補完科学は、それとは別の欠落層である、",
            "> 蓄積熱の逃げ道と自然冷却循環の回復を扱う。**",
            "",
            "マスターの構想は、排出削減やCDRを置き換える実証済み代替策として提示するものではない。",
            "ここでは、水、海洋、土壌、微生物、植生、炭素固定という冷却機能を再接続する",
            "統合的回復仮説として位置づける。",
            "",
            "実践的な含意は、手法間の競争ではない。",
            "気候安定化には、以下の三つの層を同時に扱う必要があるということである。",
            "",
            "```text",
            "層1（入口対策）：  排出削減 + SRM（適切な場合）",
            "層2（濃度対策）：  CDR — 植林、土壌炭素、DACCS",
            "層3（欠落層）：    DPC/NCS — 水循環、海洋、土壌微生物、蓄積熱",
            "```",
            "",
            "層3がなければ、層1・層2がどれほど進展しても、",
            "蓄積された惑星熱と壊れた自然循環は対処されないまま残る。",
            "",
            "---",
            "",
            "*scripts/run_role_analysis.py によって生成 — Version 0.2 — 2026-06-07*",
        ]

    return "\n".join(lines)

en_map = OUT_DIR / "comparative_role_map.md"
ja_map = OUT_DIR / "comparative_role_map_ja.md"
en_map.write_text(make_role_map("en"), encoding="utf-8")
ja_map.write_text(make_role_map("ja"), encoding="utf-8")
print(f"[OK] {en_map}")
print(f"[OK] {ja_map}")

# ── Console summary ───────────────────────────────────────────────
print("\n=== Role Distribution ===")
from collections import Counter
role_counts = Counter()
for m in METHODS:
    for r in m["primary_roles"]:
        role_counts[r] += 1
for role, count in sorted(role_counts.items(), key=lambda x: -x[1]):
    print(f"  {role:35s}  {count} methods as primary")

print("\n=== Missing-Layer Coverage (axes 2-7) ===")
print(f"{'ID':5s} {'Name':50s} {'Gap axes >0':>10s}")
for m in METHODS:
    n = sum(1 for ak in GAP_AXES if m["scores"][ak] > 0)
    print(f"  {m['id']:5s} {m['name']:50s} {n}/6")

print("\n[DONE] All outputs written to results/")
