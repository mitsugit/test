import streamlit as st
import numpy as np
import pandas as pd
import sqlite3 
import hashlib

#import plotly.express as px

st.title('タイトル：テスト')

# サイドバー
# ファイルアップロード
uploaded_file = st.sidebar.file_uploader("ファイルアップロード", type='csv') 

DATA_URL = ('C:\Users\addre\dev\streamlit')
df = pd.read_csv(DATA_URL,encoding="shift-jis")


# メイン画面
st.header('読み込みデータ表示')
if uploaded_file is not None:
    # アップロードファイルをメイン画面にデータ表示
    df = pd.read_csv(uploaded_file,encoding="shift-jis")
    #st.write(df)
    st.dataframe(df, width=500, height=500)


    target_jockey =['ルメール','岩田康誠','池添謙一', '藤岡佑介','横山武史','藤岡康太', '松岡正海','吉田隼人','横山典弘', '三浦皇成','武豊', '川田将雅', '蛯名正義','浜中俊', '藤田菜七','四位洋文','レーン','津村明秀','木幡巧也','柴田大知', '柴田善臣', '田辺裕信','松山弘平', '北村宏司', '小牧太']

    st.dataframe(df.columns, width=500, height=500)

    # 固有のrace_id作成関数

    def create_raceID(df):
        
        df = df.copy()
        
        # 場所列を複製し、変換用の列を作成
        df["場所変換用"] = df["場所"]


        # 一意のrace_id 列を追加する。
        kaisai_dict={}
        for i,x in enumerate(df["場所"].unique()):
            kaisai_dict[x] = i
        print(kaisai_dict)

        # 上記辞書に基づいて場所→番号に変換する関数 (ex. 中山→5)
        def kaisai_henkan(x):
            y = kaisai_dict[x]
            return y

        # 場所変換用に上記関数を適用する。
        df['場所変換用']=df['場所変換用'].map(lambda x:kaisai_henkan(x))
        
        
        # 固有のrace_idを作成する。
        df['race_id'] = df['場所変換用'].astype(str)+df["年"].astype(str)+df["月"].astype(str)+df["日"].astype(str)\
        +df["レース番号"].astype(str)
        df['race_id'].unique()
        
        
        return df

    
    df=create_raceID(df)

    st.dataframe(df, width=500, height=500)





