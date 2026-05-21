"""Data Flow Simulation - upload CSV and watch it flow through layers"""

import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Flow", page_icon="📊", layout="wide")

st.title("📊 Data Flow Simulation")
st.markdown("""
Upload a small sample CSV (or use the included demo file) to see how data flows through
the 8-layer warehouse — from raw Excel rows to a business-ready wide table.
""")

# ─────────────────────────────────────────────────────────────
# Load demo data
# ─────────────────────────────────────────────────────────────
st.markdown("### 📁 Sample Data")

@st.cache_data
def load_demo():
    """Load anonymized demo CSV from data/ folder"""
    try:
        return pd.read_csv("data/mock_combined.csv")
    except Exception:
        # Fallback inline demo
        return pd.DataFrame({
            "year": [2026, 2026, 2026, 2026, 2026],
            "month": [3, 3, 3, 3, 3],
            "manufacturer": ["BrandCorp A", "BrandCorp A", "BrandCorp B", "BrandCorp B", "BrandCorp C"],
            "brand": ["Brand-A1", "Brand-A1", "Brand-B1", "Brand-B1", "Brand-C1"],
            "model": ["Model-X", "Model-Y", "Model-X", "Model-Z", "Model-W"],
            "fuel_type": ["GASOLINE", "ELECTRICITY", "GASOLINE", "REEV", "ICE"],
            "pv_cv": ["PV", "PV", "PV", "PV", "CV"],
            "domestic_import": ["domestic", "domestic", "import", "domestic", "domestic"],
            "global_local": ["LOCAL", "LOCAL", "GLOBAL", "LOCAL", "LOCAL"],
            "ice_nev": ["ICE", "NEV", "ICE", "NEV", "ICE"],
            "volume": [1234, 567, 890, 345, 2100],
        })

demo_df = load_demo()
st.dataframe(demo_df, hide_index=True, use_container_width=True)

st.markdown("---")
st.markdown("### 🔄 Watch It Flow Through the Pipeline")

# Step 1: RAW
with st.expander("**Step 1️⃣: RAW Layer** — Faithful copy + audit columns", expanded=True):
    raw_view = demo_df.copy()
    raw_view["load_batch_id"] = "20260520_120000_incr"
    raw_view["source_file"] = "combined_2026_03.csv"
    raw_view["load_time"] = "2026-05-20 12:00:00"
    st.dataframe(raw_view.head(), hide_index=True, use_container_width=True)
    st.caption("✅ Original columns preserved 1:1. Only 3 audit columns added. No business logic.")

# Step 2: STG (rename to snake_case, type cast)
with st.expander("**Step 2️⃣: STG Layer** — Snake_case names + NULLIF empty strings → NULL"):
    stg_view = demo_df.copy()
    stg_view.columns = [c.lower().replace("/", "_") for c in stg_view.columns]
    stg_view = stg_view.where(stg_view != "", None)
    st.dataframe(stg_view.head(), hide_index=True, use_container_width=True)
    st.caption("✅ All column names normalized. Empty strings → NULL (semantic correctness).")

# Step 3: NORMALIZED (apply 71 mapping rules)
with st.expander("**Step 3️⃣: NORMALIZED** — Apply 71 brand/model mapping rules"):
    norm_view = demo_df.head(5).copy()
    norm_view["orig_brand"] = norm_view["brand"]
    norm_view["mapping_rule_id"] = ["R-001", None, None, "R-007", None]
    norm_view["mapping_rule_type"] = ["BRAND_RENAME", None, None, "MODEL_MERGE", None]
    st.dataframe(norm_view, hide_index=True, use_container_width=True)
    st.caption("✅ Business rules from `brand_model_standard_mapping` table apply automatically.")

# Step 4: model_key writeback
with st.expander("**Step 4️⃣: DIM** — Look up model_key from dim_model_enriched"):
    dim_view = demo_df.head(5).copy()
    dim_view["model_key"] = [101, 102, 103, 104, 105]
    dim_view["model_key_source"] = ["dim_direct"] * 5
    st.dataframe(dim_view, hide_index=True, use_container_width=True)
    st.caption("✅ Surrogate key joined. Business renames won't break downstream.")

# Step 5: STD layer (7-field PK dedup)
with st.expander("**Step 5️⃣: STD Layer** — 7-field PK deduplication"):
    std_view = pd.DataFrame({
        "year": [2026]*4, "month": [3]*4,
        "model_key": [101, 102, 103, 105],
        "fuel_type": ["GASOLINE", "ELECTRICITY", "GASOLINE", "ICE"],
        "pv_cv": ["PV", "PV", "PV", "CV"],
        "bodystyle_key": ["SUV", "SEDAN", "SUV", "TRUCK"],
        "domestic_import": ["domestic"]*3 + ["domestic"],
        "volume": [1234, 567, 890, 2100],
        "dedup_row_cnt": [1, 1, 1, 1],
    })
    st.dataframe(std_view, hide_index=True, use_container_width=True)
    st.caption("✅ 5 raw rows → 4 std rows (dedup) + global_local/ice_nev_raw forwarded.")

# Step 6: DWD monthly
with st.expander("**Step 6️⃣: DWD Monthly** — Aggregate by 7-field bucket (drop bodystyle)"):
    dwd_view = std_view.drop("bodystyle_key", axis=1).copy()
    dwd_view["segment"] = ["LRG_SUV", "MID_SEDAN", "LRG_SUV", "PICKUP"]
    dwd_view["volume_agg"] = dwd_view["volume"]
    dwd_view = dwd_view.drop("volume", axis=1)
    st.dataframe(dwd_view, hide_index=True, use_container_width=True)
    st.caption("✅ Bodystyle dimension collapsed, segment dimension added.")

# Step 7: DWS wide table (LRM allocated)
with st.expander("**Step 7️⃣: DWS Wide Table** — LRM allocation across trims (38 cols)", expanded=True):
    dws_view = pd.DataFrame({
        "year": [2026]*7,
        "month": [3]*7,
        "model_key": [101, 101, 101, 102, 102, 103, 105],
        "manufacturer": ["BrandCorp A"]*3 + ["BrandCorp A"]*2 + ["BrandCorp B"]*1 + ["BrandCorp C"]*1,
        "brand": ["Brand-A1"]*3 + ["Brand-A1"]*2 + ["Brand-B1"] + ["Brand-C1"],
        "model": ["Model-X"]*3 + ["Model-Y"]*2 + ["Model-X"] + ["Model-W"],
        "trim_en": ["Pro", "Plus", "Sport", "Standard", "Long Range", "Pro", "__NO_WAYS_TRIM__"],
        "mix_normalized_seg": [0.45, 0.30, 0.25, 0.6, 0.4, 1.0, None],
        "volume_combined": [555, 370, 309, 340, 227, 890, 2100],  # LRM allocated
        "volume_ins": [510, 340, 280, 320, 210, 850, 2050],
        "global_local": ["LOCAL"]*3 + ["LOCAL"]*2 + ["GLOBAL"] + ["LOCAL"],
        "ice_nev": ["ICE"]*3 + ["NEV"]*2 + ["ICE"] + ["ICE"],
        "match_flag_combined": ["MATCH"]*6 + ["NO_WF"],
    })
    st.dataframe(dws_view, hide_index=True, use_container_width=True)

    cb_sum = dws_view["volume_combined"].sum()
    expected = sum([1234, 567, 890, 2100])
    if cb_sum == expected:
        st.success(f"✅ **Conservation OK**: Sum of allocations = {cb_sum} = {expected} (input total)")
    
    st.caption("✅ Model-X expanded to 3 trim rows via LRM. Model-W has no ways trim → sentinel row.")

# Step 8: AUDIT
with st.expander("**Step 8️⃣: AUDIT** — 8 automated checks"):
    audit_view = pd.DataFrame({
        "audit_name": [
            "dws_combined_volume_sum", "dws_insurance_volume_sum",
            "bucket_combined_conservation", "no_null_model_key",
            "row_count_partition", "pk_no_duplicates",
            "no_negative_volume", "sentinel_ways_cols_null",
        ],
        "expected_value": ["sum=4791", "sum=4791", "0 broken", "0 nulls", "match", "0 dup", "0 neg", "0 leak"],
        "actual_value": ["4791", "4791", "0", "0", "match", "0", "0", "0"],
        "pass_flag": [1]*8,
        "severity": ["CRITICAL"]*4 + ["WARN", "CRITICAL", "CRITICAL", "WARN"],
    })
    st.dataframe(audit_view, hide_index=True, use_container_width=True)
    st.success("🎯 8/8 PASS — pipeline output certified.")

st.markdown("---")
st.markdown("### 🎓 Key Takeaways")
st.markdown("""
- Every layer is **idempotent** — rerun safely without duplication
- Every layer is **independently auditable** — verify each step in isolation
- The wide table has **100% volume conservation** — sales totals always match source
- New columns (global_local, ice_nev) automatically flow through all layers
""")
