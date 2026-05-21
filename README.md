# 🚗 Auto Sales Data Governance & Monthly Incremental Pipeline

> **Production data engineering portfolio** — 8-layer MySQL data warehouse + 4 production SQL templates + interactive Streamlit demo.

[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit)](https://YOUR-APP-NAME.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0.45-4479A1?logo=mysql)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**By 肖垚聪 (Yaocong Xiao)** · NTU · Data Engineering Intern @ GM Shanghai · 2026.01-05

---

## 🎯 What This Is

A **real production data engineering project** I shipped during my 5-month internship at General Motors China (Short-Term Sales Forecasting team). 

This repo contains:
- 📐 The **architectural decisions** behind an 8-layer MySQL warehouse (18 tables)
- 💻 **4 production SQL templates** (1,700+ lines) for monthly incremental pipeline
- 🎨 An **interactive Streamlit demo** to explore the design + play with the LRM algorithm
- 📄 25 ADRs + 11 ISSUE logs + 16 engineering lessons

**Business impact**: Compressed a 1-2 day manual workflow into a 30-minute repeatable pipeline. Final wide table: 71,304 rows × 38 columns, 99.92% coverage, 8/8 audit checks pass.

> ⚠️ **No real GM data in this repo.** Only synthetic mock data + SQL templates + architecture docs. Real data stays on internal systems.

---

## 🚀 Live Demo

**[👉 Try the interactive demo](https://YOUR-APP-NAME.streamlit.app)**

Highlights:
- **🎯 LRM Playground** — drag MIX% sliders to see the Largest Remainder Method allocate integer volumes in real time
- **🏗️ Architecture viewer** — 8 layers × 18 tables with click-to-expand details
- **🧠 25 Decisions** — every "why this choice over that one" documented

---

## 🏗️ Architecture Overview

8 layers, each with one job:

```
RAW (preserve)
  ↓
STG (normalize names)
  ↓
DIM (govern entities — model_key surrogate keys + 71 mapping rules)
  ↓
STD (apply business rules + dedupe — 7-9 field PK)
  ↓
DWD (sub-aggregations + MIX normalization)
  ↓
DWS (final wide table — LRM integer allocation + sentinel rows for 100% conservation)
  ↓
AUDIT (8 automated quality checks)
  ↓
LOG (full lineage)
```

**Why this matters**: Each layer is independent, idempotent, and auditable. Re-running any month is a `DELETE WHERE year=X AND month=Y` + `INSERT` — no schema drift, no data loss.

---

## 🔥 Top 4 Technical Highlights

### 1. Largest Remainder Method (LRM) — Integer Volume Allocation in Pure SQL
**Problem**: Sales = 12,345 (integer). Need to split across 3 trims by MIX% (decimals). Each trim must get an integer, and the sum must still equal 12,345 — **exactly, every time, no float drift**.

**Solution**: Pure SQL implementation using `FLOOR` + window functions + `ROW_NUMBER` on the fractional remainder. 100% conservation guaranteed. See `LRM Playground` page for a live interactive demo.

### 2. Sentinel-Row Pattern — Solved a 27% Data Loss Bug
**Problem**: My initial `dws` design anchored on the `ways` (catalog) table. If `ways` didn't have a particular `(model, fuel, segment)` bucket, the corresponding sales volume **vanished** — losing **504,955 cars/month (27% of total)**.

**Solution**: Take a UNION of bucket keys across all 3 fact tables. Where `ways` has no trim, insert a sentinel row (`trim_en='__NO_WAYS_TRIM__'`) that absorbs the volume but is filterable by downstream BI. Result: **100% volume conservation**.

### 3. DEFER + Watch List — Reduced Business User Toil
**Problem**: Every month, business users had to review ~50 "new model candidates" — many were just pre-release catalog entries (no actual sales yet). The default options (APPROVE / MERGE / REJECT) forced them to make a call too early.

**Solution**: Added a 4th option — **DEFER** — which parks the candidate in a `dim_new_model_watch` table. **Automatically promotes back to review when sales volume > 0 next month**. Business users went from "annoyed" to "this thinks ahead for me".

### 4. Mapping Rules as a First-Class Data Asset (Not Hardcoded SQL)
**Problem**: Business rules change weekly (brand renames, acquisitions, model merges). Hardcoded SQL means every change = code review + redeploy.

**Solution**: A `brand_model_standard_mapping` table with 71 rows, joined dynamically in the pipeline. New rule = 1 INSERT. Includes `apply_to_table` field for table-scoped rules and `rule_type` for 6 governance categories.

---

## 📁 Repository Layout

```
.
├── streamlit_app.py              # Home page
├── pages/
│   ├── 1_Architecture.py         # 8-layer + 18-table viewer
│   ├── 2_LRM_Playground.py       # Interactive LRM algorithm demo
│   ├── 3_Data_Flow.py            # Step-by-step row transformation
│   ├── 4_Decisions.py            # 25 ADRs + 11 ISSUE logs
│   └── 5_About.py                # About me + how to contact
├── data/
│   ├── mock_combined.csv         # 36 rows of synthetic data
│   └── mock_combined_sample.csv  # Smaller sample
├── docs/
│   ├── DEPLOY.md                 # Streamlit Cloud deployment guide
│   ├── resume_one_pager.pdf      # 1-page resume version
│   └── resume_bullets.md         # 4 variants of resume bullets
├── assets/
│   └── architecture.png          # 8-layer diagram (sharable image)
├── requirements.txt
└── README.md (you're here)
```

---

## 🛠️ Run Locally

```bash
# Clone
git clone https://github.com/xiaoyc2026/auto-sales-pipeline.git
cd auto-sales-pipeline

# Install
pip install -r requirements.txt

# Run
streamlit run streamlit_app.py
```

Open http://localhost:8501

---

## 📊 By the Numbers

| Metric | Value |
|---|---|
| Layers designed | 8 |
| Tables in production | 18 |
| Lines of production SQL | 1,700+ |
| Architectural decisions documented (ADRs) | 25 |
| ISSUE log entries | 11 |
| `dws_wide_table` final size | 71,304 rows × 38 cols |
| Volume conservation accuracy | 100% (LRM-guaranteed) |
| Coverage of new business fields (global_local) | 99.92% |
| Audit checks passing | 8 / 8 |
| Workflow time before → after | 1-2 days → 30 min |

---

## 💡 Engineering Lessons Worth Sharing

1. **MySQL `TABLE_ROWS` is an estimate, never trust it for accuracy** — always `SELECT COUNT(*)`
2. **Hyphenated column names like `global/local` need backticks everywhere** — easy to miss in dynamic SQL
3. **DBeaver CSV imports use `utf8mb4_unicode_ci`**, while MySQL 8.0 default is `utf8mb4_0900_ai_ci` — JOINs across them silently fail on Chinese characters. Always set explicit COLLATE.
4. **`ROWS` is a reserved keyword in MySQL 8.0** — using it as a column alias crashes window functions
5. **`-` as a sentinel value in numeric columns** breaks `CAST AS INT` — always `NULLIF(col, '-')` first
6. **Always run a conservation check (`SUM input = SUM output`) BEFORE the INSERT** — caught my 27% volume loss bug
7. **`SELECT` from a `pages/` file with emoji in filename works on Linux, breaks on Windows** — keep filenames ASCII

(Full list of 16 lessons in `pages/4_Decisions.py`.)

---

## 🎓 About Me

**肖垚聪 (Yaocong Xiao)**, Data Engineering Intern.

Currently studying at **Nanyang Technological University, Singapore**. Spent 5 months at General Motors China designing this data warehouse from scratch. Looking for full-time **Data Engineering / Data Analyst** roles at major internet companies — especially anywhere I can keep building data infrastructure that business teams actually rely on.

📩 [yaocong001@e.ntu.edu.sg](mailto:yaocong001@e.ntu.edu.sg)
💻 [github.com/xiaoyc2026](https://github.com/xiaoyc2026)

---

## 📜 License

MIT — feel free to use the architecture patterns, SQL templates, or Streamlit demo structure for your own learning / projects. A shoutout would be appreciated but not required.

⭐ **If this project helped you understand data warehousing or you're a recruiter who wants to chat, drop a star and shoot me an email!**
