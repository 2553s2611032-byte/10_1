import streamlit as st
import random

st.set_page_config(
    page_title="다정한 한국 - 우리문화 추천",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #DCECF8;
    color: #243746;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1500px;
}
h1, h2, h3, h4 {
    color: #243746;
}
[data-testid="stSidebar"] {
    background: #C7E0F3;
    border-right: 2px solid #243746;
}
div[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    min-height: 72px;
    font-size: 19px;
    font-weight: 700;
    border-radius: 16px;
    border: 2px solid #243746;
    background: #FFFFFF;
    color: #243746;
    padding: 12px;
    margin: 5px 0;
    white-space: normal;
}
div[data-testid="stSidebar"] div.stButton > button:hover {
    background: #A9D0EE;
    color: #243746;
}
.main-card {
    background: #FFFFFF;
    border: 2px solid #C7DCEC;
    border-radius: 22px;
    padding: 22px;
    margin: 10px 0 18px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 한국 문화 자료
# -----------------------------
CULTURE = {
    "인사와 예절": {
        "emoji": "🙇",
        "summary": "한국에서는 인사와 상대방을 존중하는 태도를 중요하게 여겨요.",
        "points": [
            "처음 만난 사람에게는 '안녕하세요'라고 인사해요.",
            "어른이나 처음 만난 사람에게는 존댓말을 쓰는 것이 무난해요.",
            "감사하거나 사과할 때는 말로 마음을 표현해요.",
            "인사 방식은 상대방의 상황과 문화를 존중해요.",
        ],
        "tip": "처음 만난 사람에게 '안녕하세요'라고 인사해 보세요.",
    },
    "식사 예절": {
        "emoji": "🍚",
        "summary": "함께 식사할 때는 서로 배려하고 음식을 나누는 문화를 볼 수 있어요.",
        "points": [
            "함께 식사하는 사람을 배려하며 식사를 시작해요.",
            "공용 음식은 집게나 공용 수저를 이용해요.",
            "다른 사람이 불편하지 않도록 식사 소리를 조절해요.",
            "식사 후에는 '잘 먹었습니다'라고 감사 인사를 할 수 있어요.",
        ],
        "tip": "음식을 함께 먹을 때는 다른 사람도 배려해요.",
    },
    "대중교통 예절": {
        "emoji": "🚌",
        "summary": "버스와 지하철에서는 많은 사람이 함께 이용하므로 배려가 필요해요.",
        "points": [
            "줄을 서서 차례대로 타고 내려요.",
            "내리는 사람이 먼저 내릴 수 있도록 기다려요.",
            "통화와 음악 소리는 작게 해요.",
            "교통약자석은 필요한 사람을 배려해 이용해요.",
            "혼잡할 때는 가방을 앞으로 메어 다른 사람을 배려해요.",
        ],
        "tip": "교통카드 사용법과 환승 방법을 미리 알아두면 편리해요.",
    },
