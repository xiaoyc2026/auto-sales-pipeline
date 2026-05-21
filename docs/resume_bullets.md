# 📄 Resume Bullets — Copy/Paste Ready

Choose the version that fits your resume style. All numbers based on real project metrics.

## ─────────────────────────────────────────────
## 🎯 Version A: Concise (4 bullets, ~80 words)
## ─────────────────────────────────────────────

**Data Engineering Intern | Auto Sales Data Governance | Jan-May 2026**
- Designed & shipped an 8-layer MySQL data warehouse (18 tables) compressing a 1-2 day manual Excel workflow into a 30-min automated pipeline serving 71,304-row business wide table at 99.92% data coverage
- Implemented Largest Remainder Method (LRM) in pure SQL window functions guaranteeing 100% integer volume conservation across 1,939 buckets × 12 months
- Discovered & fixed a critical 27% data loss bug (504,955 cars/month) via sentinel-row pattern; restructured wide table to bucket-union design
- Authored 25 architectural decision records + 200+ KB handoff documentation enabling smooth tech transfer to software engineering team

## ─────────────────────────────────────────────
## 🎯 Version B: Detailed (6-7 bullets, ~140 words)
## ─────────────────────────────────────────────

**Data Engineering Intern · Short-Term Sales Forecasting Team | Fortune-50 Automaker | Jan-May 2026**

- Sole engineer on a 5-month data governance + monthly pipeline project; designed full 8-layer MySQL warehouse (RAW → STG → DIM → STD → DWD → DWS → AUDIT) across 18 tables
- Wrote 1,700+ lines of production MySQL SQL using advanced features (CTEs, window functions, BINARY operators, idempotent UPSERTs); 3 Python ETL adapters (pandas + openpyxl)
- Implemented LRM (Largest Remainder Method) apportionment algorithm in pure MySQL for integer sales volume allocation across trim variants, guaranteeing 100% conservation
- Discovered and fixed a critical wide-table bug causing silent 27% volume loss (504K cars/month); restructured to bucket-union + sentinel-row pattern that doubled as business-value to-do list
- Created data-driven business rules system: 71 brand/model standardization rules in `brand_model_standard_mapping` table eliminated need for developer involvement in rule changes
- Co-designed 4-bucket new-model triage workflow (APPROVE/MERGE/DEFER/REJECT) with business analysts; cut analyst review time 70%
- Authored 25 architectural decision records, 11 issue logs, and 200+ KB of handoff documentation for software engineering team productionization

## ─────────────────────────────────────────────
## 🎯 Version C: Story-driven (for cover letter)
## ─────────────────────────────────────────────

I joined as the sole data engineering intern on a project to automate a Fortune-50 automaker's monthly sales reporting workflow. What I inherited was a 1-2 day manual Excel exercise riddled with brand-naming inconsistencies and zero audit trail. What I shipped 5 months later was a complete 8-layer MySQL data warehouse — 18 tables, 71,304-row business wide table, 99.92% data coverage, 100% volume conservation via a Largest Remainder Method algorithm I implemented in pure SQL window functions.

Along the way I discovered (and fixed) a critical bug causing 27% silent data loss in the wide table — solved by introducing a "sentinel-row" pattern that doubled as a business-value to-do list. I co-designed a 4-bucket new-model triage workflow with business analysts that cut their review time 70%. And I documented all 25 architectural decisions + 11 issues + 16 engineering lessons in 200+ KB of handoff docs so the software engineering team could take over productionization without me.

The biggest lesson? Trust no tool's defaults — measure everything. The most invisible bugs (like that 27%) only surface when you build explicit conservation checks. Pipelines can run flawlessly and silently produce wrong numbers.

## ─────────────────────────────────────────────
## 🎯 Version D: Tech keywords (for ATS/recruiter scan)
## ─────────────────────────────────────────────

**Tech Used:** MySQL 8.0 · Python 3 · pandas · openpyxl · CTE · Window Functions · LRM Algorithm · Apportionment · Surrogate Keys · Star/Snowflake Schema · Slowly Changing Dimensions · Idempotent Pipelines · Data Quality / Audit Framework · Sentinel Rows · Streamlit · Git/GitHub

**Domain:** Automotive · Sales Forecasting · Master Data Management (MDM) · Data Governance · ETL · Data Warehousing · Business Intelligence

**Soft Skills:** Cross-functional collaboration · Technical documentation · Decision records (ADR) · Cross-team handoff · Self-directed work · Business + Tech translation

