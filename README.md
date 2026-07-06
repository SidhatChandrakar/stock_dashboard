# 📈 Stock Dashboard

An interactive **Stock Market Dashboard** built with **Streamlit**, **Yahoo Finance**, **Plotly**, and the **Upstox API**. The application enables users to analyze stock price movements, visualize candlestick charts, calculate financial metrics, and experiment with a simple moving average crossover trading strategy.

---

## Features

-  Real-time stock price retrieval using Yahoo Finance
-  Interactive candlestick chart with trading volume
-  Historical stock price analysis
-  Daily percentage return calculation
-  Annual return and volatility (standard deviation)
-  Custom date range selection
-  Simple Moving Average (SMA) crossover strategy
-  Upstox API integration for automated trading (experimental)
-  Interactive dashboard built with Streamlit

---


##  Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Streamlit | Web Dashboard |
| Pandas | Data Processing |
| NumPy | Numerical Computation |
| Plotly | Interactive Charts |
| Yahoo Finance (yfinance) | Stock Market Data |
| GNews | Financial News |
| Requests | API Communication |
| Upstox API | Trading Integration |

---

##  Project Structure

```
stock_dashboard/
│
├── app.py
├── alg_img.jpg
├── requirements.txt
├── .gitignore
└── README.md
```

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/stock-dashboard.git
```

### 2. Navigate into the project

```bash
cd stock-dashboard
```

### 3. Create a virtual environment

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## 📊 Dashboard Overview

The dashboard contains three major components:

###  Live Stock Price

- Fetches intraday stock prices
- Displays minute-level data
- Calculates percentage price change

###  Price Analysis

- Historical stock prices
- Annual Return
- Daily Returns
- Volatility (Standard Deviation)

###  Trading Strategy

Implements a basic **Simple Moving Average (SMA)** crossover strategy.

- SMA(5)
- SMA(12)

Buy Signal:

- SMA(5) crosses above SMA(12)

Sell Signal:

- SMA(5) crosses below SMA(12)

---

##  Disclaimer

This project is intended for **educational and learning purposes only**.

The automated trading functionality is experimental and should **not** be used for real financial decisions without proper testing and risk management.

---

##  Future Improvements

- Portfolio Management
- Watchlist
- Technical Indicators (RSI, MACD, EMA)
- Bollinger Bands
- News Sentiment Analysis
- Machine Learning Price Prediction
- Backtesting Engine
- Dark Mode
- Live Auto Refresh
- Docker Deployment

---

##  Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and submit a pull request.

---

