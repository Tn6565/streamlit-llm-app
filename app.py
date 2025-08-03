import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# 関数：専門家の種類と入力テキストを使ってLLMから回答を得る
def get_expert_response(user_input: str, expert_type: str) -> str:
    if expert_type == "医療の専門家":
        system_prompt = "あなたは経験豊富な医療の専門家です。専門的かつ分かりやすく説明してください。"
    elif expert_type == "法律の専門家":
        system_prompt = "あなたは信頼できる法律の専門家です。分かりやすく法的な観点から回答してください。"
    else:
        system_prompt = "あなたは有能な一般知識の専門家です。親切かつ論理的に回答してください。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    # OpenAI API キーは .env ファイルで読み込まれることを前提とする
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        return "OpenAI APIキーが見つかりません。環境変数 OPENAI_API_KEY を設定してください。"

    try:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_api_key)
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"AIの応答中にエラーが発生しました: {str(e)}"

# --- Streamlit UI構築 ---

st.set_page_config(page_title="専門家に相談するAIアプリ", layout="centered")

st.title("サンプルアプリ③: 専門家AI相談窓口")
st.write("このアプリでは、入力したテキストに対して、選択した専門家の視点からLLMが回答します。")
st.write("以下の手順に従ってください：")
st.markdown("""
1. 相談したい内容をテキスト入力欄に記入します  
2. 回答してほしい専門家の種類を選びます  
3. 「実行」ボタンを押すと、LLMが回答を表示します
""")

st.divider()

# 専門家の種類を選択
expert_type = st.radio(
    "回答してほしい専門家を選んでください：",
    ["医療の専門家", "法律の専門家", "一般知識の専門家"]
)

# ユーザー入力
user_input = st.text_area("相談内容を入力してください：", height=150)

# 実行ボタン
if st.button("実行"):
    if user_input.strip() == "":
        st.error("テキストを入力してください。")
    else:
        with st.spinner("AIが考え中です..."):
            response = get_expert_response(user_input, expert_type)
        st.success("AIの回答：")
        st.write(response)

