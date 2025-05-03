import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import random

# CSVから読み込み
df = pd.read_csv('nenpyou.csv')

# データの準備
df = df.dropna(subset=['event', 'year'])  # 欠損除外
df['year'] = df['year'].astype(int)

# 紀元前／後の選択ラジオボタン
era_filter = st.radio(
    "時代を選んでください",
    ["すべて", "紀元前のみ", "紀元後のみ"],
    horizontal=True
)

# ラジオボタンに応じてデータフィルタリング
if era_filter == "紀元前のみ":
    df = df[df['year'] < 0]
elif era_filter == "紀元後のみ":
    df = df[df['year'] >= 0]

# 範囲指定スライダー（現在のdfに基づく）
if df.empty:
    st.error("選択された条件ではデータが存在しません。")
    st.stop()

min_year = int(df['year'].min())
max_year = int(df['year'].max())

year_range = st.slider(
    "出題する年の範囲を選んでください",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 範囲内の出来事を抽出
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
events = dict(zip(filtered_df['event'], filtered_df['year']))

# 出題数の選択
num_choices = st.selectbox("出題数を選んでください（最大10個）", options=list(range(2, 11)), index=4)

# 範囲内に十分な数があるか確認
if len(events) < num_choices:
    st.error(f"この条件では出来事が {len(events)} 件しかありません。出題数を減らしてください。")
    st.stop()

# 新しい問題の管理
if "new_problem" not in st.session_state:
    st.session_state.new_problem = True

# 条件が変わったら再出題
if (
    "last_num" not in st.session_state or
    st.session_state.last_num != num_choices or
    "last_range" not in st.session_state or
    st.session_state.last_range != year_range or
    "last_era" not in st.session_state or
    st.session_state.last_era != era_filter
):
    st.session_state.new_problem = True
    st.session_state.last_num = num_choices
    st.session_state.last_range = year_range
    st.session_state.last_era = era_filter

# 出題
if "sample_events" not in st.session_state or st.session_state.new_problem:
    st.session_state.sample_events = random.sample(list(events.items()), num_choices)
    st.session_state.new_problem = False

sample_events = st.session_state.sample_events
event_names = [e[0] for e in sample_events]

# 並び替え UI
sorted_events = sort_items(event_names, direction="vertical")

# 判定ボタン
if st.button("正解か不正解か判定"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    correct_names = [e[0] for e in correct_order]

    if sorted_events == correct_names:
        st.success("🎉 正解です！")
    else:
        st.error("❌ 間違いです。")

# 正しい位置の数を確認
if st.button("正しい位置の数を確認"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    correct_names = [e[0] for e in correct_order]

    correct_count = sum([1 for user, correct in zip(sorted_events, correct_names) if user == correct])

    st.info(f"✅ 現在の並びで {correct_count} 件が正しい位置にあります。")

# 答え表示
if st.button("詳細な正解を表示"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    st.write("正しい順番は：")
    for i, (event, year) in enumerate(correct_order, 1):
        st.write(f"{i}. {event}（{year}年）")

# 再出題
if st.button("新しい問題を出す"):
    st.session_state.new_problem = True
