import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
from gnews import GNews
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser as wb
from values import*
from urllib.parse import parse_qs,urlparse,quote
import pandas as pd
import requests
import upstox_client
from upstox_client.rest import ApiException
import pandas as pd
import datetime as dt
import time


st.title('📈Stock Dashboard')
st.image('alg_img.jpg')


now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days=1)
yesterday = yesterday.strftime('%m-%d-%Y')



stock = st.text_input("Enter a stock ticker symbol", "LT")
Today_stock = st.button("Get Today's Price",)
today = dt.date.today()
# start_date = today
if Today_stock:
    df = yf.download(f"{stock}", start=today, interval="1m")
    df['% Change'] = df['Close'].pct_change()*100
    df['% Change'] = df['% Change'].round(2)
    st.write(df)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[
                        0.7, 0.3], specs=[[{"type": "candlestick"}], [{"type": "bar"}]])
    fig.update_xaxes(rangeslider_visible=False)
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                  low=df['Low'], close=df['Close'], name='market data'), row=1, col=1)
    
    fig.add_trace(
        go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=2, col=1)
    st.plotly_chart(fig, use_container_width=True)

pricing_data,news = st.tabs(["Pricing Data", 'Top 3 News'])

# def calculate_price_difference(stock_data):
#     latest_price = stock_data.iloc[-1]["Close"]
#     previous_year_price = stock_data.iloc[-252]["Close"] if len(stock_data) > 252 else stock_data.iloc[0]["Close"]
#     price_difference = latest_price - previous_year_price
#     percentage_difference = (price_difference / previous_year_price) * 100
#     return price_difference, percentage_difference


with pricing_data:
    st.header("Price Movements")
    start_date = st.date_input('Start Date')
    End_date = st.date_input('End Date')
    dcf = yf.download(f"{stock}", start=start_date, end= End_date, interval="1d")
    data = dcf
    data["% Change"] = data['Adj Close']/ data['Adj Close'].shift(1)-1
    data.dropna(inplace=True)
    st.write(data)
    annual_return = data['% Change'].mean()*252*100
    st.write('Annual Return is: ', annual_return,'%')
    std_dev = np.std(data['% Change'])*np.sqrt(252)
    st.write('Standard Devivation is: ',std_dev*100,'%')

    


# with news:
#     gn = GNews(language='en', country='IN')
#     df_news= pd.DataFrame(gn.get_news(f'{stock}'+' stocks'))

#     for i in range(3):
#         st.subheader(f'News{i+1}')
#         # st.write(df_news['publisher'][i])
#         st.write(df_news['title'][i])
#         # st.write(df_news['description'][i])
#         Link = df_news['url'][i]
#         url = st.button(f'Link{i+1}',)
#         if url:
#             wb.open_new_tab(Link)
#         st.write(df_news['published date'][i])

with news:

    tick = st.text_input("NSE_INDEX|Nifty 50")
    Accs_tkn = st.text_input("Enter access token!")

    def buy_order(accs_token, ticker):
        import requests

        url = 'https://api.upstox.com/v2/order/place'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {accs_token}',
        }

        data = {
            'quantity': 1,
            'product': 'I',
            'validity': 'DAY',
            'price': 20.0,
            'tag': 'string',
            'instrument_token': ticker,
            'order_type': 'SL',
            'transaction_type': 'BUY',
            'disclosed_quantity': 0,
            'trigger_price': 19.5,
            'is_amo': False,
        }

        try:
            # Send the POST request
            response = requests.post(url, json=data, headers=headers)

            # Print the response status code and body
            print('Response Code:', response.status_code)
            print('Response Body:', response.json())

        except Exception as e:
            # Handle exceptions
            print('Error:', str(e))




    Start = st.button("Start the Trade")
    if Start:
            ticker = tick
            api_version = '2.0'
            api_instance = upstox_client.HistoryApi()
            instrument_key = ticker
            interval = '1minute'
            to_date = '2024-03-04'
            from_date = '2024-03-03'
            short = 5
            long = 12
            position = False
            count = 0

            for i in range(100):
                try:
                    # response = api_instance.get_historical_candle_data1(instrument_key, interval,to_date, from_date, api_version) 
                    response = api_instance.get_intra_day_candle_data(instrument_key,interval,api_version)   
                    df = pd.DataFrame.from_dict(response.data.candles)
                    
                    clos = ['datetime', 'open', 'high', 'low', 'close','null','null1']
                    df.columns = clos
                    df.drop(['null','null1'],axis=1,inplace=True)
                    df = df.iloc[::-1]
                    
                    df = df.set_index('datetime')
                    trade_signal = pd.DataFrame(index=df.index)
                    trade_signal['sma5'] = df['close'].rolling(window=short, min_periods=1).mean()
                    trade_signal['sma12'] = df['close'].rolling(window=long , min_periods=1).mean()
                    trade_signal['signal'] = 0.0
                    trade_signal['signal'] = np.where(trade_signal['sma5']> trade_signal['sma12'], 1.0, 0.0)
                    trade_signal['postn'] = trade_signal['signal'].diff()
                

                    # global em_data
                    # em_data = trade_dignal
                    print(trade_signal)
                    if(trade_signal['postn'].item ==1 and position == False):
                        if(count<3):
                            # buy_order(Accs_tkn,ticker)
                            print("yeah")
                            position = True 
                            count = count+1

                    if(trade_signal['postn'].item ==-1 and position==True):
                        # sell_order(accs_tkn,ticker)
                        print("n0o")
                        position = False

        
    # df['datetime'] = df['datetime'].dt.tz_localize('utc')
    # df['datetime'] = pd.to_datetime(df['datetime'], unit='s')

                except ApiException as e:
                    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)
                time.sleep(60)

        

        






