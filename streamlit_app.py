"""
🚗 Auto Sales Data Governance & Monthly Incremental Pipeline
Portfolio Demo - by Yaocong Xiao (肖垚聪)

Run locally:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

Deploy:
    Push to GitHub → streamlit.io/cloud → Connect repo → Deploy
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Auto Sales Data Governance | Portfolio",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        padding-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Hero Section
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🚗 Auto Sales Data Governance Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">A Production Data Warehouse Project for a Fortune-50 Automaker | Short-Term Sales Forecasting Team</div>', unsafe_allow_html=True)

st.markdown("""
> **A data engineering intern designed and shipped a full data governance + monthly incremental pipeline
> that compressed a 1-2 day manual Excel workflow into a 30-minute automated SQL pipeline.**
""")

# ─────────────────────────────────────────────────────────────
# Key Metrics
# ─────────────────────────────────────────────────────────────
st.markdown("### 📊 Project at a Glance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="stat-number">8</div>
        <div class="stat-label">Data Layers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="stat-number">18</div>
        <div class="stat-label">Tables Designed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="stat-number">71,304</div>
        <div class="stat-label">Wide Table Rows</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="stat-number">99.92%</div>
        <div class="stat-label">Data Coverage</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Quick Tour
# ─────────────────────────────────────────────────────────────
st.markdown("### 🧭 Take the Tour (5 min)")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    #### 🏗️ Architecture
    Explore the 8-layer data warehouse design — from raw Excel uploads
    to a 38-column business wide table.

    👉 Sidebar → **Architecture**
    """)

with c2:
    st.markdown("""
    #### 🎯 LRM Algorithm
    Interactive playground for the **Largest Remainder Method** —
    how I allocate integer sales volumes across trim variants while
    guaranteeing 100% volume conservation.

    👉 Sidebar → **LRM Playground**
    """)

with c3:
    st.markdown("""
    #### 🧠 Decisions
    25 architectural decisions documented:
    surrogate keys, mapping rules as data,
    business sentinels, etc.

    👉 Sidebar → **Decisions**
    """)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# The Problem → Solution
# ─────────────────────────────────────────────────────────────
st.markdown("### 💡 The Problem & Solution")

p1, p2 = st.columns(2)

with p1:
    st.markdown("""
    #### 😣 Before (Manual)
    - Analyst manually opens **3 Excel files** every month
    - Hand-aligns brand/model names across sources
    - **No version control, no audit trail**
    - 1-2 days work per month, error-prone
    - Reports inconsistent between team members
    """)

with p2:
    st.markdown("""
    #### 🚀 After (This Project)
    - **3 Python adapters** standardize raw Excel → CSV
    - **MySQL pipeline** in 11 SQL steps (raw → dws)
    - **Automated audit** with 8-class data quality checks
    - **30 min** end-to-end per month
    - **100% reproducible**, full audit trail in `incremental_log`
    """)

st.markdown("---")

# ─────────────────────────────────────────────────────────────
# Tech Stack
# ─────────────────────────────────────────────────────────────
st.markdown("### 🛠️ Tech Stack")

tech = pd.DataFrame({
    "Layer": ["Ingestion", "Storage", "Transformation", "Quality", "Documentation"],
    "Tools": [
        "Python (pandas, openpyxl) — 3 adapters for Excel→CSV",
        "MySQL 8.0.45 (utf8mb4_0900_ai_ci)",
        "Pure SQL (CTEs, window functions, LRM algorithm)",
        "8-class audit_result framework (conservation, completeness, range)",
        "200+ KB Markdown docs, 25 decision records, 11 issue logs",
    ],
})
st.dataframe(tech, hide_index=True, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# About Me / Contact
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 👋 About This Project")

st.markdown("""
**Role**: Data Engineering Intern · Short-Term Sales Forecasting & Reporting

**Duration**: 3 months (Mar-Jun 2026)

**My Contributions**:
- 🏗️ Designed full 8-layer data warehouse from scratch
- 📐 Defined 25 architectural decisions (PK design, mapping rule strategy, etc.)
- 💻 Wrote 1,700+ lines of production MySQL SQL
- 🐛 Discovered & fixed 11 data quality issues (incl. critical 27% volume loss bug)
- 📚 Authored complete handoff documentation (READMEs, SOPs, decision logs)
- 🤝 Cross-functional collaboration with business analysts (4-bucket new-model triage)

**Key Technical Highlights**:
- LRM integer allocation algorithm with 100% conservation guarantee
- Sentinel-row pattern to prevent 27% data loss in wide table
- Business rules-as-data (71 mapping rules in MySQL, not hardcoded)
- Surrogate key strategy to handle business renames without data migration

📧 Contact: yaocong.xiao@gm.com
🔗 Code: github.com/xiaoyc026/auto-sales-pipeline
""")

st.markdown("---")
st.caption("⚠️ This demo uses anonymized data. Original project handled confidential GM sales data.")
