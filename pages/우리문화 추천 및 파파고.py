import streamlit as st
import requests
import random

st.set_page_config(
    page_title="다정한 한국 - 우리문화 추천 및 번역",
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
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3, h4 {
    color: #243746;
}

[data-testid="stSidebar"] {
    background: #C7E0F3;
    border-right: 2px solid #243746;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #243746;
}

/* 왼쪽 메뉴 버튼만 크게 변경 */
div[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    min-height: 82px;
    font-size: 21px;
    line-height: 1.35;
    font-weight: 750;
    border-radius: 18px;
    border: 2px solid #243746;
    background: #FFFFFF;
    color: #243746;
    padding: 15px 12px;
    margin: 6px 0 10px 0;
    white-space: normal;
    text-align: left;
}

div[data-testid="stSidebar"] div.stButton > button:hover {
    background: #A9D0EE;
    border: 2px solid #243746;
    color: #243746;
}

div[data-testid="stSidebar"] div.stButton > button:focus {
    border: 3px solid #243746;
    color: #243746;
}

.small-note {
    color: #435969;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 한국 문화 데이터
# -----------------------------
CULTURE = {
    "인사하기": {
        "emoji": "🙇",
        "summary": "한국에서는 처음 만나거나 헤어질 때 인사를 중요하게 생각해요.",
        "points": [
            "처음 만났을 때는 '안녕하세요'라고 인사해요.",
            "감사할
