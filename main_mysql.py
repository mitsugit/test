import streamlit as st
import numpy as np
import pandas as pd
import sqlite3 
import hashlib

#import plotly.express as px

st.title('タイトル：テスト')

# サイドバー
# ファイルアップロード
# uploaded_file = st.sidebar.file_uploader("ファイルアップロード", type='csv') 

# DATA_URL = ('C:\Users\addre\dev\streamlit')
# df = pd.read_csv(DATA_URL,encoding="shift-jis")


# メイン画面
st.header('読み込みデータ表示')


import MySQLdb

# 接続する
conn = MySQLdb.connect(
user='root',
passwd='root',
host='localhost',
db='test_db',
charset='utf8')

# カーソルを取得する
cur = conn.cursor()

# SQL（データベースを操作するコマンド）を実行する
# userテーブルから、HostとUser列を取り出す
sql = "select * from net_keiba2019"
cur.execute(sql)

df = pd.read_sql(sql, conn,)
conn.close()



#st.dataframe(df, width=900, height=500)


df = pd.read_csv('2019全開催.csv',encoding="shift-jis")

target_jockey =['ルメール','岩田康誠','池添謙一', '藤岡佑介','横山武史','藤岡康太', '松岡正海','吉田隼人','横山典弘', '三浦皇成','武豊', '川田将雅', '蛯名正義','浜中俊', '藤田菜七','四位洋文','レーン','津村明秀','木幡巧也','柴田大知', '柴田善臣', '田辺裕信','松山弘平', '北村宏司', '小牧太']

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

#　初期化と同時に様々な値を取得できるようにした。

class jockey_renpai:
    
    def __init__(self,target_jockey):
        
        # 騎手名_renpaiという列名を追加し、値は空とする。
        self.df = self.newcolumns(target_jockey)
        
        #　各ジョッキーの対象レース行のインデックスを取得する。（辞書型でまとめる）
        self.index_jockey_dict = self.jockey_dict(target_jockey)
        
        #  各ジョッキーの1着になるまでの連敗数のリスト取得し、辞書型でまとめる。
        #  騎手名_renpai列に連敗数入れる。
        self.max_renpai_dict = self.renpaibeforewin(self.index_jockey_dict,self.df)
        
        # 各騎手の平均連敗数をリスト取得し、辞書型でまとめる。
        self.heikin_renpai = self.heikin_renpai(self.max_renpai_dict)
        
        
        self.hindo_renpai_dict = self.hindo_keisan(self.max_renpai_dict)
        
        
        
    # 騎手名_renpaiという列を作成
    def newcolumns(self,target_jockey):
        new_columns=[]
        for i in target_jockey:
            #print("{}_renpai".format(i))
            new_columns.append("{}_renpai".format(i))
        for x in new_columns:
            df[x]=""
            
        return df
    
    # 騎手ごとの行のインデックス番号リストを作成
    def jockey_dict(self,target_jockey):
        index_jockey_dict={}
        for i in target_jockey:
            index_list = []
            index_list =list(df[df['騎手']==i].index)
            index_jockey_dict[i] = index_list
            
        return index_jockey_dict
    
    
    
    
    # max_renpai_dictの作成　+  連敗列の作成
        
    def renpaibeforewin(self,index_jockey_dict,df2):
        max_renpai_dict = {}

        for i in index_jockey_dict:
            max_renpai = []    
            #　各ジョッキー連敗列の列番号を取得
            column_no = df2.columns.get_loc("{}_renpai".format(i))

            # for文の何回目かをカウント
            count = 0

            for s in index_jockey_dict[i]:


                if df2.iloc[s]['確定着順']==1:
                    df2.iat[s,column_no] = 0
                    if count != 0:
                        max_renpai.append(df2.iat[index_jockey_dict[i][count-1],column_no])


                else:
                    if count == 0:
                        #print("0")
                        #print(df.iat[s,column_no])
                        df2.iat[s,column_no] = 1
                    else:
                        #print(df.iat[i-1,32]+1)
                        #1着でない場合は、前の出走レースの連敗数に１を加えた数を連敗数フィールドに入れる
                        df2.iat[s,column_no] = df2.iat[index_jockey_dict[i][count-1],column_no]+1

                count += 1
                
                max_renpai = [t for t in max_renpai if t >0]
            max_renpai_dict[i] = max_renpai

        return max_renpai_dict
        


    # 平均連敗数を作成
    def heikin_renpai(self,max_renpai_dict):

        heikin_renpai_dict = {}

        for i in max_renpai_dict:
            #renpai_list_length =  len(max_renpai_dict[i])-max_renpai_dict[i].count(0.0)
            
            heikin = sum(max_renpai_dict[i])/len(max_renpai_dict[i])


            heikin_renpai_dict[i] = heikin


        return heikin_renpai_dict
    
    
    # 統計情報計算
    
    # 連敗数の頻度を算出(何連敗が何回あるかの出現確率リストを作り、騎手ごとに辞書型でまとめる)
    def hindo_keisan(self,max_renpai_dict):
        hindo_renpai_dict = {}
        for i in max_renpai_dict:
            kakuritsu=pd.Series(max_renpai_dict[i])
            # 各連敗数の出現確率
            hindo=kakuritsu.value_counts()/kakuritsu.value_counts().sum()
            
            hindo_renpai_dict[i] = hindo
        
        return hindo_renpai_dict

    
    # 連敗数を指定してその確率を求める（引数のhindoには、hindo_ranapai_dictで計算した辞書から「辞書変数名["騎手名"]」という形で指定する。）
    def prob(self,hindo,target_renpai):
        probtotal=0 
        for i,x in hindo.items():
            if i >= target_renpai:
                probtotal = probtotal + x 
        return probtotal

    # 指定する確率に達する連敗数を見つける（targetprobに0.5といったように確率を指定する。）
    def prob_target(self,hindo,targetprob):
        # 連敗数の小さい順に並べ替える
        sortedlist = sorted(hindo.keys())
        probtotal=0
        for i in sortedlist:
            probtotal += hindo[i]
            if probtotal > targetprob:
                target=i
                break
        return i
    
hr = jockey_renpai(target_jockey)

#hr.max_renpai_dict

# hr.heikin_renpai

# hr.hindo_renpai_dict
    
#     # 情報を調べたいジョッキーを指定
jocky = "田辺裕信"

# #hr = jockey_renpai(target_jockey)

# hr.hindo_renpai_dict

target_hindo = hr.hindo_renpai_dict
target_hindo[jocky]


st.line_chart(target_hindo[jocky])
# hr.prob_target(target_hindo[jocky],0.5)



# hr.prob(target_hindo[jocky],10)


# print(hr.prob_target(target_hindo[jocky],0.5))
# print(hr.prob(target_hindo[jocky],10))

# print("hello world")


#st.write(hr.prob(target_hindo[jocky],10))





# if uploaded_file is not None:
    # アップロードファイルをメイン画面にデータ表示
    # df = pd.read_csv(uploaded_file,encoding="shift-jis")
    #st.write(df)


















    # st.dataframe(df, width=500, height=500)


    # target_jockey =['ルメール','岩田康誠','池添謙一', '藤岡佑介','横山武史','藤岡康太', '松岡正海','吉田隼人','横山典弘', '三浦皇成','武豊', '川田将雅', '蛯名正義','浜中俊', '藤田菜七','四位洋文','レーン','津村明秀','木幡巧也','柴田大知', '柴田善臣', '田辺裕信','松山弘平', '北村宏司', '小牧太']

    # st.dataframe(df.columns, width=500, height=500)


    # 固有のrace_id作成関数

    # def create_raceID(df):
        
    #     df = df.copy()
        
    #     # 場所列を複製し、変換用の列を作成
    #     df["場所変換用"] = df["場所"]


    #     # 一意のrace_id 列を追加する。
    #     kaisai_dict={}
    #     for i,x in enumerate(df["場所"].unique()):
    #         kaisai_dict[x] = i
    #     print(kaisai_dict)

    #     # 上記辞書に基づいて場所→番号に変換する関数 (ex. 中山→5)
    #     def kaisai_henkan(x):
    #         y = kaisai_dict[x]
    #         return y

    #     # 場所変換用に上記関数を適用する。
    #     df['場所変換用']=df['場所変換用'].map(lambda x:kaisai_henkan(x))
        
        
    #     # 固有のrace_idを作成する。
    #     df['race_id'] = df['場所変換用'].astype(str)+df["年"].astype(str)+df["月"].astype(str)+df["日"].astype(str)\
    #     +df["レース番号"].astype(str)
    #     df['race_id'].unique()
        
        
    #     return df

    
    # df=create_raceID(df)

    # st.dataframe(df, width=500, height=500)





