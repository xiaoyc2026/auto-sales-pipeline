"""Architecture page - 8-layer data warehouse visualization"""

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Architecture", page_icon="🏗️", layout="wide")

st.title("🏗️ 8-Layer Data Warehouse Architecture")
st.markdown("""
The pipeline follows a **classical layered data warehouse pattern**: each layer transforms
data closer to business-ready form, with clear separation of concerns.
""")

# ─────────────────────────────────────────────────────────────
# Architecture Diagram (ASCII)
# ─────────────────────────────────────────────────────────────
st.markdown("### 📐 Layer Diagram")

st.markdown("""
```
┌──────────────────────────────────────────────────────────────┐
│  8️⃣  AUDIT LAYER          audit_result (8-class checks)      │
│                            ↑                                  │
│  7️⃣  DWS LAYER (App)      dws_wide_table (38 cols)           │  ← Business Wide Table
│                            ↑                                  │
│  6️⃣  DWD LAYER (Detail)   dwd_combined_monthly                │
│                            dwd_insurance_monthly              │
│                            dwd_ways_segment_monthly           │
│                            dwd_ways_clean                     │
│                            ↑                                  │
│  5️⃣  STD LAYER (Standard) std_combined, std_insurance,        │
│                            std_ways (7-9 field PK dedup)      │
│                            ↑                                  │
│  4️⃣  DIM LAYER            dim_model_enriched (master)         │
│                            brand_model_standard_mapping       │
│                            brand_model_alias_extra            │
│                            dim_new_model_watch                │
│                            ↑                                  │
│  3️⃣  STG_INBOX (Incr)     stg_inbox_combined/insurance/ways  │  ← Monthly increment
│                            ↑                                  │
│  2️⃣  STG LAYER (History)  stg_combined/insurance/ways         │
│                            (snake_case, NULLIF normalized)    │
│                            ↑                                  │
│  1️⃣  RAW LAYER            raw_combined/insurance/ways         │  ← Excel→CSV→raw
└──────────────────────────────────────────────────────────────┘
```
""")

# ─────────────────────────────────────────────────────────────
# Layer Details
# ─────────────────────────────────────────────────────────────
st.markdown("### 🔍 Layer Details")

layer_data = [
    {
        "Layer": "1️⃣ RAW",
        "Tables": "raw_combined, raw_insurance, raw_ways",
        "Purpose": "Faithfully preserve source data; only add audit columns (batch_id, source_file, load_time)",
        "Key Principle": "Zero business transformation - any bug must be traceable",
    },
    {
        "Layer": "2️⃣ STG",
        "Tables": "stg_combined, stg_insurance, stg_ways",
        "Purpose": "Column name standardization (snake_case), type casting (VARCHAR→INT)",
        "Key Principle": "Naming consistency, no business semantic changes",
    },
    {
        "Layer": "3️⃣ STG_INBOX",
        "Tables": "stg_inbox_* (3 tables)",
        "Purpose": "Monthly increment landing zone, isolated from historical stg",
        "Key Principle": "Dual-entry pattern prevents historical pollution",
    },
    {
        "Layer": "4️⃣ DIM",
        "Tables": "dim_model_enriched, brand_model_standard_mapping, alias_extra, watch",
        "Purpose": "Master data: 1577 model_keys + 71 cleaning rules + business decisions",
        "Key Principle": "Surrogate key (model_key) decouples from business names",
    },
    {
        "Layer": "5️⃣ STD",
        "Tables": "std_combined, std_insurance, std_ways",
        "Purpose": "7-9 field PK dedup, apply 13 attribute mapping rules",
        "Key Principle": "Business idempotency (year + month + model_key + fuel...)",
    },
    {
        "Layer": "6️⃣ DWD",
        "Tables": "4 dwd_* tables",
        "Purpose": "Monthly aggregation, MIX% normalization within (model_key, fuel_type)",
        "Key Principle": "Fact-dimension separation, ready for joins",
    },
    {
        "Layer": "7️⃣ DWS",
        "Tables": "dws_wide_table (38 cols, 71,304 rows)",
        "Purpose": "Final business wide table with LRM-allocated integer volumes",
        "Key Principle": "100% volume conservation via sentinel-row pattern",
    },
    {
        "Layer": "8️⃣ AUDIT",
        "Tables": "audit_result, incremental_log",
        "Purpose": "8-class automated quality checks + full pipeline audit trail",
        "Key Principle": "Trust but verify - every layer outputs verification",
    },
]

import pandas as pd
df = pd.DataFrame(layer_data)
st.dataframe(df, hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# 4 Design Principles
# ─────────────────────────────────────────────────────────────
st.markdown("### 🎯 4 Core Design Principles")

p1, p2 = st.columns(2)

with p1:
    st.markdown("""
    #### 1. Raw Layer is Sacred
    Any bug must be traceable to raw — so raw is **never** modified
    by business logic. Only audit columns added.

    #### 2. Naming vs Aggregation Separated
    Stg layer = naming hygiene only.
    Std layer = business deduplication.
    Don't mix them — testability suffers otherwise.
    """)

with p2:
    st.markdown("""
    #### 3. Fact-Dimension Separation
    Wide tables for the business, but always backed by
    properly-normalized dim tables (model_key as foreign key).

    #### 4. Every Layer Serves the Next
    Each layer has a clear contract with the layer above.
    Test outputs in isolation; debug each layer independently.
    """)

# ─────────────────────────────────────────────────────────────
# Bonus: Sankey Data Flow
# ─────────────────────────────────────────────────────────────
st.markdown("### 🌊 Data Flow Visualization (Sankey)")

# Build a Sankey diagram showing data flow
labels = [
    "combined.csv (2,794)", "insurance.csv (2,384)", "ways.csv (4,458)",
    "stg_inbox_combined", "stg_inbox_insurance", "stg_inbox_ways",
    "std_combined (2,458)", "std_insurance (2,067)", "std_ways (4,416)",
    "dwd_combined_monthly", "dwd_insurance_monthly", "dwd_ways_segment_monthly",
    "dws_wide_table (5,560)",
    "Business Reports",
]

source = [0, 1, 2,  # raw → stg_inbox
          3, 4, 5,  # stg_inbox → std
          6, 7, 8,  # std → dwd
          9, 10, 11,  # dwd → dws
          12,  # dws → business
          ]
target = [3, 4, 5,
          6, 7, 8,
          9, 10, 11,
          12, 12, 12,
          13,
          ]
value = [2794, 2384, 4458,
         2458, 2067, 4416,
         2200, 1800, 4400,
         3000, 2000, 4416,
         5560,
         ]

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=["#667eea"] * 3 + ["#764ba2"] * 3 + ["#f093fb"] * 3 + ["#f5576c"] * 3 + ["#4facfe"] + ["#43e97b"]
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color="rgba(102, 126, 234, 0.3)"
    )
)])

fig.update_layout(title_text="Monthly Increment Data Flow (2026-03 actual numbers)", font_size=11, height=500)
st.plotly_chart(fig, use_container_width=True)
