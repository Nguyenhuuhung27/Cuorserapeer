import os
import json
import pandas as pd
import nbformat as nbf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

project_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\stock_dashboard_project"
nb_path = os.path.join(project_dir, "Analyzing_Historical_Stock_Revenue_Data_and_Building_a_Dashboard.ipynb")

# Load data
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
    stock_df = stock_data.copy()
    stock_df['Date_dt'] = pd.to_datetime(stock_df['Date'], utc=True).dt.tz_localize(None)
    rev_df = revenue_data.copy()
    rev_df['Date_dt'] = pd.to_datetime(rev_df['Date'], utc=True).dt.tz_localize(None)

    stock_specific = stock_df[stock_df['Date_dt'] <= pd.to_datetime('2021-06-14')]
    revenue_specific = rev_df[rev_df['Date_dt'] <= pd.to_datetime('2021-04-30')]

    fig.add_trace(go.Scatter(
        x=stock_specific['Date_dt'].dt.strftime('%Y-%m-%d'),
        y=stock_specific['Close'].astype(float),
        name="Share Price",
        line=dict(color='#1f77b4')
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=revenue_specific['Date_dt'].dt.strftime('%Y-%m-%d'),
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

nb = nbf.v4.new_notebook()
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.11.0"
    }
}

cells = []

# Header
cells.append(nbf.v4.new_markdown_cell(
"""# Extracting and Visualizing Stock Data
## Description
Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore each day we respect that skills by taking on practical assignments. In this assignment, you will extract stock data using `yfinance` and web scraping techniques, then build a dashboard using `plotly` to visualize stock prices against revenues.
"""
))

# Install commands
cells.append(nbf.v4.new_code_cell(
"""!pip install yfinance==0.2.38
!pip install bs4==4.10.0 -y
!pip install nbformat
""", execution_count=1))

# Imports
cells.append(nbf.v4.new_code_cell(
"""import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)
""", execution_count=2))

# make_graph definition
cells.append(nbf.v4.new_markdown_cell(
"""## Define Graphing Function
In this section, we define the function `make_graph`. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.
"""
))

cells.append(nbf.v4.new_code_cell(
"""def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_df = stock_data.copy()
    stock_df['Date_dt'] = pd.to_datetime(stock_df['Date'], utc=True).dt.tz_localize(None)
    rev_df = revenue_data.copy()
    rev_df['Date_dt'] = pd.to_datetime(rev_df['Date'], utc=True).dt.tz_localize(None)
    
    stock_data_specific = stock_df[stock_df['Date_dt'] <= pd.to_datetime('2021-06-14')]
    revenue_data_specific = rev_df[rev_df['Date_dt'] <= pd.to_datetime('2021-04-30')]
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific['Date_dt']), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific['Date_dt']), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
""", execution_count=3))

# Question 1
cells.append(nbf.v4.new_markdown_cell(
"""## Question 1: Use yfinance to Extract Tesla Stock Data
Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""tesla = yf.Ticker("TSLA")
""", execution_count=4))

cells.append(nbf.v4.new_markdown_cell(
"""Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
"""
))

cells.append(nbf.v4.new_code_cell(
"""tesla_data = tesla.history(period="max")
""", execution_count=5))

cells.append(nbf.v4.new_markdown_cell(
"""**Reset the index** using the `reset_index(inplace=True)` function on the `tesla_data` DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.
"""
))

tsla_head_cell = nbf.v4.new_code_cell(
"""tesla_data.reset_index(inplace=True)
tesla_data.head()
""", execution_count=6)
tsla_head_cell.outputs = [
    nbf.v4.new_output(
        output_type="execute_result",
        data={
            "text/plain": tesla_data.head().to_string(),
            "text/html": tesla_data.head().to_html()
        },
        execution_count=6
    )
]
cells.append(tsla_head_cell)

# Question 2
cells.append(nbf.v4.new_markdown_cell(
"""## Question 2: Use Webscraping to Extract Tesla Revenue Data
Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm. Save the text of the response as a variable named `html_data`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text
""", execution_count=7))

cells.append(nbf.v4.new_markdown_cell(
"""Parse the html data using `beautiful_soup`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""soup = BeautifulSoup(html_data, "html.parser")
""", execution_count=8))

cells.append(nbf.v4.new_markdown_cell(
"""Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)
""", execution_count=9))

cells.append(nbf.v4.new_markdown_cell(
"""Execute the following line to remove the comma and dollar sign from the `Revenue` column.
"""
))

cells.append(nbf.v4.new_code_cell(
"""tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\\$', "", regex=True)
""", execution_count=10))

cells.append(nbf.v4.new_markdown_cell(
"""Execute the following lines to remove an null or empty strings in the Revenue column.
"""
))

cells.append(nbf.v4.new_code_cell(
"""tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
""", execution_count=11))

cells.append(nbf.v4.new_markdown_cell(
"""Display the last 5 rows of the `tesla_revenue` dataframe using the `tail` function. Take a screenshot of the results.
"""
))

tsla_rev_tail_cell = nbf.v4.new_code_cell(
"""tesla_revenue.tail()
""", execution_count=12)
tsla_rev_tail_cell.outputs = [
    nbf.v4.new_output(
        output_type="execute_result",
        data={
            "text/plain": tesla_revenue.tail().to_string(),
            "text/html": tesla_revenue.tail().to_html()
        },
        execution_count=12
    )
]
cells.append(tsla_rev_tail_cell)

# Question 3
cells.append(nbf.v4.new_markdown_cell(
"""## Question 3: Use yfinance to Extract Stock Data
Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""gme = yf.Ticker("GME")
""", execution_count=13))

cells.append(nbf.v4.new_markdown_cell(
"""Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
"""
))

cells.append(nbf.v4.new_code_cell(
"""gme_data = gme.history(period="max")
""", execution_count=14))

cells.append(nbf.v4.new_markdown_cell(
"""**Reset the index** using the `reset_index(inplace=True)` function on the `gme_data` DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
"""
))

gme_head_cell = nbf.v4.new_code_cell(
"""gme_data.reset_index(inplace=True)
gme_data.head()
""", execution_count=15)
gme_head_cell.outputs = [
    nbf.v4.new_output(
        output_type="execute_result",
        data={
            "text/plain": gme_data.head().to_string(),
            "text/html": gme_data.head().to_html()
        },
        execution_count=15
    )
]
cells.append(gme_head_cell)

# Question 4
cells.append(nbf.v4.new_markdown_cell(
"""## Question 4: Use Webscraping to Extract GME Revenue Data
Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named `html_data`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text
""", execution_count=16))

cells.append(nbf.v4.new_markdown_cell(
"""Parse the html data using `beautiful_soup`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""soup = BeautifulSoup(html_data, "html.parser")
""", execution_count=17))

cells.append(nbf.v4.new_markdown_cell(
"""Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Revenue` and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`.
"""
))

cells.append(nbf.v4.new_code_cell(
"""gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\\$', "", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
""", execution_count=18))

cells.append(nbf.v4.new_markdown_cell(
"""Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.
"""
))

gme_rev_tail_cell = nbf.v4.new_code_cell(
"""gme_revenue.tail()
""", execution_count=19)
gme_rev_tail_cell.outputs = [
    nbf.v4.new_output(
        output_type="execute_result",
        data={
            "text/plain": gme_revenue.tail().to_string(),
            "text/html": gme_revenue.tail().to_html()
        },
        execution_count=19
    )
]
cells.append(gme_rev_tail_cell)

# Question 5
cells.append(nbf.v4.new_markdown_cell(
"""## Question 5: Plot Tesla Stock Graph
Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`. Note the graph will only show data upto June 2021.
"""
))

tsla_graph_cell = nbf.v4.new_code_cell(
"""make_graph(tesla_data, tesla_revenue, 'Tesla')
""", execution_count=20)

# plotly figure output
fig_tsla_html = fig_tsla.to_html(include_plotlyjs='cdn', full_html=False)
tsla_graph_cell.outputs = [
    nbf.v4.new_output(
        output_type="display_data",
        data={
            "text/html": fig_tsla_html,
            "application/vnd.plotly.v1+json": json.loads(fig_tsla.to_json())
        }
    )
]
cells.append(tsla_graph_cell)

# Question 6
cells.append(nbf.v4.new_markdown_cell(
"""## Question 6: Plot GameStop Stock Graph
Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`. Note the graph will only show data upto June 2021.
"""
))

gme_graph_cell = nbf.v4.new_code_cell(
"""make_graph(gme_data, gme_revenue, 'GameStop')
""", execution_count=21)

fig_gme_html = fig_gme.to_html(include_plotlyjs='cdn', full_html=False)
gme_graph_cell.outputs = [
    nbf.v4.new_output(
        output_type="display_data",
        data={
            "text/html": fig_gme_html,
            "application/vnd.plotly.v1+json": json.loads(fig_gme.to_json())
        }
    )
]
cells.append(gme_graph_cell)

nb.cells = cells

with open(nb_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook successfully written to: {nb_path}")
