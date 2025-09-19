import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil

st.set_page_config(page_title="Employees Analytics", layout="wide")
st.title("📈 Employee Analytics Visualizer")

col1, col2 = st.columns([2, 1])
with col1:
    base_url = st.text_input("API Base URL", value="http://127.0.0.1:8000")
    api_prefix = st.text_input("API prefix", value="/api")
with col2:
    token = st.text_input("Token (optional)", type="password")
    use_token = bool(token)

def headers():
    h = {"Accept": "application/json"}
    if use_token:
        h["Authorization"] = f"Token {token}"
    return h

dept_counts_url = f"{base_url.rstrip('/')}{api_prefix}/analytics/dept-counts/"
avg_perf_url = f"{base_url.rstrip('/')}{api_prefix}/analytics/avg-perf-by-dept/"
employees_url = f"{base_url.rstrip('/')}{api_prefix}/employees/"

st.markdown("---")
st.header("Department counts")
try:
    r = requests.get(dept_counts_url, headers=headers(), timeout=10)
    if r.status_code == 200:
        dept_data = pd.DataFrame(r.json())
        if not dept_data.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(data=dept_data, x="department", y="count", ax=ax)
            ax.set_title("Employees per Department")
            ax.set_xlabel("")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            st.subheader("Raw data")
            st.dataframe(dept_data)
        else:
            st.info("No department data returned.")
    else:
        st.error(f"Failed to fetch department counts: {r.status_code} — {r.text}")
except Exception as e:
    st.error(f"Error fetching department counts: {e}")

st.markdown("---")
st.header("Average Performance by Department")
try:
    r = requests.get(avg_perf_url, headers=headers(), timeout=10)
    if r.status_code == 200:
        perf_data = pd.DataFrame(r.json())
        if not perf_data.empty:
            perf_data = perf_data.sort_values("avg_score", ascending=False)
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            sns.barplot(data=perf_data, x="department", y="avg_score", ax=ax2)
            ax2.set_title("Avg Performance Score by Department")
            ax2.set_xlabel("")
            ax2.set_ylabel("Avg Score")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
            st.subheader("Raw data")
            st.dataframe(perf_data)
        else:
            st.info("No performance data returned.")
    else:
        st.error(f"Failed to fetch avg performance: {r.status_code} — {r.text}")
except Exception as e:
    st.error(f"Error fetching avg performance: {e}")

st.markdown("---")
st.header("Employees list (paginated)")

dept_filter = st.selectbox("Filter by department",
                           options=["(all)"] + list(dept_data["department"]) if 'dept_data' in locals() and not dept_data.empty else ["(all)"])
per_page = st.selectbox("Per page", [5, 10, 20, 50], index=1)
params = {"page": 1, "per_page": per_page}
if dept_filter and dept_filter != "(all)":
    params["department"] = dept_filter
page = st.number_input("Page", min_value=1, value=1, step=1)
params["page"] = page

try:
    r = requests.get(employees_url, headers=headers(), params=params, timeout=10)
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, dict) and "results" in data:
            results = pd.DataFrame(data["results"])
            total = data.get("count", None)
        elif isinstance(data, list):
            results = pd.DataFrame(data)
            total = None
        else:
            results = pd.DataFrame([data]) if data else pd.DataFrame()
            total = None

        if not results.empty:
            st.subheader(f"Employees (page {page})")
            cols_to_show = [c for c in ["id", "first_name", "last_name", "email", "department", "role", "salary", "date_of_joining"] if c in results.columns]
            st.dataframe(results[cols_to_show].fillna(""), height=300)
            if total:
                total_pages = ceil(total / per_page)
                st.caption(f"Showing page {page} of {total_pages} — total employees: {total}")
        else:
            st.info("No employees found for these filters.")
    else:
        st.error(f"Failed to fetch employees: {r.status_code} — {r.text}")
except Exception as e:
    st.error(f"Error fetching employees: {e}")

