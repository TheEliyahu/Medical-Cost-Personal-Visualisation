# Submitted by Eli Titiyevsky: 314654310 and Chen Shmeltz:207268012

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['axes.facecolor'] = '#f7f9fc'
plt.rcParams['figure.facecolor'] = '#f7f9fc'
from matplotlib.ticker import FuncFormatter



st.set_page_config(page_title="Medical Cost Analytics", page_icon="⚕️", layout="wide")
st.markdown("""<style>  div[data-testid="stTabs"] button {  font-size: 16px;  padding: 10px 20px;  }</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('insurance.csv')
    return df

df = load_data()

def format_k(x, pos):
    """Formats numbers like 10000 to 10K"""
    return f'{int(x/1000)}K'


st.markdown("<h1 style='text-align: center;'>Medical Cost Analytics: Demographic Risk & Decision Support</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Submitted  By: Chen Shmeltz and Eli Titiyevsky</h5>", unsafe_allow_html=True)
st.divider()


# Sidebar Header and Logo
st.sidebar.image("images\logo - witho bg.png", use_container_width=True)

st.sidebar.markdown("<h2 style='text-align: center; font-weight: bold; '>Filter Menu</h2>", unsafe_allow_html=True)
st.sidebar.divider() # Adds a clean line to separate branding from filters

# Gender Selection
st.sidebar.markdown("<h3 style='text-align: center;'>Gender Selection</h3>", unsafe_allow_html=True)
sex = st.sidebar.selectbox("Gender", ["All", "male", "female"], label_visibility="collapsed")
st.sidebar.divider() 

if sex == "All":
    filtered_df = df
else:
    filtered_df = df[df['sex'] == sex]
    
# Age Range Selection
st.sidebar.markdown("<h3 style='text-align: center;'>Age Range</h3>", unsafe_allow_html=True)
age_range = st.sidebar.slider("Age", int(df['age'].min()), int(df['age'].max()), (18, 64), label_visibility="collapsed")
st.sidebar.divider() 

# Regions Selection
st.sidebar.markdown("<h3 style='text-align: center;'>Region Selection</h3>", unsafe_allow_html=True)
regions = st.sidebar.multiselect("Regions", options=df['region'].unique(), default=df['region'].unique(), label_visibility="collapsed")
st.sidebar.divider() 

# Filter by Age and Region
filtered_df = filtered_df[
    (filtered_df['age'].between(age_range[0], age_range[1])) &
    (filtered_df['region'].isin(regions))
]

# Download Button
st.sidebar.markdown("<h3 style='text-align: center;'>Export Data</h3>", unsafe_allow_html=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button( label="📥 Download Data (CSV)", data=csv, file_name='underwriting_analysis.csv', mime='text/csv',use_container_width=True)
st.sidebar.divider() 

refresh_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
st.sidebar.markdown(f"""<div style="text-align: center; color: gray; font-size: 0.8rem;">Last data refresh: {refresh_time}</div>""", unsafe_allow_html=True)


left_col, divider_col, right_col = st.columns([1, 0.02, 1])

ticks = np.arange(0, 65000, 10000) 


with left_col:
    st.markdown("<h4 style='text-align: center;'>Deep Risk Exploration</h4>", unsafe_allow_html=True)
    st.markdown("""<style> button[data-baseweb="tab"] {margin: 0 auto;} div[data-testid="stTabs"] > div:first-child {justify-content: center;}</style>""", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Cost Distribution", "BMI/Smoke/Cost Correlation", "Children Analysis", "Risk Correlation Matrix"])

    with tab1:        
        fig_hist, ax_hist = plt.subplots(figsize=(6,5))
        sns.histplot(df['charges'], color='gray', element="step", fill=True, alpha=0.3, label='Total Population', ax=ax_hist, kde=True, linewidth=0)
        sns.histplot(filtered_df['charges'], color='#3498db', element="step", fill=True, alpha=0.6, label='Filtered Segment', ax=ax_hist, kde=True, linewidth=0)
        ax_hist.spines[['top','right']].set_visible(False)
        ax_hist.xaxis.set_major_formatter(FuncFormatter(format_k))
        ax_hist.grid(axis='y', alpha=0.3)
        ax_hist.set_xticks(ticks)
        ax_hist.set_xlim(left=0, right=65000)
        ax_hist.set_xlabel("Charges ($)")
        ax_hist.set_ylabel("Number of People")
        ax_hist.legend()
        
        st.pyplot(fig_hist)
        plt.close(fig_hist)

    with tab2:
        fig_scatter, ax_sc = plt.subplots(figsize=(6,5))
        sns.scatterplot(data=filtered_df, x='bmi', y='charges', hue='smoker', palette={'yes': '#081d58', 'no': "#65A9D375"}, alpha=0.8, ax=ax_sc)
        ax_sc.axvline(30, color='black', linestyle='--', label='Obesity Threshold (30)')
        ax_sc.yaxis.set_major_formatter(FuncFormatter(format_k))
        ax_sc.set_yticks(ticks)
        ax_sc.set_xlim(left=10)
        ax_sc.set_ylim(bottom=0, top=65000)
        ax_sc.legend(title = "Smoker")
        ax_sc.set_facecolor("#f7f9fc")
        ax_sc.grid(alpha=0.2)
        st.pyplot(fig_scatter)
        plt.close(fig_scatter)

    with tab3:
        child_stats = filtered_df.groupby('children').agg(avg_charges=('charges', 'mean'), smoker_pct=('smoker', lambda x: (x == 'yes').mean() * 100)).reset_index()
        fig_child, ax1 = plt.subplots(figsize=(6,5))
        sns.barplot(data=child_stats, x='children', y='avg_charges', ax=ax1, color='#65A9D3', alpha=1)
        ax1.yaxis.set_major_formatter(FuncFormatter(format_k))
        ax1.set_ylabel('Mean Charges ($)')
        ax1.set_ylim(bottom=0)
        ax2 = ax1.twinx()
        sns.lineplot(data=child_stats, x= 'children', y='smoker_pct', ax=ax2, color='#e74c3c', marker='o', linewidth=3)
        ax2.set_ylabel('Smoker Rate (%)', color='#e74c3c')
        ax2.set_ylim(0, 100)
        ax2.grid(True)
        st.pyplot(fig_child)
        plt.close(fig_child)
    
    with tab4:
        corr_df = filtered_df.copy()
        corr_df['smoker'] = corr_df['smoker'].map({'yes': 1, 'no': 0})
        corr_df['sex'] = corr_df['sex'].map({'male': 1, 'female': 0})
        corr_matrix = corr_df.select_dtypes(include=[np.number])
        corr_matrix = corr_matrix.loc[:, corr_matrix.nunique() > 1]
        fig_corr, ax_corr = plt.subplots(figsize=(5,4))
        sns.heatmap(corr_matrix.corr(), annot=True, cmap='coolwarm', ax=ax_corr, annot_kws={"size": 7}, cbar_kws={"aspect": 10})
        fig_corr.patch.set_facecolor("#f7f9fc")
        ax_corr.set_facecolor("#f7f9fc")
        st.pyplot(fig_corr)
        plt.close(fig_corr)

with divider_col:
    st.markdown( """<div style="border-left: 2px solid #e6e9ef; height: 1000px; margin-left: auto; margin-right: auto; "></div> """, unsafe_allow_html=True)

with right_col:

    # KPI Calculations
    avg_cost = filtered_df['charges'].mean()
    global_avg_cost = df['charges'].mean()
    avg_bmi = filtered_df['bmi'].mean()
    global_avg_bmi = df['bmi'].mean()
    smoker_rate = (filtered_df['smoker'] == 'yes').mean() * 100
    global_smoker_rate = (df['smoker'] == 'yes').mean() * 100   
    total_customers = len(df)


    # KPI Display 
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # KPI Standart Size
    st.markdown(""" <style>[data-testid="stMetric"] {min-height: 100px; display: flex; flex-direction: column; align-items: center; text-align: center;}</style>""", unsafe_allow_html=True)
    
    with kpi1:
        with st.container(border=True):
            st.metric(
                label="Average Medical Cost",
                value=f"${format_k(avg_cost, None)}",
                delta=f"{((avg_cost - global_avg_cost) / global_avg_cost) * 100:.1f}% vs Global",
                delta_color="inverse" # Red if cost is higher than global avg
            )

    with kpi2:
        with st.container(border=True):
            st.metric(
                label="Average BMI Index",
                value=f"{avg_bmi:.1f}",
                delta=f"{avg_bmi - global_avg_bmi:.1f} pts",
                delta_color="inverse" # Red if BMI is higher (higher risk)
            )

    with kpi3:
        with st.container(border=True):
            st.metric(
                label="Smoker Prevalence",
                value=f"{smoker_rate:.1f}%",
                delta=f"{smoker_rate - global_smoker_rate:.1f}%",
                delta_color="inverse" # Red if Smoker (Increased Risk)
            )

    with kpi4:
        with st.container(border=True):
            st.metric(
                label="Segment Size",
                value=f"{len(filtered_df):,}",
                delta=" ",
                help="Total number of policyholders in the selected demographic"
            )   

    st.divider()
    graph_col1, graph_divid, graph_col2 = st.columns([1, 0.02, 1])

    with graph_col1:
        st.markdown("<h5 style='text-align: right;'>Insurance Risk & Profitability Comparison</h5>", unsafe_allow_html=True)

        def get_deviation(col, is_binary=False):
            if is_binary:
                total_avg = (df[col] == 'yes').mean()
                group_avg = (filtered_df[col] == 'yes').mean()
            else:
                total_avg = df[col].mean()
                group_avg = filtered_df[col].mean()
            return ((group_avg - total_avg) / total_avg) * 100 if total_avg != 0 else 0

        metrics_data = {'Metric': ['Avg Charges ($)', 'Avg BMI', 'Smoker Rate (%)'], 
                        'Diff (%)': [get_deviation('charges'), get_deviation('bmi'), get_deviation('smoker', True)]}
        
        diff_df = pd.DataFrame(metrics_data)
        diff_df['Color'] = ['#e74c3c' if x > 0 else '#2ecc71' for x in diff_df['Diff (%)']]
        fig_bench, ax_bench = plt.subplots(figsize=(6, 10))
        sns.barplot(data=diff_df, x='Diff (%)', y='Metric', palette=dict(zip(diff_df['Metric'], diff_df['Color'])), ax=ax_bench)
        ax_bench.axvline(0, color='black', linewidth=1)
        ax_bench.grid(axis='x', alpha=0.3)
        ax_bench.spines[['top','right','left']].set_visible(False)
        ax_bench.tick_params(axis='y', labelsize=15)  
        ax_bench.tick_params(axis='x', labelsize=15)  
        ax_bench.set_xlabel("Diff (%)", fontsize=20, fontweight='bold', labelpad = 30)
        ax_bench.set_ylabel("Metric", fontsize=20, fontweight='bold')
        st.pyplot(fig_bench)
    
    with graph_divid:
        st.markdown( """<div style="border-left: 2px solid #e6e9ef; height: 770px; margin-left: auto; margin-right: auto; "></div> """, unsafe_allow_html=True)
    
    with graph_col2:
        st.markdown("<h5 style='text-align: center;'>Demographic Breakdown</h5>", unsafe_allow_html=True)
        pie_option = st.selectbox("Analyze by:", ["region", "smoker", "children"], index=0)
        pie_data = filtered_df[pie_option].value_counts()
        fig_pie, ax_pie = plt.subplots(figsize=(8, 7))
        explode = [0.2 if (x / pie_data.sum() < 0.05) else 0 for x in pie_data]
        wedges, texts, autotexts = ax_pie.pie( pie_data, autopct='%1.1f%%', colors=sns.color_palette("Blues_r",len(pie_data)+3),  wedgeprops={'linewidth': 2, 'edgecolor': 'white'}, startangle=220, pctdistance=1.2, explode=explode, textprops={'fontsize': 18})
        ax_pie.legend( wedges, pie_data.index, title=pie_option.capitalize(), loc="center left", bbox_to_anchor=(1.1, 0.5), fontsize=16, title_fontsize=18, frameon=True, borderpad=1, labelspacing=0.8, handlelength=1.4, handleheight=2) 
        ax_pie.axis('equal')
        plt.subplots_adjust(right= 0.85)
        st.pyplot(fig_pie)

