import streamlit as st
from streamlit_sortables import sort_items
import random

# 歴史的出来事と年
events = {
    "アメリカ独立宣言": 1776,
    "フランス革命": 1789,
    "明治維新": 1868,
    "第一次世界大戦": 1914,
    "第二次世界大戦": 1939,
    "ベルリンの壁崩壊": 1989
}

# ランダムに4つの出来事を選ぶ
sample_events = random.sample(list(events.items()), 4)
event_names = [e[0] for e in sample_events]

st.title("🧠 歴史的出来事 並び替えゲーム")
st.write("以下の出来事を **古い順** に並び替えてください。")

# ドラッグ＆ドロップのUI
sorted_events = sort_items(event_names, direction="vertical")

# 判定
if st.button("判定する"):
    correct_order = sorted(sample_events, key=lambda x: x[1])
    correct_names = [e[0] for e in correct_order]

    if sorted_events == correct_names:
        st.success("🎉 正解です！")
    else:
        st.error("❌ 残念、不正解です。")
        st.write("正しい順番はこちら：")
        for i, name in enumerate(correct_names, 1):
            st.write(f"{i}. {name}（{events[name]}年）")
