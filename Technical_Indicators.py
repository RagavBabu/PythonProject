import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
stock = st.text_input("Enter the stock ticker you wish to analyze:")
stock=stock.upper()
date =  st.text_input("Enter the date at which you would like to start the analysis of this stock(YYYY-MM-DD):")
days = st.text_input("Enter the length of the period you would like to analyze with a unit('d' or 'h'):")
Interval = st.text_input("Enter the interval between each data point you would like to analyze('m', 'h', 'd'):")
st.write("Please enter the indicator you would like to use to analyze this stock")
Indicator = st.text_input("Options: \nWilliams_R \nMACD \nEMA \nRSI \nVWAP")
def reset():
    stock = ""
    date = ""
    days = ""
    Interval = ""
    Indicator = ""
    st.write("Please re-enter the variables you would like to replace")
    return stock, date, days, Interval, Indicator

st.button("Click to reset variables", on_click=reset, type="primary")
data=yf.download(stock, start=date, period = days, interval = Interval)
Close = data['Close']
High = data['High']
Low = data['Low']
Volume = data['Volume']
period = len(Close)

def calc_Williams_R(data, Williams_R=None):
    if period > 27:
        Highest_High = High.rolling(window=14).max()
        Lowest_Low = Low.rolling(window=14).min()
        Williams_R = -100 * ((Highest_High - Close) / (Highest_High - Lowest_Low))
        print('If the value is greater than -20, the market is at the top of its recent range. If the value is lower than -80, the market is at the bottom of its recent range.')
        plt.title(stock + ' Williams Percent Range')
        plt.xlabel('Date')
        plt.xticks(fontsize=8)
        plt.ylabel('Percent Range')
        plt.ylim(-100, 0)
        plt.grid(True)
        plt.plot(Williams_R)
        print(Volume)
        plt.show()
        st.pyplot(plt.gcf())
        return Williams_R
    else:
        print('Period is not long enough, please increase it to include more than 27 business days to obtain Williams % data')
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
    plt.title(stock + ' Moving Average Convergence/Divergence')
    plt.grid(True)
    print(Volume)
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
    plt.ylabel('Price')
    plt.grid(True)
    print(Volume)
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
        plt.ylabel('Index Value')
        plt.grid(True)
        print(Volume)
        plt.show()
        st.pyplot(plt.gcf())
        return rsi

def calc_ROC(data, n=14):
    data['ROC'] = ((data['Close'] - data['Close'].shift(n)) / data['Close'].shift(n)) * 100
    plt.plot(data['ROC'])
    plt.xlabel('Date')
    plt.xticks(fontsize=8)
    plt.ylabel('Percent Change')
    plt.grid(True)
    print(Volume)
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
    plt.ylabel('Price')
    plt.grid(True)
    print(Volume)
    plt.show()
    st.pyplot(plt.gcf())
    return data['VWAP']


if Indicator == 'Williams_R':
    calc_Williams_R(data)

elif Indicator == 'MACD':
    calc_MACD(data)

elif Indicator == 'EMA':
    calc_EMA(data)

elif Indicator == 'RSI':
    calc_RSI(data)

elif Indicator == 'ROC':
    calc_ROC(data)

elif Indicator == 'VWAP':
    calc_VWAP(data)

else:
    print('This is not a valid technical indicator')