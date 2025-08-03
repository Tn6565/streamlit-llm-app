from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from openai import OpenAI

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# タイトルと説明
st.title("サンプルアプリ②: 少し複雑なWebアプリ")

st.write("##### 動作モード1: 健康アドバイザー")
st.write("健康に関するテキストを入力すると、健康アドバイザーがアドバイスを提供します。")
st.write("##### 動作モード2: スポーツインストラクター")
st.write("スポーツに関するテキストを入力すると、スポーツインストラクターがアドバイスを提供します。")

# モード選択
selected_item = st.radio(
    "動作モードを選択してください。",
    ["健康アドバイザー", "スポーツインストラクター"]
)

st.divider()

# 入力フォーム
user_input = st.text_area("質問を入力してください。", height=100)

# モードごとの system メッセージ
role_messages = {
    "健康アドバイザー": "あなたは健康に関するアドバイザーです。安全で信頼できる健康アドバイスを提供してください。",
    "スポーツインストラクター": "あなたはプロのスポーツインストラクターです。運動やトレーニングについて、実践的かつ安全なアドバイスを提供してください。"
}

# 実行ボタン
if st.button("アドバイスをもらう"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("アドバイスを生成中..."):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": role_messages[selected_item]},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5
            )
            response = completion.choices[0].message.content
            st.success("アドバイス:")
            st.markdown(response)
