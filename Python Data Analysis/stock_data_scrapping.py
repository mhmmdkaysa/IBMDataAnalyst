# Extracting and Visualizing Tesla and GameStop Stock Data
!pip install yfinance
!pip install bs4
!pip install nbformat
!pip install --upgrade plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "iframe"

# Ignore all warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define graphing function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))



# Extract Tesla's stock data with yfinance
tesla = yf.Ticker("TSLA")
tesla_data = pd.DataFrame(tesla.history(period="max"))

# Reset index of tesla_data
tesla_data.reset_index(inplace=True)

# Display the first five rows of tesla_data
tesla_data.head()



# Use webscrapping to extract Tesla's revenue data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

# Parsing html data using beautiful_soup
soup = BeautifulSoup(html_data,"html.parser")
table = soup.find_all("tbody")[1]
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in table.find_all("tr"):
    cols = row.find_all("td")
    if len(cols) == 2:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip().replace("$", "").replace(",", "")
        if revenue != "":
            tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame([[date, revenue]], columns=["Date", "Revenue"])], ignore_index=True)

# Remove comma, dollar sign, null, or empty sting from Revenue column
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# Display the last 5 row of tesla_revenue
tesla_revenue.tail()



# Extract GameStop's stock data with yfinance
gme = yf.Ticker("GME")
gme_data = pd.DataFrame(gme.history(period="max"))

# Reset index of gme_data
gme_data.reset_index(inplace=True)

# Display the first five rows of gme_data
gme_data.head()



# Use webscrapping to extract GameStop's revenue data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url).text

# Parsing html data using beautiful_soup
soup = BeautifulSoup(html_data_2, "html.parser")
table = soup.find_all("tbody")[1]
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in table.find_all("tr"):
    cols = row.find_all("td")
    if len(cols) == 2:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip().replace("$", "").replace(",", "")
        if revenue != "":
            gme_revenue = pd.concat([gme_revenue, pd.DataFrame([[date, revenue]], columns=["Date", "Revenue"])], ignore_index=True)

# Remove comma, dollar sign, null, or empty sting from Revenue column
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# Display the last 5 row of gme_revenue
gme_revenue.tail()


# Plot Tesla's stock graph
make_graph(tesla_data, tesla_revenue, "Tesla")

# Plot GameStop's stock graph
make_graph(gme_data, gme_revenue, "GameStop")
