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

crypto_list = cc.get_historical_price_minute(
                                            'BTC',
                                            limit=300,
                                            exchange='CCCAGG',
                                            toTs=datetime.datetime.now(),           
                                          )

crypto_prices_df = pd.DataFrame(crypto_list, columns=['time', 'open', 'close', 'volumeto'])
crypto_prices_df['time']= pd.to_datetime(crypto_prices_df['time'], unit='s')
st.write(crypto_list)

chart_ = chart.get_chart(crypto_prices_df)
st.altair_chart(chart_, use_container_width=True)






























    
