import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import random

# CSVから出来事を読み込む
df = pd.read_csv('nenpyou.csv')

# 年号の最小値・最大値を取得
min_year = int(df['year'].min())
max_year = int(df['year'].max())

st.title("🧠 歴史的出来事 並び替えゲーム")
st.write("以下の出来事を **古い順** に並び替えてください。")

# 出題範囲を選択（スライダー）
year_range = st.slider(
    "出題する時代の範囲を選んでください（年）",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 範囲内にある出来事だけ抽出
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
events = dict(zip(filtered_df['event'], filtered_df['year']))

# 出題数の選択（2〜10個まで）
num_choices = st.selectbox("出題数を選んでください（最大10個）", options=list(range(2, 11)), index=4)

# エラーハンドリング：範囲内に出題数未満の出来事しかない場合
if len(events) < num_choices:
    st.error(f"この時代には出来事が {len(events)} 件しかありません。出題数を減らしてください。")
    st.stop()

# 新しい問題ボタンが押されたら新しく出題
if "new_problem" not in st.session_state:
    st.session_state.new_problem = True

# 問題数や範囲が変わったら再出題
if (
    "last_num" not in st.session_state or
    st.session_state.last_num != num_choices or
    "last_range" not in st.session_state or
    st.session_state.last_range != year_range
):
    st.session_state.new_problem = True
    st.session_state.last_num = num_choices
    st.session_state.last_range = year_range

# 初回またはリセット時にランダムに出題
if "sample_events" not in st.session_state or st.session_state.new_problem:
    st.session_state.sample_events = random.sample(list(events.items()), num_choices)
    st.session_state.new_problem = False

sample_events = st.session_state.sample_events
event_names = [e[0] for e in sample_events]

# 並び替えUI
sorted_events = sort_items(event_names, direction="vertical")

# 正解か不正解かのみを判定するボタン
if st.button("正解か不正解か判定"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    correct_names = [e[0] for e in correct_order]

    if sorted_events == correct_names:
        st.success("🎉 正解です！")
    else:
        st.error("❌ 間違いです。")

# 正解の詳細を表示するボタン
if st.button("詳細な正解を表示"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    correct_names = [e[0] for e in correct_order]

    st.write("正しい順番は：")
    for i, name in enumerate(correct_names, 1):
        st.write(f"{i}. {name}（{events[name]}年）")

# 新しい問題を出す
if st.button("新しい問題を出す"):
    st.session_state.new_problem = True
