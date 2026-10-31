import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIG & CUSTOM DARK THEME CSS
# ==========================================
st.set_page_config(page_title="Punjab Monsoon Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom CSS to match the reference images
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0B1120; /* Very dark blue/black */
    }
    
    /* Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Roboto', sans-serif;
        color: #E2E8F0; /* Light gray text */
    }
    
    /* Headers */
    h1 {
        color: #FFFFFF !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0px !important;
    }
    h2 {
        color: #F8FAFC !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-top: 0px !important;
        margin-bottom: 15px !important;
    }
    
    /* Custom Card Style */
    .dashboard-card {
        background-color: #111827; /* Slightly lighter than background */
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        height: 100%;
    }
    
    /* KPI Metric Cards */
    .kpi-container {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 16px;
        text-align: left;
        height: 100%;
    }
    .kpi-title {
        font-size: 11px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-size: 12px;
        color: #64748B;
    }
    
    /* Text Utility Classes */
    .text-green { color: #10B981 !important; }
    .text-blue { color: #38BDF8 !important; }
    .text-orange { color: #F59E0B !important; }
    .text-red { color: #EF4444 !important; }

    /* Custom Badge */
    .badge {
        background-color: #064E3B;
        color: #10B981;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #10B981;
        display: inline-block;
    }
    
    /* Insight Box (Below Charts) */
    .insight-box {
        background-color: #0F172A;
        border-left: 4px solid #38BDF8;
        padding: 12px 16px;
        font-size: 13px;
        color: #CBD5E1;
        line-height: 1.6;
        border-radius: 0 8px 8px 0;
        margin-top: 15px;
    }
    
    /* List styling for findings */
    .custom-list {
        color: #CBD5E1; 
        font-size: 13px; 
        line-height: 1.8; 
        padding-left: 20px;
        margin: 0;
    }
    .custom-list li {
        margin-bottom: 8px;
    }
    
    /* Custom HTML Table for Confusion Matrix */
    .matrix-table {
        width: 100%; 
        text-align: center; 
        border-collapse: collapse; 
        color: white; 
        font-size: 18px;
        font-weight: 600;
    }
    .matrix-table td {
        padding: 20px; 
        border: 1px solid #1F2937;
    }
    .matrix-label {
        color: #94A3B8; 
        font-size: 12px; 
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Hide Streamlit Branding & Padding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 98%;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOCK CHART GENERATORS (Your Project Data)
# ==========================================
def chart_estimation():
    np.random.seed(42)
    actual = np.random.normal(500, 150, 50)
    predicted_linear = actual + np.random.normal(0, 50, 50)
    predicted_poly = actual + np.random.normal(0, 80, 50) # Poly is worse
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual, y=predicted_linear, mode='markers', name='Linear', marker=dict(color='#38BDF8', size=8)))
    fig.add_trace(go.Scatter(x=actual, y=predicted_poly, mode='markers', name='Polynomial', marker=dict(color='#F59E0B', size=8)))
    
    # Add perfect prediction line
    min_val, max_val = 200, 900
    fig.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines', name='Perfect Fit', line=dict(color='#475569', dash='dash')))
    
    fig.update_layout(
        title=dict(text="Actual vs Predicted Rainfall (mm)", font=dict(size=14, color='#F8FAFC')),
        plot_bgcolor='#111827', paper_bgcolor='#111827',
        font=dict(color='#94A3B8', size=11),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(title="Actual Rainfall", showgrid=True, gridcolor='#1F2937', zeroline=False),
        yaxis=dict(title="Predicted Rainfall", showgrid=True, gridcolor='#1F2937', zeroline=False)
    )
    return fig

def chart_clusters():
    fig = go.Figure()
    months = ['Jun', 'Jul', 'Aug', 'Sep']
    # Mock cluster data
    fig.add_trace(go.Scatter(x=months, y=[150, 650, 400, 100], mode='lines+markers', name='Cluster 0', line=dict(color='#38BDF8', width=2)))
    fig.add_trace(go.Scatter(x=months, y=[50, 200, 250, 150], mode='lines+markers', name='Cluster 1', line=dict(color='#F59E0B', width=2)))
    fig.add_trace(go.Scatter(x=months, y=[80, 100, 280, 200], mode='lines+markers', name='Cluster 2', line=dict(color='#10B981', width=2)))
    fig.add_trace(go.Scatter(x=months, y=[60, 50, 220, 180], mode='lines+markers', name='Cluster 3', line=dict(color='#EF4444', width=2)))
    
    fig.update_layout(
        title=dict(text="Average Monthly Rainfall Pattern", font=dict(size=14, color='#F8FAFC')),
        plot_bgcolor='#111827', paper_bgcolor='#111827',
        font=dict(color='#94A3B8', size=11),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor='#1F2937'),
        yaxis=dict(showgrid=True, gridcolor='#1F2937')
    )
    return fig

def chart_leaderboard():
    models = ['Random Forest', 'Linear Regression', 'PCA + MLP', 'MLP (No PCA)', 'Decision Tree']
    scores = [0.57, 0.57, 0.51, 0.31, -0.22] # R2 scores
    
    colors = ['#10B981' if s > 0 else '#EF4444' for s in scores]
    
    fig = go.Figure(go.Bar(
        x=scores, y=models,
        orientation='h',
        marker=dict(color=colors),
        text=[f"{s:.2f}" for s in scores],
        textposition='outside',
        textfont=dict(color='#E2E8F0')
    ))
    
    fig.update_layout(
        title=dict(text="Model Leaderboard (R² Score)", font=dict(size=14, color='#F8FAFC')),
        plot_bgcolor='#111827', paper_bgcolor='#111827',
        font=dict(color='#94A3B8', size=11),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor='#1F2937', range=[-0.3, 0.7]),
        yaxis=dict(showgrid=False)
    )
    fig.update_yaxes(autorange="reversed")
    return fig

# ==========================================
# 3. HEADER SECTION
# ==========================================
header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown("<h1>Punjab Monsoon Rainfall Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-top: 5px;'>Five-model analysis of JJAS rainfall estimation, drought risk, regional patterns and dimensionality reduction.</p>", unsafe_allow_html=True)

with header_right:
    st.markdown(
        """
        <div style="text-align: right;">
            <span class="badge">Model Analysis Ready</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 1px solid #1F2937; margin-top: 10px; margin-bottom: 24px;'>", unsafe_allow_html=True)

# ==========================================
# 4. KPI METRICS ROW
# ==========================================
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown("""
        <div class="kpi-container" style="border-top: 3px solid #38BDF8;">
            <div class="kpi-title">Best Estimation R²</div>
            <div class="kpi-value text-blue">0.57</div>
            <div class="kpi-sub">Multiple Linear Regression</div>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
        <div class="kpi-container" style="border-top: 3px solid #10B981;">
            <div class="kpi-title">SVM Accuracy</div>
            <div class="kpi-value text-green">73.9%</div>
            <div class="kpi-sub">Drought threshold: 349.1 mm</div>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
        <div class="kpi-container" style="border-top: 3px solid #F59E0B;">
            <div class="kpi-title">Drought Years</div>
            <div class="kpi-value text-orange">29</div>
            <div class="kpi-sub">of 115 Punjab seasons</div>
        </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
        <div class="kpi-container" style="border-top: 3px solid #10B981;">
            <div class="kpi-title">Best Ensemble R²</div>
            <div class="kpi-value text-green">0.57</div>
            <div class="kpi-sub">Random Forest · bagging</div>
        </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown("""
        <div class="kpi-container" style="border-top: 3px solid #94A3B8;">
            <div class="kpi-title">PCA + MLP R²</div>
            <div class="kpi-value" style="color: #E2E8F0;">0.51</div>
            <div class="kpi-sub">3 principal components</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================
# 5. MAIN CONTENT ROW 1 (Estimation & Clusters)
# ==========================================
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.plotly_chart(chart_estimation(), use_container_width=True)
    st.markdown("""
        <div class="insight-box">
            <strong>Insight:</strong> Multiple Linear Regression explains about 57% of test-set variation. The polynomial model (orange) does not improve the result and shows signs of overfitting at extreme values.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row1_col2:
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.plotly_chart(chart_clusters(), use_container_width=True)
    st.markdown("""
        <div class="insight-box">
            <strong>Insight:</strong> K-Means (k=4) reveals distinct monsoon patterns. Cluster 0 represents extreme peak rainfall in July, while Clusters 1-3 show more distributed or delayed rainfall patterns.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
# ==========================================
# 6. MAIN CONTENT ROW 2 (Leaderboard & Confusion Matrix)
# ==========================================
row2_col1, row2_col2 = st.columns([1.2, 1])

with row2_col1:
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.plotly_chart(chart_leaderboard(), use_container_width=True)
    st.markdown("""
        <div class="insight-box">
            <strong>Insight:</strong> Random Forest (0.57) ties with Linear Regression, proving the relationship is mostly linear. PCA + MLP (0.51) performs better than the raw MLP (0.31). Decision Tree failed completely (-0.22 R²).
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row2_col2:
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.markdown("<h2>SVM Confusion Matrix</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: space-around; color: #94A3B8; font-size: 12px; margin-bottom: 10px; text-transform: uppercase;">
            <span>Predicted Non-Drought</span>
            <span>Predicted Drought</span>
        </div>
        <table class="matrix-table">
            <tr>
                <td class="matrix-label" style="background-color: #111827; width: 20%;">Actual<br>Non-Drought</td>
                <td style="background-color: #1E3A8A; color: #93C5FD;">16</td> <!-- True Negative -->
                <td style="background-color: #111827;">1</td>  <!-- False Positive -->
            </tr>
            <tr>
                <td class="matrix-label" style="background-color: #111827; width: 20%;">Actual<br>Drought</td>
                <td style="background-color: #111827; color: #CBD5E1;">5</td> <!-- False Negative -->
                <td style="background-color: #1E3A8A; color: #93C5FD;">1</td>  <!-- True Positive -->
            </tr>
        </table>
        <div style="color: #64748B; font-size: 12px; margin-top: 15px; line-height: 1.5;">
            <strong>Insight:</strong> The model is highly precise for Non-Drought years (16 correct). However, it struggles to catch actual droughts (5 missed). Accuracy is 73.9%, but we must focus on drought Recall for risk management.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ==========================================
# 7. BOTTOM SECTION (Key Findings & Recommendations)
# ==========================================
bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.markdown("""
        <div class="dashboard-card">
            <h2>Key Findings</h2>
            <ul class="custom-list">
                <li><strong>Estimation:</strong> Multiple Linear Regression explains about 57% of test-set variation; the polynomial model does not improve the result.</li>
                <li><strong>Ensemble:</strong> Random Forest is the strongest tested ensemble, with R² around 0.57.</li>
                <li><strong>Dimensionality:</strong> PCA + MLP performs better than the MLP without PCA in this experiment (R² around 0.51).</li>
                <li><strong>Interpretation:</strong> Treat these as retrospective model results, not official seasonal forecasts.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with bottom_col2:
    st.markdown("""
        <div class="dashboard-card">
            <h2>Recommendations & Next Steps</h2>
            <ul class="custom-list">
                <li><strong>Risk:</strong> Drought sensitivity should be assessed using the confusion matrix, not accuracy alone.</li>
                <li><strong>Modeling:</strong> Stick to Linear Regression or Random Forest for estimation. Drop the Decision Tree due to negative R².</li>
                <li><strong>Clustering:</strong> Use the K-Means clusters to analyze which patterns lead to severe drought years.</li>
                <li><strong>Pipeline:</strong> Improve the MLP by testing more components in PCA or adding early stopping.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("<div style='text-align: center; color: #475569; font-size: 12px; margin-top: 40px; padding-bottom: 20px;'>Punjab Monsoon Rainfall Analysis · IMD Historical data · Research/educational use</div>", unsafe_allow_html=True)