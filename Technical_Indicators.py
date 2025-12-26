import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
from stocknews import StockNews
st.title("Technical Indicator Dashboard")
stock = st.text_input("Enter the stock ticker:", "AAPL")
stock=stock.upper()
date =  st.text_input("Adjust the start date (YYYY-MM-DD):")
data=yf.download(stock, start=date, period = "90d", interval = "1d")
Close = data['Close']
High = data['High']
Low = data['Low']
Volume = data['Volume']
period = len(Close)
price_info = yf.Ticker(stock)
current_price = price_info.info.get("regularMarketPrice")
def calc_Williams_R(data, Williams_R=None):
    if period > 27:
        Highest_High = High.rolling(window=14).max()
        Lowest_Low = Low.rolling(window=14).min()
        Williams_R = -100 * ((Highest_High - Close) / (Highest_High - Lowest_Low))
        plt.title(stock + ' Williams Percent Range')
        plt.xlabel('Date')
        plt.xticks(rotation=75)
        plt.xticks(fontsize=8)
        plt.ylabel('Percent Range')
        plt.ylim(-100, 0)
        plt.grid(True)
        plt.plot(Williams_R)
        plt.show()
        st.pyplot(plt.gcf())
        return Williams_R
    else:
        return Williams_R

def calc_MACD(data):
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    plt.plot(data['Signal_Line'],'red', label = 'Signal Line')
    plt.plot(data['MACD'], 'green', label = 'MACD')
    plt.plot(data['MACD_Histogram'], 'blue', label = 'MACD Histogram')
    plt.legend(loc = 'best')
    plt.ylabel('MACD Information')
    plt.xlabel('Date')
    plt.xticks(fontsize=8)
    plt.xticks(rotation=75)
    plt.title(stock + ' Moving Average Convergence/Divergence')
    plt.grid(True)
    st.pyplot(plt.gcf())
    plt.show()
    return data['MACD_Histogram']

def calc_EMA(data):
    smooth= 2/(period+1)
    data['EMA'] = data['Close'].ewm(span = period, adjust = False).mean()
    plt.plot(data['EMA'])
    plt.title(stock + ' Exponential Moving Average')
    plt.xlabel('Date')
    plt.xticks(fontsize=8)
    plt.xticks(rotation=75)
    plt.ylabel('Price')
    plt.grid(True)
    st.pyplot(plt.gcf())
    plt.show()
    return data['EMA']

def calc_RSI(data):
        Diff = Close.diff()
        gain= Diff.clip(lower=0)
        loss = -Diff.clip(upper=0)
        period = 14
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        for i in range(period, len(data)):
            avg_gain.iloc[i] = ((avg_gain.iloc[i-1] * (period - 1)) + gain.iloc[i]) / period
            avg_loss.iloc[i] = ((avg_loss.iloc[i-1] * (period - 1)) + loss.iloc[i]) / period
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        plt.plot(rsi)
        plt.title(stock + ' Relative Strength Index')
        plt.ylim(0,100)
        plt.xlabel('Date')
        plt.xticks(fontsize=8)
        plt.xticks(rotation=75)
        plt.ylabel('Index Value')
        plt.grid(True)
        plt.show()
        st.pyplot(plt.gcf())
        return rsi

def calc_ROC(data, n=14):
    data['ROC'] = ((data['Close'] - data['Close'].shift(n)) / data['Close'].shift(n)) * 100
    plt.plot(data['ROC'])
    plt.xlabel('Date')
    plt.xticks(fontsize=8)
    plt.xticks(rotation=75)
    plt.ylabel('Percent Change')
    plt.title(stock + ' Rate of Change')
    plt.grid(True)
    plt.show()
    st.pyplot(plt.gcf())

    return data['ROC']

def calc_VWAP(data):
    Typical_Price = (High*Low*Close)/3
    Cumulative_TP_Volume = (Typical_Price * Volume).cumsum()
    Cumulative_Volume = Cumulative_TP_Volume.cumsum()
    data['VWAP'] = Cumulative_TP_Volume/Cumulative_Volume
    plt.plot(data['VWAP'])
    plt.xlabel('Date')
    plt.xticks(fontsize=8)
    plt.xticks(rotation=75)
    plt.ylabel('Price')
    plt.title(stock + ' Volume-Weighted Average Price')
    plt.grid(True)
    plt.show()
    st.pyplot(plt.gcf())
    return data['VWAP']
@st.dialog("Indicator Information", width="medium", dismissible=True, on_dismiss="ignore")
def info():
    st.write("Williams Percent Range")
    st.caption("A momentum indicator that suggests a stock being oversold in the range of -80% to -100% and overbought in the range of 0% to -20%.")
    st.write("MACD")
    st.caption("When MACD falls below the signal line, it is an indicator of a downward trend. When MACD crosses above the signal line, it is an indicator of an upward trend." )
    st.write("EMA")
    st.caption("A moving average that has a stronger emphasis on recent data points. Offers an advantage in responding fast to price fluctuations.")
    st.write("RSI")
    st.caption("When RSI holds a value above 70, it is suggested that a stock is overbought. \nWhen RSI holds a value below 30, it is suggested that a stock is oversold.")
    st.write("ROC")
    st.caption("Calculates the speed of price changes. If it is positive, prices are rising. If it is negative, prices are falling.")
    st.write("VWAP")
    st.caption("The average price of a stock based on volume and price. Similar to a moving average but smoother.")
if st.button("Indicator Information"):
    info()

graph = st.radio("Select a technical indicator", ["Williams_R", "MACD", "EMA", "RSI", "ROC", "VWAP"],
                 captions=["Williams Percent Range",
                           "Moving Average Convergence/Divergence",
                           "Exponential Moving Average",
                           "Relative Strength Index",
                           "Rate of Change",
                           "Volume Weighted Average Price"])


st.subheader(f"Current price is **{current_price}**")


if graph == "Williams_R":
    calc_Williams_R(data)

elif graph == "MACD":
    calc_MACD(data)

elif graph == "EMA":
    calc_EMA(data)

elif graph == "RSI":
    calc_RSI(data)

elif graph == "ROC":
    calc_ROC(data)

elif graph == "VWAP":
    calc_VWAP(data)


sn = StockNews(stock, wt_key = 'MY_WORLD_TRADING_DATA_KEY')
df= sn.summarize()
st.write(df)
st.write(df.columns)