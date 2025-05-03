import streamlit as st
from streamlit_sortables import sort_items
import random

# 歴史的出来事とその年
events = {
    "アメリカ独立宣言": 1776,
    "フランス革命": 1789,
    "明治維新": 1868,
    "第一次世界大戦": 1914,
    "第二次世界大戦": 1939,
    "ベルリンの壁崩壊": 1989
}

st.title("🧠 歴史的出来事 並び替えゲーム")
st.write("以下の出来事を **古い順** に並び替えてください。")

# セッションに保存されたイベントがなければ作成
if "sample_events" not in st.session_state:
    st.session_state.sample_events = random.sample(list(events.items()), 4)

# 現在の出来事を取得
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
        st.write("正しい順番は：")
        for i, name in enumerate(correct_names, 1):
            st.write(f"{i}. {name}（{events[name]}年）")

# 新しい問題ボタン → セッション削除して再描画
if st.button("新しい問題を出す"):
    del st.session_state.sample_events
    st.experimental_rerun()
