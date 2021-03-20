import streamlit as st
import numpy as np
import pandas as pd

st.title('Streamlit 超入門')

# df = pd.DataFrame({
#     '1列目':[1,2,3,4],
#     '2列目':[10,20,30,40]
# })


# マジックコマンド　マークアップ記法
"""
# 章
## 節
### 項目

```python

import streamlit as st
import numpy
import pandas as pd

```
"""

"""
dataframe オリジン

```python

df = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69,139.70],
    columns=['lat','long']
)

```
"""
df = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69,139.70],
    columns=['lat','lon'] 
)


# df = pd.DataFrame(
#     np.random.rand(20,3),
#     columns=['a','b','c']
# )


#st.write(df)

"""

```python
st.dataframe(df, width=300, height=300)
```

"""
st.dataframe(df, width=300, height=300)

"""
最大行をハイライト
```python
st.dataframe(df.style.highlight_max(axis=0))
```

"""

st.dataframe(df.style.highlight_max(axis=0))


# staticなテーブルを作りたい時はtable()を使用

"""
staticなテーブルを作りたい時はtable()を使用

```python
st.table(df.style.highlight_max(axis=0))
```
"""

st.table(df.style.highlight_max(axis=0))



# チャートを描く
"""
```python
st.line_chart(df)
```
"""

st.line_chart(df)

"""
```python
st.area_chart(df)
```
"""

st.area_chart(df)

"""
```python
st.map(df)
```
"""

st.map(df)

"""
画像を表示
```python
from PIL import Image

st.write('Display Image')


img=Image.open('sample.jpg')

#use_column_width=True 実際のレイアウトの横幅に合わせて表示する
st.image(img,caption='mitsu',use_column_width=True)

```
"""

from PIL import Image

st.write('Display Image')

img=Image.open('sample.jpg')
#use_column_width=True 実際のレイアウトの横幅に合わせて表示する
st.image(img,caption='mitsu',use_column_width=True)



"""
### チェックボックスによる表示切替
```python

if st.checkbox('Show Image'):
    img=Image.open('sample.jpg')
    #use_column_width=True 実際のレイアウトの横幅に合わせて表示する
    st.image(img,caption='mitsu',use_column_width=True)


```
"""


if st.checkbox('Show Image'):
    img=Image.open('sample.jpg')
    #use_column_width=True 実際のレイアウトの横幅に合わせて表示する
    st.image(img,caption='mitsu',use_column_width=True)


"""
### セレクトボックスによる表示切替
```python

option = st.selectbox(
    'あなたの好きな数字を教えてください。',
    list(range(1,11))
)

'あなたの好きな数字は、',option, 'です。'

```

"""




option = st.selectbox(
    'あなたの好きな数字を教えてください。',
    list(range(1,11))
)

'あなたの好きな数字は、',option, 'です。'

"""
### テキストボックスによる表示切替
```python

st.write('Interactive Widgets')

text = st.text_input('あなたの趣味を教えてください。')
'あなたの趣味:',text

```

"""



st.write('Interactive Widgets')

text = st.text_input('あなたの趣味を教えてください。')
'あなたの趣味:',text


"""
### スライダーによる値の変更
```python

condition = st.slider('あなたの調子は？',0,100,50)
'コンディション', condition

```

"""

condition = st.slider('あなたの調子は？',0,100,50)
'コンディション', condition


"""
### 2カラム
```python
left_column,right_column = st.beta_columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラム')
```

"""

left_column,right_column = st.beta_columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラム')


"""
### expander
```python

expander1 = st.beta_expander('問い合わせ１')
expander1.write('問い合わせ１の回答')
expander2 = st.beta_expander('問い合わせ2')
expander2.write('問い合わせ2の回答')
expander3 = st.beta_expander('問い合わせ3')
expander3.write('問い合わせ3の回答')

```

"""




expander1 = st.beta_expander('問い合わせ１')
expander1.write('問い合わせ１の回答')
expander2 = st.beta_expander('問い合わせ2')
expander2.write('問い合わせ2の回答')
expander3 = st.beta_expander('問い合わせ3')
expander3.write('問い合わせ3の回答')







import time

st.write('プログレスバーの表示')
'Start!!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i + 1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'Done!!!'

"""

表示

"""