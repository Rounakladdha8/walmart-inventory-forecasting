import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Walmart Sales Forecasting", layout="wide")
st.title("📈 Walmart Inventory Forecasting Dashboard")

# Load submission
submission = pd.read_csv("submission.csv")

# Split Id column to extract info
submission['Date'] = submission['Id'].apply(lambda x: x.split('_')[2])
submission['Store'] = submission['Id'].apply(lambda x: int(x.split('_')[0]))
submission['Dept'] = submission['Id'].apply(lambda x: int(x.split('_')[1]))

# Sidebar
st.sidebar.header("🔍 Options")
store_id = st.sidebar.selectbox("Select Store", sorted(submission['Store'].unique()))
dept_options = sorted(submission[submission['Store'] == store_id]['Dept'].unique())
dept_id = st.sidebar.selectbox("Select Dept", dept_options)
model_choice = st.sidebar.selectbox("Select Model", ["XGBoost", "Prophet", "Average"])

# Placeholder metrics for now (could be dynamic later)
mae = 4669.39
rmse = 5773.58
wmae = 3643.34

st.subheader("📊 Forecasting Performance")
st.metric("MAE", f"{mae:,.2f}")
st.metric("RMSE", f"{rmse:,.2f}")
st.metric("WMAE", f"{wmae:,.2f}")

# Filter forecasted data
filtered = submission[(submission['Store'] == store_id) & (submission['Dept'] == dept_id)]

# Plot
st.subheader("📅 Forecasted Weekly Sales")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(filtered['Date'], filtered['Weekly_Sales'], marker='o', label=f'{model_choice} Forecast')
ax.set_title(f"Store {store_id} - Dept {dept_id} ({model_choice})")
ax.set_xlabel("Date")
ax.set_ylabel("Weekly Sales")
ax.tick_params(axis='x', rotation=45)
ax.legend()
st.pyplot(fig)

# Download
st.subheader("📥 Download Submission")
st.download_button("Download CSV", submission.to_csv(index=False), "submission.csv")
