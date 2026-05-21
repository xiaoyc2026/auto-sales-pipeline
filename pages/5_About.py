import streamlit as st

st.set_page_config(page_title="About", page_icon="👋", layout="wide")

st.title("👋 About Me")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 肖垚聪 (Yaocong Xiao)")
    st.markdown("""
    **🎓 Nanyang Technological University**  
    Singapore

    **💼 Data Engineering Intern**  
    General Motors (Shanghai)  
    Short-Term Sales Forecasting & Reporting  
    *2026.03 – 2026.06*

    ---

    **📫 Contact**
    - 📧 [yaocong001@e.ntu.edu.sg](mailto:yaocong001@e.ntu.edu.sg)
    - 💻 [github.com/xiaoyc2026](https://github.com/xiaoyc2026)

    ---

    **🛠️ Tech Stack**
    - **SQL**: MySQL 8.0 (CTE, Window Functions, LRM)
    - **Python**: pandas, openpyxl, streamlit
    - **Data Modeling**: Star schema, surrogate keys, SCD
    - **Tools**: DBeaver, Git, Excel
    """)

with col2:
    st.markdown("### 💡 What I Learned From This Project")

    with st.expander("**Lesson 1: Data engineering ≠ writing SQL**", expanded=True):
        st.markdown("""
        At first I thought my job was "write SQL to clean data". 4 months later I learned 
        data engineering is mostly about:
        
        - **Designing layers** — why do we need raw / stg / std / dwd / dws? Each has a job.
        - **Aligning with business** — the 71 mapping rules aren't SQL knowledge, they're 
          business decisions encoded into data. Designing the `apply_to_table` field 
          took 3 iterations.
        - **Defensive coding** — sentinel rows, NULL conventions, idempotent DELETE+INSERT, 
          audit trails. SQL without these breaks on month 2.
        - **Documentation** — 25 ADRs + 11 ISSUE logs. Future-me thanked past-me a hundred 
          times when picking up the project after a 2-week gap.
        """)

    with st.expander("**Lesson 2: Question your own assumptions, hard**", expanded=True):
        st.markdown("""
        My biggest bug — losing 27% of monthly volume — happened because I anchored the 
        dws JOIN on `ways` table (catalog) instead of taking a UNION of all three sources. 
        It "worked" on day 1 because I didn't compare `dws.SUM(volume) vs std.SUM(volume)`.
        
        **The fix wasn't hard. Finding it was.** Now I always:
        - Write a conservation check (SUM input = SUM output) **before** writing the INSERT
        - Pick "what's my anchor table?" as an explicit architectural decision, not an accident
        """)

    with st.expander("**Lesson 3: Make tools, not one-off scripts**", expanded=True):
        st.markdown("""
        The first month I wrote SQL files like `april_load.sql`, `may_load.sql`. 
        Every month it was 80% copy-paste and 20% bugs from forgotten replacements.
        
        Eventually I refactored into **4 parameterized templates** with `@target_year` / 
        `@target_month` at the top. Now adding a new month = changing 2 numbers and running.
        
        **Marginal cost of automation pays back in 2 months. Always.**
        """)

st.caption("Built with ❤️ using Streamlit. Code: [github.com/xiaoyc2026](https://github.com/xiaoyc2026)")
