import streamlit as st
import numpy as np
import pandas as pd


#import plotly.express as px

st.title('タイトル：テスト')

# サイドバー
# ファイルアップロード
uploaded_file = st.sidebar.file_uploader("ファイルアップロード", type='csv') 



# メイン画面
st.header('読み込みデータ表示')
if uploaded_file is not None:
    # アップロードファイルをメイン画面にデータ表示
    df = pd.read_csv(uploaded_file,encoding="shift-jis")
    #st.write(df)
    st.dataframe(df, width=500, height=500)


    target_jockey =['ルメール','岩田康誠','池添謙一', '藤岡佑介','横山武史','藤岡康太', '松岡正海','吉田隼人','横山典弘', '三浦皇成','武豊', '川田将雅', '蛯名正義','浜中俊', '藤田菜七','四位洋文','レーン','津村明秀','木幡巧也','柴田大知', '柴田善臣', '田辺裕信','松山弘平', '北村宏司', '小牧太']

    df.columns



"""
### サイドバー表示
```python

st.write('Interactive Widgets')

text = st.sidebar.text_input('あなたの趣味を教えてください。')
condition = st.sidebar.slider('あなたの調子は？',0,100,50)

'あなたの趣味:',text
'コンディション', condition
```

"""



st.title('Streamlit 超入門')

st.write('Interactive Widgets')

text = st.sidebar.text_input('あなたの趣味を教えてください。')
condition = st.sidebar.slider('あなたの調子は？',0,100,50)

'あなたの趣味:',text
'コンディション', condition



