# ⚕️ Medical Cost Analytics: Demographic Risk & Decision Support

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](Link-to-your-live-app-if-deployed)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

An interactive web application built with Streamlit to visualize and analyze medical insurance costs. This dashboard allows users to explore how demographic factors (such as age, BMI, and smoking status) correlate with medical charges, providing actionable insights for underwriting risk assessment.

*Developed by: Chen Shmeltz & Eli Titiyevsky*

---

## 📸 Dashboard Sneak Peek
<img width="1277" height="671" alt="Analytics" src="https://github.com/user-attachments/assets/92874c96-2345-4bd4-a3eb-f38f6683af89" />


---

## ✨ Key Features
* **Dynamic Demographic Filtering:** Slice the dataset in real-time by Gender, Age Range, and Geographic Region.
* **Deep Risk Exploration (Tabbed Interface):**
  * **Cost Distribution:** Compare the cost distribution of your filtered segment against the total population.
  * **Risk Correlation:** Scatter plots mapping BMI and smoking status against total charges, complete with obesity thresholds.
  * **Family Impact:** Dual-axis charts analyzing the relationship between the number of children, smoking prevalence, and average costs.
  * **Correlation Matrix:** A dynamic heatmap showing the statistical relationships between all numerical variables.
* **KPI Benchmarking:** Real-time metrics (Avg Cost, Avg BMI, Smoker Rate) that automatically calculate deviations against the global dataset averages.
* **Data Export:** Securely download the filtered demographic segments as a CSV for offline analysis.

---

## 🛠️ Tech Stack
* **Framework:** Streamlit
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Seaborn, Matplotlib

---

## 🚀 How to Run Locally

1. pip install -r requirements.txt
2. py -m streamlit run Final.py
