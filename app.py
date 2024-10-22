import os

# Install the required packages if they are not available
os.system("pip install requests==2.28.1")
os.system("pip install beautifulsoup4==4.11.1")
os.system("pip install pandas==1.4.3")
os.system("pip install streamlit==1.12.2")
os.system("pip install matplotlib==3.5.2")


import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Reading the first file and creating a DataFrame for stock names and symbols
data = pd.read_csv(r'C:\Users\Gaurav Bohra\Desktop\Assignment\GauravBohra_Assignment_Ambit\ambit_dashboard\EQUITY_L.csv')

# Dropping unnecessary columns and renaming columns for consistency
data.drop(data.columns[2:], axis=1, inplace=True)
data = data.reindex(columns=['NAME OF COMPANY', 'SYMBOL'])
data.rename(columns={'NAME OF COMPANY': 'stock_name', 'SYMBOL': 'stock_symbol'}, inplace=True)

# Reading the second file and processing it similarly
df = pd.read_csv(r'C:\Users\Gaurav Bohra\Desktop\Assignment\GauravBohra_Assignment_Ambit\ambit_dashboard\Equity.csv')
df.drop(df.columns[0], axis=1, inplace=True)
df.drop(df.columns[2:], axis=1, inplace=True)
df.rename(columns={'Issuer Name': 'stock_name', 'Security Id': 'stock_symbol'}, inplace=True)

# Merging the two DataFrames
new_df = pd.concat([data, df], ignore_index=True)

# Dropping duplicate rows
new_df.drop_duplicates(inplace=True)

# Reading the Excel file and converting columns to a dictionary
xls = pd.ExcelFile(r'C:\Users\Gaurav Bohra\Desktop\Assignment\GauravBohra_Assignment_Ambit\ambit_dashboard\StockData.xlsx')
df = pd.read_excel(xls, 'Combined')
stk_name = df['stock_name']
stk_symbl = df['stock_symbol']
res = {stk_name[i]: stk_symbl[i] for i in range(len(stk_name))}

# Streamlit interface enhancements for styling
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        color: #4CAF50;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Header for the dashboard
st.markdown('<p class="big-font">Reverse DCF Dashboard 📈🧑‍💻↗️</p>', unsafe_allow_html=True)
st.sidebar.header("Selecting The Best ✨")

# Step 1: User input for stock name
selected_stock = st.sidebar.selectbox("**Enter Stock Symbol or Stock Name**", res)

if selected_stock:
    sym = res.get(selected_stock)
    if not sym:
        st.error("Stock symbol not found. Please enter a valid stock name or symbol.")
    else:
        st.write(f"### Stock Symbol: `{sym}`")

        # Step 2: Determine URL for fetching financial data
        url = f"https://www.screener.in/company/{sym}/consolidated/"
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        webpage = requests.get(url, headers=HEADERS)

        if webpage.status_code != 200:
            st.error("Failed to retrieve data from the website.")
        else:
            soup = BeautifulSoup(webpage.content, "html.parser")

            # Check if consolidated data is available, otherwise switch to standalone
            bs = soup.find_all('tr', attrs={'class': 'stripe strong', 'class': 'strong'})
            total_liabilities_values = []
            total_assets_values = []

            for row in bs:
                if row.find('td', class_='text').text.strip() == 'Total Liabilities':
                    total_liabilities_values.extend([cell.text.strip() for cell in row.find_all('td')[1:]])
                if row.find('td', class_='text').text.strip() == 'Total Assets':
                    total_assets_values.extend([cell.text.strip() for cell in row.find_all('td')[1:]])

            new_url = f"https://www.screener.in/company/{sym}/" if not total_liabilities_values and not total_assets_values else url
            webpage = requests.get(new_url, headers=HEADERS)

            if webpage.status_code != 200:
                st.error("Failed to retrieve data from the updated URL.")
            else:
                page = BeautifulSoup(webpage.content, "html.parser")

                # Step 3: Scrape financial data and display metrics
                st.write("### Financial Metrics")
                col1, col2, col3 = st.columns(3)

                with col1:
                    # Display Stock PE
                    stock_pe = None
                    try:
                        stock_pe_element = page.find_all('span', class_='number')
                        if len(stock_pe_element) > 4 and stock_pe_element[4].text.strip():
                            stock_pe = float(stock_pe_element[4].text.strip().replace(',', ''))
                            st.markdown(f"<div class='metric-card'>Stock PE: <strong>{stock_pe}</strong></div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='metric-card'>Stock PE: Not Available</div>", unsafe_allow_html=True)
                    except (IndexError, ValueError):
                        st.markdown("<div class='metric-card'>Stock PE: Not Available</div>", unsafe_allow_html=True)

                with col2:
                    # Display Market Cap
                    try:
                        market_cap = int(page.find_all('span', class_='number')[0].text.strip().replace(',', ''))
                        formatted_market_cap = f"₹ {market_cap:,} Cr"
                        st.markdown(f"<div class='metric-card'>Market Cap: <strong>{formatted_market_cap}</strong></div>", unsafe_allow_html=True)
                    except (IndexError, ValueError):
                        st.markdown("<div class='metric-card'>Market Cap: Not Available</div>", unsafe_allow_html=True)

                with col3:
                    # Display FY23 PE
                    try:
                        profit_fy = page.find(id='profit-loss', class_='card card-large')
                        rows = profit_fy.find_all('tr')
                        net_profit_data = [cell.get_text(strip=True) for row in rows if 'Net Profit' in row.get_text() for cell in row.find_all('td')[1:]]
                        net_profit_dec_23 = int(net_profit_data[-3].replace(',', ''))
                        FY23PE = (market_cap * 1e7) / net_profit_dec_23
                        st.markdown(f"<div class='metric-card'>FY23 PE: <strong>{FY23PE:.2f}</strong></div>", unsafe_allow_html=True)
                    except (IndexError, ValueError):
                        st.markdown("<div class='metric-card'>FY23 PE: Not Available</div>", unsafe_allow_html=True)

                # Display Compounded Growth Rates
                st.write("### Compounded Growth Rates")
                try:
                    sales_profit = page.find(id='profit-loss', class_='card card-large')
                    rows = sales_profit.find_all('table', class_='ranges-table')

                    compounded_sales_growth = []
                    compounded_profit_growth = []
                    for row in rows:
                        if 'Compounded Sales Growth' in row.get_text():
                            compounded_sales_growth.extend([cell.get_text(strip=True) for cell in row.find_all('td')])
                        if 'Compounded Profit Growth' in row.get_text():
                            compounded_profit_growth.extend([cell.get_text(strip=True) for cell in row.find_all('td')])

                    # Create DataFrames for growth data and display
                    sales_growth_df = pd.DataFrame({
                        "Period": compounded_sales_growth[::2],
                        "Sales Growth": compounded_sales_growth[1::2]
                    })
                    profit_growth_df = pd.DataFrame({
                        "Period": compounded_profit_growth[::2],
                        "Profit Growth": compounded_profit_growth[1::2]
                    })

                    st.write("#### Compounded Sales Growth")
                    st.table(sales_growth_df)

                    st.write("#### Compounded Profit Growth")
                    st.table(profit_growth_df)

                except (IndexError, ValueError):
                    st.error("Failed to fetch compounded growth rates.")

                # DCF Calculation for Intrinsic PE and Overvaluation
                try:
                    st.write("### User Inputs for DCF Calculation")
                    coc = st.slider("Cost of Capital (CoC): %", min_value=8, max_value=16, step=1) / 100
                    roc = st.slider("Return on Capital Employed (RoCE): %", min_value=10, max_value=100, step=10) / 100
                    growth_rate = st.slider("Growth during High Growth Period: %", min_value=8, max_value=20, step=2) / 100
                    high_growth_period = st.slider("High Growth Period (years)", min_value=10, max_value=25, step=2)
                    fade_period = st.slider("Fade Period (years)", min_value=5, max_value=20, step=5)
                    terminal_growth_rate = st.slider("Terminal Growth Rate: %", min_value=0.0, max_value=7.5, step=0.5) / 100

                    tax_rate = 0.25
                    fcf = []
                    ebt = [100]
                    nopat = []
                    investment = []
                    discount_factors = []
                    discounted_fcf = []

                    # Calculate Free Cash Flow (FCF), Discounted FCF, and Intrinsic Value
                    for year in range(int(high_growth_period + fade_period)):
                        if year < high_growth_period:
                            current_growth = growth_rate
                        else:
                            current_growth = max(
                                terminal_growth_rate,
                                growth_rate - (year - high_growth_period) * ((growth_rate - terminal_growth_rate) / fade_period)
                            )

                        ebt.append(ebt[-1] * (1 + current_growth))
                        current_nopat = ebt[-1] * (1 - tax_rate)
                        nopat.append(current_nopat)
                        current_investment = current_nopat * (roc - terminal_growth_rate)
                        investment.append(current_investment)

                        current_fcf = current_nopat - current_investment
                        fcf.append(current_fcf)
                        discount_factor = 1 / ((1 + coc) ** (year + 1))
                        discount_factors.append(discount_factor)
                        discounted_fcf.append(current_fcf * discount_factor)

                    terminal_value = fcf[-1] * (1 + terminal_growth_rate) / (coc - terminal_growth_rate)
                    discounted_terminal_value = terminal_value * discount_factors[-1]
                    intrinsic_value = sum(discounted_fcf) + discounted_terminal_value
                    intrinsic_pe = intrinsic_value / net_profit_dec_23
                    st.write(f"Intrinsic PE: {intrinsic_pe:.2f}")

                    # Calculate Degree of Overvaluation
                    try:
                        if stock_pe is None or FY23PE is None or intrinsic_pe is None or intrinsic_pe == 0:
                            raise ValueError("Required data for calculating the Degree of Overvaluation is not available.")
                        
                        degree_of_overvaluation = (stock_pe / intrinsic_pe) - 1 if stock_pe < FY23PE else (FY23PE / intrinsic_pe) - 1
                        st.write(f"Degree of Overvaluation: {degree_of_overvaluation * 100:.2f}%")

                    except (ValueError, ZeroDivisionError) as e:
                        st.error(f"Failed to calculate the Degree of Overvaluation: {e}")

                    # Visualization of Discounted Cash Flows
                    st.write("### Discounted Cash Flows Visualization")
                    try:
                        if stock_pe is None or not discounted_fcf:
                            raise ValueError("Required data is not available for this stock. Cannot display the graph.")
                        
                        years = [f'Year {i}' for i in range(1, high_growth_period + fade_period + 1)] + ['Terminal Value']
                        discounted_fcf_with_terminal = discounted_fcf + [discounted_terminal_value]

                        fig, ax = plt.subplots(figsize=(12, 8))
                        bars = ax.barh(years, discounted_fcf_with_terminal, color=plt.cm.Blues(np.linspace(0.4, 0.8, len(years))), alpha=0.9)

                        ax.set_title('Discounted Cash Flows Including Terminal Value', fontsize=16, fontweight='bold', pad=20)
                        ax.set_xlabel('Value (₹)', fontsize=14)
                        ax.set_ylabel('Year', fontsize=14)
                        ax.grid(axis='x', linestyle='--', alpha=0.7)

                        for bar in bars:
                            width = bar.get_width()
                            ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:,.2f}', ha='left', va='center', fontsize=10, color='black')

                        st.pyplot(fig)

                    except (ValueError, ZeroDivisionError) as e:
                        st.error(f"Failed to display the graph: {e}")

                except (ValueError, ZeroDivisionError) as e:
                    st.error(f"Error in DCF calculation: {e}")
