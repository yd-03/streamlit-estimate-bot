import streamlit as st

# 過去の見積データ（例として）
past_estimates = {
    "example1": {
        "お客様のお名前は何ですか？": "田中 太郎",
        "ご住所を教えてください。": "東京都新宿区",
        "電話番号を教えてください。": "090-1234-5678",
        "ご希望のリフォーム内容を教えてください。": "キッチンのリフォーム",
        "予算はいくらですか？": "100万円",
        "希望の完成日を教えてください。": "2023年12月1日",
    }
}

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 見積作成チャットボット")

if "start_estimate" not in st.session_state:
    st.session_state["start_estimate"] = None

if st.session_state["start_estimate"] is None:
    st.write("以前の現場と似た仕様のお見積りですか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい"):
            st.session_state["start_estimate"] = "past"
            st.rerun()
    with col2:
        if st.button("いいえ"):
            st.session_state["start_estimate"] = "new"
            st.rerun()
else:
    if st.session_state["start_estimate"] == "past":
        st.write("過去の見積を使用します。")
        estimate_data = past_estimates["example1"]
        st.write("過去の見積データ:")
        for question, answer in estimate_data.items():
            st.write(f"{question}: {answer}")
    elif st.session_state["start_estimate"] == "new":
        if "current_question_index" not in st.session_state:
            st.session_state["current_question_index"] = 0
        if "estimate_data" not in st.session_state:
            st.session_state["estimate_data"] = {}
        if "current_answer" not in st.session_state:
            st.session_state["current_answer"] = ""

        questions = [
            "お客様のお名前は何ですか？",
            "ご住所を教えてください。",
            "電話番号を教えてください。",
            "ご希望のリフォーム内容を教えてください。",
            "予算はいくらですか？",
            "希望の完成日を教えてください。",
        ]

        current_question_index = st.session_state["current_question_index"]
        estimate_data = st.session_state["estimate_data"]

        def ask_question(index):
            st.write(questions[index])
            st.session_state["current_answer"] = st.text_input(
                "回答を入力してください：", key=f"question_{index}"
            )
            if st.button("一つ前に戻る", key=f"back_button_{index}"):
                if st.session_state["current_question_index"] > 0:
                    st.session_state["current_question_index"] -= 1
                    previous_question = questions[
                        st.session_state["current_question_index"]
                    ]
                    if previous_question in estimate_data:
                        del estimate_data[previous_question]
                    st.session_state["current_answer"] = ""
                    st.rerun()
            if st.button("次へ", key=f"next_button_{index}"):
                if st.session_state["current_answer"].strip() == "":
                    st.warning("回答を入力してください。")
                else:
                    estimate_data[questions[index]] = st.session_state["current_answer"]
                    st.session_state["current_question_index"] += 1
                    st.session_state["current_answer"] = ""
                    st.rerun()

        if current_question_index < len(questions):
            ask_question(current_question_index)
        else:
            st.write("全ての質問が完了しました。")

        if estimate_data:
            st.write("これまでの回答:")
            for question, answer in estimate_data.items():
                st.write(f"{question}: {answer}")

        if st.button("最初からやり直す"):
            st.session_state["current_question_index"] = 0
            st.session_state["estimate_data"] = {}
            st.session_state["current_answer"] = ""
            st.rerun()
    else:
        st.write("見積もり作成をキャンセルしました。")
