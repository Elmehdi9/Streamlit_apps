import streamlit as st
import cryptocompare as cc
import pandas as pd
from comps import chart
import datetime
import time


api_key= '1728a77ec571c20f3c6b403a5fd85b57adf32763eae8e0e6270c2de25d4c47e2'

st.set_page_config(layout="centered")

cco= cc.cryptocompare._set_api_key_parameter(api_key)

# Get Coins Names
coins=[]
for coin in cc.get_coin_list(format=False):
    coins.append(coin)
coins_df= pd.DataFrame.from_dict(coins)

col1, col2= st.columns(2)
choosen_coins= col1.multiselect(
                                label= 'Coins to visualize',
                                options= coins,
                                default= coins[:3],
                             )
price_per= col2.selectbox( label= 'Prices per:', options= ['Day', 'Hour', 'Minute'])

crypto_list= []

if price_per== 'Day':
    for coin in choosen_coins:
        crypto_list.append(cc.get_historical_price_day(
                                                coin,
                                                limit=300,
                                                exchange='CCCAGG',
                                                toTs=datetime.datetime.now(),           
                                              ))
elif price_per== 'Hour':
    for coin in choosen_coins:
        crypto_list.append(cc.get_historical_price_hour(
                                                  coin,
                                                  limit=300,
                                                  exchange='CCCAGG',
                                                  toTs=datetime.datetime.now(),           
                                                ))
else:
    for coin in choosen_coins:
        crypto_list.append(cc.get_historical_price_minute(
                                                  coin,
                                                  limit=300,
                                                  exchange='CCCAGG',
                                                  toTs=datetime.datetime.now(),           
                                                ))

dataframes_ls= []
for item, coin in zip(crypto_list, choosen_coins):
    coin_df = pd.DataFrame(item, columns=['time', 'open', 'close', 'volumeto'])
    coin_df['time']= pd.to_datetime(coin_df['time'], unit='s')
    coin_df['coin']= coin
    dataframes_ls.append(coin_df)

crypto_prices_df= pd.concat(dataframes_ls)

chart_ = chart.get_chart(crypto_prices_df)

st.altair_chart(chart_, use_container_width=True)






























    
