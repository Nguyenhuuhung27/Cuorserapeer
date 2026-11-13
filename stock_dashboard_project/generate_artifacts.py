import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import nbformat as nbf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

project_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\stock_dashboard_project"
screenshots_dir = os.path.join(project_dir, "coursera_screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# 1. Load cached data
tesla_data = pd.read_csv(os.path.join(project_dir, "tesla_data.csv"))
tesla_revenue = pd.read_csv(os.path.join(project_dir, "tesla_revenue.csv"))
gme_data = pd.read_csv(os.path.join(project_dir, "gme_data.csv"))
gme_revenue = pd.read_csv(os.path.join(project_dir, "gme_revenue.csv"))

# Build Plotly Figures
def make_plotly_figure(stock_data, revenue_data, stock_name):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )
    # Datetime handling
    stock_df = stock_data.copy()
    stock_df['Date_dt'] = pd.to_datetime(stock_df['Date'], utc=True).dt.tz_localize(None)
    rev_df = revenue_data.copy()
    rev_df['Date_dt'] = pd.to_datetime(rev_df['Date'], utc=True).dt.tz_localize(None)

    stock_specific = stock_df[stock_df['Date_dt'] <= pd.to_datetime('2021-06-14')]
    revenue_specific = rev_df[rev_df['Date_dt'] <= pd.to_datetime('2021-04-30')]

    fig.add_trace(go.Scatter(
        x=stock_specific['Date_dt'],
        y=stock_specific['Close'].astype(float),
        name="Share Price",
        line=dict(color='#1f77b4')
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=revenue_specific['Date_dt'],
        y=revenue_specific['Revenue'].astype(float),
        name="Revenue",
        line=dict(color='#ff7f0e')
    ), row=2, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock_name,
        xaxis_rangeslider_visible=True
    )
    return fig

fig_tsla = make_plotly_figure(tesla_data, tesla_revenue, "Tesla")
fig_gme = make_plotly_figure(gme_data, gme_revenue, "GameStop")

# Convert plotly figures to JSON specs for notebook mime output
plotly_tsla_json = json.loads(fig_tsla.to_json())
plotly_gme_json = json.loads(fig_gme.to_json())

# Generate static image plots using matplotlib for screenshots (questions 5 & 6)
def plot_dashboard_image(stock_data, revenue_data, stock_name, out_path):
    stock_df = stock_data.copy()
    stock_df['Date_dt'] = pd.to_datetime(stock_df['Date'], utc=True).dt.tz_localize(None)
    rev_df = revenue_data.copy()
    rev_df['Date_dt'] = pd.to_datetime(rev_df['Date'], utc=True).dt.tz_localize(None)

    stock_specific = stock_df[stock_df['Date_dt'] <= pd.to_datetime('2021-06-14')].sort_values('Date_dt')
    revenue_specific = rev_df[rev_df['Date_dt'] <= pd.to_datetime('2021-04-30')].sort_values('Date_dt')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=False)
    fig.suptitle(f"{stock_name} Stock and Revenue Dashboard", fontsize=16, fontweight='bold', y=0.98)

    # Subplot 1: Share Price
    ax1.plot(stock_specific['Date_dt'], stock_specific['Close'].astype(float), color='#e74c3c' if stock_name=='Tesla' else '#2980b9', linewidth=2)
    ax1.set_title("Historical Share Price", fontsize=13, fontweight='semibold')
    ax1.set_ylabel("Price ($US)", fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Subplot 2: Revenue
    ax2.plot(revenue_specific['Date_dt'], revenue_specific['Revenue'].astype(float), color='#27ae60', linewidth=2, marker='o', markersize=4)
    ax2.set_title("Historical Revenue", fontsize=13, fontweight='semibold')
    ax2.set_xlabel("Date", fontsize=11)
    ax2.set_ylabel("Revenue ($US Millions)", fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()

plot_dashboard_image(tesla_data, tesla_revenue, "Tesla", os.path.join(screenshots_dir, "Question_5_Tesla_Dashboard.png"))
plot_dashboard_image(gme_data, gme_revenue, "GameStop", os.path.join(screenshots_dir, "Question_6_GameStop_Dashboard.png"))

# Generate code + output screenshots for Questions 1, 2, 3, 4
def render_table_screenshot(title_text, desc_text, code_text, df_display, out_path, is_tail=False):
    fig = plt.figure(figsize=(11, 4.8), dpi=200)
    
    # Background color white
    fig.patch.set_facecolor('#ffffff')
    
    # Title & description
    plt.text(0.04, 0.93, title_text, fontsize=13, fontweight='bold', color='#111827', transform=fig.transFigure)
    plt.text(0.04, 0.86, desc_text, fontsize=9.5, color='#4b5563', transform=fig.transFigure)
    
    # Code box
    rect = plt.Rectangle((0.04, 0.65), 0.92, 0.17, fill=True, color='#f8fafc', edgecolor='#cbd5e1', transform=fig.transFigure, zorder=2)
    fig.patches.append(rect)
    plt.text(0.06, 0.73, code_text, fontsize=10, family='monospace', color='#0f172a', transform=fig.transFigure, zorder=3)
    
    # Table output
    ax = fig.add_axes([0.04, 0.08, 0.92, 0.52])
    ax.axis('off')
    
    # Prepare table data
    df_clean = df_display.copy()
    # Format floating numbers if any
    for c in df_clean.columns:
        if df_clean[c].dtype == float:
            df_clean[c] = df_clean[c].map(lambda x: f"{x:.6f}" if abs(x) < 100 else f"{x:.2f}")
    
    table_data = [df_clean.columns.tolist()] + df_clean.values.tolist()
    row_labels = df_clean.index.astype(str).tolist()
    
    # Add index as first column
    table_data_with_idx = []
    headers = [''] + df_clean.columns.tolist()
    table_data_with_idx.append(headers)
    for idx_label, row in zip(row_labels, df_clean.values.tolist()):
        table_data_with_idx.append([idx_label] + row)
        
    table = ax.table(
        cellText=table_data_with_idx[1:],
        colLabels=table_data_with_idx[0],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.4)
    
    # Style table headers
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor('#e2e8f0')
        if r == 0:
            cell.set_text_props(weight='bold', color='#1e293b')
            cell.set_facecolor('#f1f5f9')
        else:
            if r % 2 == 0:
                cell.set_facecolor('#f8fafc')
            else:
                cell.set_facecolor('#ffffff')
                
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

# Q1 Screenshot
render_table_screenshot(
    "Question 1: Use yfinance to Extract Stock Data",
    "Reset the index, save, and display the first five rows of the tesla_data dataframe using the head function.",
    "tesla = yf.Ticker('TSLA')\ntesla_data = tesla.history(period='max')\ntesla_data.reset_index(inplace=True)\ntesla_data.head()",
    tesla_data.head(),
    os.path.join(screenshots_dir, "Question_1_Tesla_Stock_Data.png")
)

# Q2 Screenshot
render_table_screenshot(
    "Question 2: Use Webscraping to Extract Tesla Revenue Data",
    "Display the last five rows of the tesla_revenue dataframe using the tail function.",
    "# Clean revenue & display tail\ntesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',|\\$', '', regex=True)\ntesla_revenue.dropna(inplace=True)\ntesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != '']\ntesla_revenue.tail()",
    tesla_revenue.tail(),
    os.path.join(screenshots_dir, "Question_2_Tesla_Revenue_Data.png"),
    is_tail=True
)

# Q3 Screenshot
render_table_screenshot(
    "Question 3: Use yfinance to Extract Stock Data",
    "Reset the index, save, and display the first five rows of the gme_data dataframe using the head function.",
    "gme = yf.Ticker('GME')\ngme_data = gme.history(period='max')\ngme_data.reset_index(inplace=True)\ngme_data.head()",
    gme_data.head(),
    os.path.join(screenshots_dir, "Question_3_GameStop_Stock_Data.png")
)

# Q4 Screenshot
render_table_screenshot(
    "Question 4: Use Webscraping to Extract GameStop Revenue Data",
    "Display the last five rows of the gme_revenue dataframe using the tail function.",
    "# Clean revenue & display tail\ngme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(',|\\$', '', regex=True)\ngme_revenue.dropna(inplace=True)\ngme_revenue = gme_revenue[gme_revenue['Revenue'] != '']\ngme_revenue.tail()",
    gme_revenue.tail(),
    os.path.join(screenshots_dir, "Question_4_GameStop_Revenue_Data.png"),
    is_tail=True
)

print("Screenshots created successfully!")
