"""LRM Algorithm Playground - the technical highlight"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="LRM Algorithm", page_icon="🎯", layout="wide")

st.title("🎯 Largest Remainder Method (LRM) — Interactive Playground")
st.markdown("""
**The Problem**: How do you allocate an integer sales volume across N trim variants
based on their MIX% (market share), while guaranteeing the sum equals the original volume?

This is the **core technical highlight** of the project. Play with it below ↓
""")

# ─────────────────────────────────────────────────────────────
# The Problem
# ─────────────────────────────────────────────────────────────
with st.expander("📚 Why is this hard? (Click to expand)", expanded=False):
    st.markdown("""
    **Naive approach**: `volume_trim = volume_total * mix_pct`

    Problem: This gives floats (e.g., 1234.7 cars sold). Business wants integers.

    **Naive rounding**: `ROUND(volume * mix%)` — but `ROUND(1.5) + ROUND(1.5) + ROUND(1.5) = 6`,
    while total should be 4.5 → off by 1.5!

    **LRM solution**:
    1. Take FLOOR of each ideal allocation
    2. Calculate "remainder" = total - SUM(floors)
    3. Sort by fractional part DESC
    4. Distribute the remainder by giving +1 to top-K trims by fractional part

    **Guarantee**: SUM(allocations) = original volume, ALWAYS.
    """)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Interactive Playground
# ─────────────────────────────────────────────────────────────
st.markdown("### 🎮 Try it Yourself")

c1, c2 = st.columns([1, 2])

with c1:
    st.markdown("#### Inputs")
    total_volume = st.number_input("Total Combined Volume (cars sold)", 
                                    min_value=100, max_value=100000, 
                                    value=12345, step=100)

    num_trims = st.slider("Number of Trims", min_value=2, max_value=8, value=5)

    st.markdown("**MIX% for each trim** (will be normalized to sum=1)")
    mixes = []
    for i in range(num_trims):
        default_val = round(1.0 / num_trims, 3) + (0.1 if i == 0 else -0.02)
        mix = st.slider(f"Trim {i+1} MIX",
                        min_value=0.0, max_value=1.0,
                        value=max(0.01, default_val),
                        step=0.01,
                        key=f"mix_{i}")
        mixes.append(mix)

    # Normalize
    mix_sum = sum(mixes)
    mix_normalized = [m / mix_sum for m in mixes]

with c2:
    st.markdown("#### LRM Allocation Result")

    # Compute LRM
    ideal = [total_volume * m for m in mix_normalized]
    floors = [int(np.floor(x)) for x in ideal]
    fracs = [x - np.floor(x) for x in ideal]
    floor_sum = sum(floors)
    remainder = total_volume - floor_sum

    # Rank trims by fractional part (highest gets +1 first)
    rank_indices = sorted(range(num_trims), key=lambda i: -fracs[i])
    allocations = floors.copy()
    for i in range(remainder):
        allocations[rank_indices[i]] += 1

    df = pd.DataFrame({
        "Trim": [f"Trim {i+1}" for i in range(num_trims)],
        "MIX% (normalized)": [f"{m:.4f}" for m in mix_normalized],
        "Ideal (float)": [f"{x:.4f}" for x in ideal],
        "FLOOR": floors,
        "Fractional Part": [f"{f:.4f}" for f in fracs],
        "Rank by Fraction": [rank_indices.index(i) + 1 for i in range(num_trims)],
        "+1 Bonus?": ["✅" if rank_indices.index(i) < remainder else "" for i in range(num_trims)],
        "🎯 LRM Final": allocations,
    })

    st.dataframe(df, hide_index=True, use_container_width=True)

    # Conservation check
    alloc_sum = sum(allocations)
    if alloc_sum == total_volume:
        st.success(f"✅ **Conservation verified**: SUM(allocations) = {alloc_sum} = {total_volume} (input)")
    else:
        st.error(f"❌ Conservation broken: {alloc_sum} ≠ {total_volume}")

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────────────────────────
st.markdown("### 📊 Visual Comparison: Ideal vs LRM vs Naive Rounding")

naive = [round(x) for x in ideal]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[f"Trim {i+1}" for i in range(num_trims)],
    y=ideal,
    name='Ideal (float)',
    marker_color='lightgray',
    text=[f"{x:.2f}" for x in ideal],
    textposition='outside',
))

fig.add_trace(go.Bar(
    x=[f"Trim {i+1}" for i in range(num_trims)],
    y=naive,
    name=f'Naive ROUND (sum={sum(naive)})',
    marker_color='#ffa07a',
    text=naive,
    textposition='outside',
))

fig.add_trace(go.Bar(
    x=[f"Trim {i+1}" for i in range(num_trims)],
    y=allocations,
    name=f'🎯 LRM (sum={alloc_sum})',
    marker_color='#667eea',
    text=allocations,
    textposition='outside',
))

fig.update_layout(
    barmode='group',
    title=f"Total Volume: {total_volume:,} | LRM guarantees exact total, naive does not",
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# SQL Implementation
# ─────────────────────────────────────────────────────────────
st.markdown("### 💻 The Actual MySQL Implementation")

st.markdown("This runs in production every month on 71,304 rows in < 5 seconds:")

st.code("""
WITH lrm AS (
  SELECT *,
    FLOOR(combined_vol * mix_normalized_seg) AS cb_floor,
    combined_vol * mix_normalized_seg - 
      FLOOR(combined_vol * mix_normalized_seg) AS cb_frac
  FROM joined_buckets
),
ranked AS (
  SELECT *,
    SUM(cb_floor) OVER bk AS cb_floor_sum,
    ROW_NUMBER() OVER (
      PARTITION BY year,month,model_key,fuel_type,pv_cv,segment,domestic_import
      ORDER BY cb_frac DESC, trim_en, model_year_key
    ) AS cb_rank
  FROM lrm
  WINDOW bk AS (
    PARTITION BY year,month,model_key,fuel_type,pv_cv,segment,domestic_import
  )
)
SELECT *,
  cb_floor + CASE 
    WHEN cb_rank <= (combined_vol - cb_floor_sum) THEN 1 
    ELSE 0 
  END AS volume_combined  -- ← Final integer allocation
FROM ranked;
""", language="sql")

st.info("""
**Why LRM and not naive ROUND?**
- Naive `ROUND` can drift by ±N where N = number of trims (e.g., 5 trims = ±5 cars/month error)
- Across 1,939 buckets × 12 months = potentially 100K+ car miscounting per year
- LRM guarantees **0 drift, forever**
- This is a textbook algorithm (used in apportioning legislative seats — "Hamilton's method")
""")
