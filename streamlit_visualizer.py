import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

BASE_URL = "http://127.0.0.1:8000/api"
st.title("📊 Employee Analytics Dashboard")

def fetch_json(path):
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"__error__": str(e)}

dept = fetch_json("/analytics/by-department/")
avg_salary = fetch_json("/analytics/avg-salary-by-department/")
gender = fetch_json("/analytics/gender-split/")
hist = fetch_json("/analytics/experience-histogram/")

if "__error__" in dept:
    st.error("Error fetching by-department: " + dept["__error__"])
else:
    if dept:
        df_dept = pd.DataFrame(list(dept.items()), columns=["department", "count"])
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(data=df_dept, x="department", y="count", ax=ax)
        ax.set_ylabel("Count")
        ax.set_xlabel("Department")
        ax.set_title("Employees by Department")
        plt.xticks(rotation=30)
        st.pyplot(fig)
    else:
        st.info("No department data available")

if "__error__" in avg_salary:
    st.error("Error fetching avg-salary-by-department: " + avg_salary["__error__"])
else:
    if avg_salary:
        df_avg = pd.DataFrame(list(avg_salary.items()), columns=["department", "avg_salary"])
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(data=df_avg, x="department", y="avg_salary", ax=ax)
        ax.set_ylabel("Average Salary")
        ax.set_xlabel("Department")
        ax.set_title("Average Salary by Department")
        plt.xticks(rotation=30)
        st.pyplot(fig)
    else:
        st.info("No average salary data available")

if "__error__" in gender:
    st.error("Error fetching gender-split: " + gender["__error__"])
else:
    if gender:
        df_gender = pd.DataFrame(list(gender.items()), columns=["gender","count"])
        fig, ax = plt.subplots(figsize=(6,4))
        ax.pie(df_gender["count"], labels=df_gender["gender"], autopct="%1.1f%%", startangle=90)
        ax.set_title("Gender Split")
        st.pyplot(fig)
    else:
        st.info("No gender split data available")

if "__error__" in hist:
    st.error("Error fetching experience-histogram: " + hist["__error__"])
else:
    if hist:
        bins = list(hist.keys())
        counts = [hist[b] for b in bins]
        df_hist = pd.DataFrame({"bin": bins, "count": counts})
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(data=df_hist, x="bin", y="count", ax=ax)
        ax.set_xlabel("Experience (years) range")
        ax.set_ylabel("Count")
        ax.set_title("Experience Distribution")
        plt.xticks(rotation=30)
        st.pyplot(fig)
    else:
        st.info("No experience histogram data available")
