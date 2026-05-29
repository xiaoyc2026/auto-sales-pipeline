"""Decision Records - showcase 25 architectural decisions"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Decisions", page_icon="🧠", layout="wide")

st.title("🧠 Architectural Decisions Documented")
st.markdown("""
Throughout the project I documented **25 key architectural decisions** in a Q1-Q25 log
(plus 11 known issues, ISSUE-001 to 011). Below are the most impactful ones — each shows
the reasoning, alternatives considered, and tradeoff acknowledged.

This is the **closest peek into "how I think"** as a data engineer.
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Top 8 Decisions
# ─────────────────────────────────────────────────────────────

decisions = [
    {
        "id": "Q4",
        "title": "Use surrogate key `model_key` instead of (brand, model, manufacturer) composite",
        "context": "Business renames brands frequently (e.g., GEELY→Zeekr). Composite key would cascade updates across all 7 fact tables.",
        "decision": "Auto-incrementing integer `model_key` as PK; composite key only in dim layer.",
        "tradeoff": "Indirection cost (extra JOIN), but business renames now require updating only `dim_model_enriched` 1 row.",
        "impact": "Saved ~3 hours of manual data migration when 9 GEELY models were renamed to Zeekr brand mid-project.",
    },
    {
        "id": "Q5",
        "title": "Mapping rules as DATA in MySQL, not hardcoded SQL",
        "context": "Business added new brand/model rename rules ~5x/month. Hardcoding in SQL meant code change + deploy for every rule.",
        "decision": "Created `brand_model_standard_mapping` table with `apply_to_table` column (ALL/combined/insurance/ways).",
        "tradeoff": "Slightly slower INSERT (LEFT JOIN), but business analysts can now manage rules independently.",
        "impact": "71 rules accumulated by end of project, zero developer involvement for rule additions.",
    },
    {
        "id": "Q10",
        "title": "4-bucket new-model triage (not 3)",
        "context": "Standard was 3 buckets: APPROVE / MERGE / REJECT. Some new models appear in catalog before any sales — analyst couldn't decide.",
        "decision": "Added 4th bucket: DEFER + `dim_new_model_watch` table. Auto-promotes to PENDING when volume > 0.",
        "tradeoff": "1 more table + 30 more lines of SQL, but analyst burden dropped significantly.",
        "impact": "21/55 new models DEFERred in 2026-03; analyst spent 5 min instead of 30 min on triage.",
    },
    {
        "id": "Q14",
        "title": "Sentinel-row pattern in DWS wide table",
        "context": "DWS originally used ways-anchored design. Discovered 27% of `combined_volume` (504K cars!) was being lost.",
        "decision": "Changed to (ways ∪ combined ∪ insurance) bucket union; for buckets with no ways trim, emit a sentinel row with `trim_en='__NO_WAYS_TRIM__'`.",
        "tradeoff": "1144 extra sentinel rows in DWS (10% bloat), but 100% volume conservation guaranteed.",
        "impact": "Bonus: sentinel rows became business value — they're literally 'ways catalog to-do list' for analyst.",
    },
    {
        "id": "Q15",
        "title": "LRM algorithm for integer volume allocation",
        "context": "Need to allocate integer cars across trim variants based on MIX%, conserve total, be deterministic.",
        "decision": "Implement Largest Remainder Method (a.k.a. Hamilton's apportionment method) in pure SQL using window functions.",
        "tradeoff": "More complex SQL than ROUND, but mathematically guaranteed conservation.",
        "impact": "0 conservation errors across 1,939 buckets × 12 months of historical data.",
    },
    {
        "id": "Q22",
        "title": "Treat `-` as NULL across all numeric/date columns",
        "context": "Excel data uses `'-'` as 'no value' sentinel in many columns (nedc_range, transmission, etc.). Caused INT casting errors.",
        "decision": "Apply `NULLIF(col, '-')` at the STG layer for all suspect columns. Add to checklist.",
        "tradeoff": "Loses semantic distinction between 'unknown' vs 'not applicable', but data type integrity preserved.",
        "impact": "Fixed 2,345 row import failures in ways data with 1 SQL line.",
    },
    {
        "id": "Q11",
        "title": "Apply mapping rules BEFORE new-model detection (not after)",
        "context": "Initial design did new-model detection on raw data — got 200+ 'new' models that were just GEELY/Zeekr renames.",
        "decision": "Insert normalization step (apply 71 mapping rules) between RAW and DETECT.",
        "tradeoff": "1 extra table (`stg_inbox_*_normalized`), but new-model count dropped from 200 → 55 (truly new).",
        "impact": "Analyst review time dropped 70%. Discovered design pattern: 'normalize before discover'.",
    },
    {
        "id": "Q21",
        "title": "Keep STD and DWD as separate layers, despite tempting to merge",
        "context": "STD does dedup + attribute mapping. DWD does monthly aggregation. They look similar.",
        "decision": "Keep separated. STD is row-level (1 row per business key + bodystyle). DWD is bucket-aggregated.",
        "tradeoff": "1 extra layer to maintain, but each layer is independently testable + reusable.",
        "impact": "When mix algorithm bug was found, fix was in 1 layer; STD untouched.",
    },
]

# Display as expandable cards
for d in decisions:
    with st.expander(f"**{d['id']}** · {d['title']}", expanded=False):
        c1, c2 = st.columns([1, 4])
        with c1:
            st.markdown(f"### {d['id']}")
        with c2:
            st.markdown(f"**Context**\n\n{d['context']}")
            st.markdown(f"**Decision**\n\n{d['decision']}")
            st.markdown(f"**Tradeoff**\n\n{d['tradeoff']}")
            st.success(f"**Impact**: {d['impact']}")

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Issues (curated)
# ─────────────────────────────────────────────────────────────
st.markdown("## 🐛 Notable Issues Discovered & Fixed")

issues = [
    {
        "id": "ISSUE-001",
        "title": "UTF-8 encoding loss in CSV pipeline",
        "severity": "🔴 CRITICAL",
        "description": "Greek letters (α, π) in model names became `?` in MySQL.",
        "fix": "Enforced utf8mb4_0900_ai_ci collation end-to-end + explicit UTF-8 in pd.read_csv.",
    },
    {
        "id": "ISSUE-007",
        "title": "27% of combined volume lost in DWS wide table",
        "severity": "🔴 CRITICAL",
        "description": "Original DWS logic used a ways-centered INNER JOIN. Combined buckets with no matching ways trim were silently dropped → 27% volume missing.",
        "fix": "Restructured to bucket-union design + sentinel-row pattern (Q14). Recovered 504,955 cars.",
    },
    {
        "id": "ISSUE-009",
        "title": "Cross-manufacturer MERGE creates orphan dim row",
        "severity": "🟡 WARN",
        "description": "Business marked NIO/ES9 → GAC MOTOR/ES9 but GAC MOTOR/ES9 doesn't exist in dim.",
        "fix": "Logged for next month's review; raw NIO/ES9 falls back to APPROVE_AS_NEW path.",
    },
    {
        "id": "ISSUE-010",
        "title": "fuel_type aliases ('ICE', 'GASOLINE') treated as distinct",
        "severity": "🟡 WARN",
        "description": "Same fuel was sometimes 'ICE' (informal) and 'GASOLINE' (formal). Split rows.",
        "fix": "Added Q22 rule R-FUEL-1: `CASE WHEN BINARY fuel='ICE' THEN 'GASOLINE'`.",
    },
    {
        "id": "ISSUE-011",
        "title": "DBeaver CSV imports use different collation than DB",
        "severity": "🟢 INFO",
        "description": "Temp tables created with utf8mb4_unicode_ci while production uses utf8mb4_0900_ai_ci.",
        "fix": "JOIN conditions add `COLLATE utf8mb4_0900_ai_ci` explicitly when joining temp + prod tables.",
    },
]

for i in issues:
    with st.expander(f"{i['severity']} · **{i['id']}** · {i['title']}"):
        st.markdown(f"**Description**\n\n{i['description']}")
        st.markdown(f"**Fix**\n\n{i['fix']}")

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Full list link
# ─────────────────────────────────────────────────────────────
st.markdown("### 📚 Full Documentation")
st.info("""
The complete documentation includes:
- **25 decisions** (Q1-Q25) with full context
- **11 issues** (ISSUE-001 to 011) with reproduction steps
- **16 engineering lessons** learned (the "don't repeat my mistakes" log)
- **18 table schemas** with field-by-field rationale

→ Available in GitHub repo under `/docs/`
""")
