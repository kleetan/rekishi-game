import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import random

# CSVから出来事を読み込む
df = pd.read_csv('nenpyou.csv')

# CSVから出来事と年を辞書に変換
events = dict(zip(df['event'], df['year']))

st.title("🧠 歴史的出来事 並び替えゲーム")
st.write("以下の出来事を **古い順** に並び替えてください。")

# 出題数の選択（2〜6個まで）
num_choices = st.selectbox("出題数を選んでください（最大6個）", options=[2, 3, 4, 5, 6], index=2)

# 新しい問題ボタンが押されたら新しく出題
if "new_problem" not in st.session_state:
    st.session_state.new_problem = True

# 問題数が変わったら再出題
if "last_num" not in st.session_state or st.session_state.last_num != num_choices:
    st.session_state.new_problem = True
    st.session_state.last_num = num_choices

# 初回またはリセット時にランダムに出題
if "sample_events" not in st.session_state or st.session_state.new_problem:
    st.session_state.sample_events = random.sample(list(events.items()), num_choices)
    st.session_state.new_problem = False

sample_events = st.session_state.sample_events
event_names = [e[0] for e in sample_events]

# 並び替えUI
sorted_events = sort_items(event_names, direction="vertical")

# 判定ボタン
if st.button("判定する"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    correct_names = [e[0] for e in correct_order]

    if sorted_events == correct_names:
        st.success("🎉 正解です！")
    else:
        st.error("❌ 間違いです。")

    # 正解の順番は必ず表示
    st.write("正しい順番は：")
    for i, name in enumerate(correct_names, 1):
        st.write(f"{i}. {name}（{events[name]}年）")

# 新しい問題を出す
if st.button("新しい問題を出す"):
    st.session_state.new_problem = True
