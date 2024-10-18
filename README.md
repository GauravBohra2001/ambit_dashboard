# Ambit Dashboard

Ambit Dashboard is an interactive web app for performing Discounted Cash Flow (DCF) valuation using a growth-RoC model. The app fetches financial data from Screener.in, calculates intrinsic PE, and assesses the degree of overvaluation for user-specified companies.

## Features
- **User Input for Company Symbol**: Enter any NSE/BSE company symbol to retrieve financial data directly from Screener.in.
- **Automated Web Scraping**: Fetches current PE, FY23 PE, 5-year median RoCE, and compounded sales/profit growth for different periods.
- **DCF Model Calculation**: Implements a growth-RoC DCF model using user-specified parameters such as cost of capital, RoCE, high growth period, fade period, and terminal growth rate.
- **Dynamic Financial Analysis**:
  - Computes intrinsic PE and evaluates the degree of overvaluation based on current and FY23 PE.
  - Provides flexibility with user-adjustable parameters to customize the valuation process.
- **Clean and Interactive UI**: Displays results in a structured format with real-time updates based on user inputs.

## Technologies Used
- **Python**: Main programming language for data processing and calculations.
- **Streamlit**: For creating the interactive web dashboard.
- **BeautifulSoup and Requests**: For web scraping financial data from Screener.in.
- **Pandas**: For data manipulation and analysis.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/GauravBohra2001/ambit_dashboard.git

## 2. Setup Instructions

- Navigate to the Project Directory:
  ```bash
  cd reversed-dcf
  ```

- Set Up a Virtual Environment:
  ```bash
  python -m venv venv
  ```

- Activate the Virtual Environment:
  - On Windows:
    ```bash
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

- Install the Required Dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 3. Usage

- Run the Streamlit App:
  ```bash
  streamlit run app.py
  ```

- Open the Web App:
  The dashboard will open in your web browser. Enter the company symbol, adjust the parameters, and view the calculated intrinsic value and overvaluation degree.

## 4. Project Structure
- **app.py**: The main script that runs the Streamlit app.
- **scraper.py**: Contains the functions for scraping data from Screener.in.
- **calculations.py**: Includes functions for performing DCF and other financial calculations.
- **requirements.txt**: Lists all the dependencies needed to run the project.
- **README.md**: Project documentation.

## 5. Contributing
Contributions are welcome! Feel free to fork this repository, create a new branch, and submit a pull request. Please ensure that your changes are well-documented and tested.
