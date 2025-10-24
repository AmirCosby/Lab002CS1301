# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.
import ast

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    csv_data = pd.read_csv("data.csv")
    st.dataframe(csv_data)  
else:
    st.error("Couldn't find the CSV file.")
    csv_data = None

# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.
if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
    with open("data.json") as w:
        json_data = json.load(w) #NEW
    st.json(json_data) #NEW
else:
    st.error("The 'data.json' file is missing or empty.")
    json_data = None




# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Static: Average Phone Usage per day") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.

st.subheader("Static: Average Phone Usage per Day")

if csv_data is not None:
    if "Value" in csv_data.columns:
        csv_data["Value"] = csv_data["Value"].apply(ast.literal_eval)
        expanded = pd.DataFrame(csv_data["Value"].to_list())
        avg_usage = expanded.mean().reset_index()
        avg_usage.columns = ["Day", "Average Hrs"]

        st.bar_chart(data=avg_usage, x="Day", y="Average Hrs")

    else:
        st.warning("Error")
else:
    st.warning("Can't find CSV data.")


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Dynamic: Compare two days") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
# ===== GRAPH 2: Compare two days =====
df = pd.read_csv("data.csv")
parsed = []
for v in df["Value"]:
    try:
        d = v if isinstance(v, dict) else ast.literal_eval(str(v)) #NEW
    except Exception:
        d = {}
    parsed.append(d)

days_df = pd.DataFrame(parsed).apply(pd.to_numeric, errors="coerce") #NEW
day_cols = [c for c in ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"] if c in days_df.columns]

if len(day_cols) < 2:
    st.error("Need at least two weekday colums")
else:
    c1, c2 = st.columns(2)
    with c1:
        d1 = st.selectbox("Select Day 1", day_cols, index=0, key="g2_d1")
    with c2:
        d2 = st.selectbox("Select Day 2", [d for d in day_cols if d != d1], index=0, key="g2_d2")

    mean1 = days_df[d1].mean()
    mean2 = days_df[d2].mean()
    compare_df = pd.DataFrame({"Day": [d1, d2], "Average Hours": [mean1, mean2]})

    st.bar_chart(compare_df.set_index("Day"))
    st.caption(f"Average phone usage: {d1} vs {d2}.")
# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Dynamic") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.
df = pd.read_csv("data.csv")

# Parse the dict stored as a string in the Value column
rows = []
for v in df["Value"]:
    if isinstance(v, str):
        try:
            rows.append(ast.literal_eval(v))
        except Exception:
            rows.append({})
    elif isinstance(v, dict):
        rows.append(v)
    else:
        rows.append({})

days_df = pd.DataFrame(rows)  # columns: Sunday..Saturday
mean_usage = days_df.mean(numeric_only=True)

if mean_usage.empty:
    st.error("No numeric day data found.")
else:
    low = mean_usage.idxmin() #NEW
    high = mean_usage.idxmax()
    out = pd.DataFrame({"Day": [low, high],
                        "Average Hours": [mean_usage[low], mean_usage[high]]})
    st.bar_chart(out.set_index("Day"))
    st.caption(f"Lowest: {low} ({mean_usage[low]:.2f} h). Highest: {high} ({mean_usage[high]:.2f} h).")
