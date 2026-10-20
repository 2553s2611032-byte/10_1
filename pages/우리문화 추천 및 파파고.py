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
            "감사할 때는 '감사합니다' 또는 '고맙습니다'라고 말해요.",
            "어른이나 선생님께는 공손한 말투를 사용하는 것이 좋아요.",
        ],
        "phrase": "안녕하세요. 만나서 반갑습니다.",
    },
    "식사 예절": {
        "emoji": "🍚",
        "summary": "함께 식사할 때는 상대방을 배려하는 태도가 중요해요.",
        "points": [
            "어른과 식사할 때는 어른이 먼저 수저를 든 뒤 먹는 것이 예의로 여겨져요.",
            "식사 중 큰 소리를 내지 않도록 해요.",
            "음식을 함께 나눌 때는 공용 집게나 숟가락을 사용해요.",
        ],
        "phrase": "잘 먹겠습니다. 맛있게 드세요!",
    },
    "대중교통": {
        "emoji": "🚌",
        "summary": "버스와 지하철에서는 서로 배려하는 태도가 중요해요.",
        "points": [
            "대중교통 안에서는 통화나 음악 소리를 작게 해요.",
            "내리는 사람을 먼저 보내고 줄을 지켜요.",
            "교통약자석은 필요한 사람이 이용할 수 있도록 배려해요.",
        ],
        "phrase": "먼저 내리세요.",
    },
    "말투와 존댓말": {
        "emoji": "💬",
        "summary": "한국어는 상대방과 상황에 따라 말투가 달라질 수 있어요.",
        "points": [
            "처음 만난 사람이나 어른에게는 존댓말을 쓰는 것이 무난해요.",
            "친한 친구끼리는 편한 말투를 사용하기도 해요.",
            "상대방을 존중하며 예의를 지켜요.",
        ],
        "phrase": "도와주셔서 감사합니다.",
    },
    "집 방문하기": {
        "emoji": "🏡",
        "summary": "다른 사람의 집에 방문할 때는 집주인과 공간을 존중해요.",
        "points": [
            "방문하기 전에 미리 연락하고 약속 시간을 지켜요.",
            "신발을 벗고 들어가는 집이 많으니 입구에서 확인해요.",
            "물건을 사용할 때는 먼저 허락을 구하는 것이 좋아요.",
        ],
        "phrase": "초대해 주셔서 감사합니다.",
    },
}


# -----------------------------
# 음식 데이터
# -----------------------------
FOODS = {
    "비빔밥": {
        "emoji": "🥗",
        "type": "밥",
        "taste": "고소하고 다양한 재료의 맛",
        "description": "밥 위에 여러 나물과 채소, 고기 등을 올리고 고추장과 함께 비벼 먹는 음식이에요.",
        "good_for": "여러 재료를 한 번에 맛보고 싶은 사람",
    },
    "김치찌개": {
        "emoji": "🍲",
        "type": "찌개",
        "taste": "새콤하고 얼큰한 맛",
        "description": "김치와 두부, 돼지고기 등을 넣고 끓이는 한국의 대표적인 찌개예요.",
        "good_for": "따뜻하고 얼큰한 국물 음식을 좋아하는 사람",
    },
    "불고기": {
        "emoji": "🥩",
        "type": "고기",
        "taste": "달콤짭짤한 맛",
        "description": "얇게 썬 고기를 간장 양념에 재워 굽거나 볶아 먹는 음식이에요.",
        "good_for": "맵지 않고 달콤한 맛을 좋아하는 사람",
    },
    "떡볶이": {
        "emoji": "🍢",
        "type": "간식",
        "taste": "매콤달콤한 맛",
        "description": "떡을 고추장 양념 등에 넣어 조리하는 인기 있는 분식이에요.",
        "good_for": "매콤한 길거리 음식을 맛보고 싶은 사람",
    },
    "잡채": {
        "emoji": "🍜",
        "type": "면",
        "taste": "담백하고 달콤짭짤한 맛",
        "description": "당면과 채소, 고기 등을 볶아 만든 음식이에요.",
        "good_for": "다양한 채소와 쫄깃한 면을 좋아하는 사람",
    },
    "삼계탕": {
        "emoji": "🍗",
        "type": "국물",
        "taste": "진하고 담백한 맛",
        "description": "닭 안에 찹쌀과 재료를 넣어 푹 끓인 음식이에요.",
        "good_for": "든든하고 담백한 국물 음식을 원하는 사람",
    },
    "김밥": {
        "emoji": "🍙",
        "type": "간편식",
        "taste": "재료에 따라 다양함",
        "description": "김에 밥과 여러 가지 재료를 넣고 말아 한입 크기로 썬 음식이에요.",
        "good_for": "간편하게 먹을 수 있는 음식을 찾는 사람",
    },
    "전": {
        "emoji": "🥞",
        "type": "반찬",
        "taste": "고소하고 바삭한 맛",
        "description": "채소나 해산물, 고기 등을 반죽에 묻혀 부쳐 먹는 음식이에요.",
        "good_for": "고소한 반찬이나 간식을 좋아하는 사람",
    },
}


# -----------------------------
# 생활 한국어
# -----------------------------
PHRASES = {
    "인사": [
        ("안녕하세요.", "Hello."),
        ("만나서 반갑습니다.", "Nice to meet you."),
        ("안녕히 가세요.", "Goodbye."),
    ],
    "감사": [
        ("감사합니다.", "Thank you."),
        ("정말 고마워요.", "Thank you very much."),
        ("도와주셔서 감사합니다.", "Thank you for helping me."),
    ],
    "식당": [
        ("메뉴판 주세요.", "Could I have a menu, please?"),
        ("이거 하나 주세요.", "One of these, please."),
        ("계산해 주세요.", "Could I have the bill, please?"),
    ],
    "길 찾기": [
        ("지하철역이 어디예요?", "Where is the subway station?"),
        ("여기 어떻게 가요?", "How do I get there?"),
        ("천천히 말씀해 주세요.", "Please speak slowly."),
    ],
    "쇼핑": [
        ("이거 얼마예요?", "How much is this?"),
        ("카드로 결제할 수 있어요?", "Can I pay by card?"),
        ("다른 색도 있어요?", "Do you have another color?"),
    ],
}


# -----------------------------
# 번역 언어
# -----------------------------
LANGUAGES = {
    "한국어": "ko",
    "영어": "en",
    "일본어": "ja",
    "중국어(간체)": "zh-CN",
    "중국어(번체)": "zh-TW",
    "스페인어": "es",
    "프랑스어": "fr",
    "베트남어": "vi",
    "태국어": "th",
    "인도네시아어": "id",
    "독일어": "de",
    "러시아어": "ru",
    "이탈리아어": "it",
    "포르투갈어": "pt",
}


# -----------------------------
# 관광지 데이터
# -----------------------------
PLACES = {
    "서울": [
        {
            "name": "경복궁",
            "kind": "역사",
            "description": "조선 시대의 대표적인 궁궐로 한국의 전통 건축과 역사를 살펴볼 수 있어요.",
            "tip": "한복을 입고 방문하면 특별한 추억을 만들 수 있어요.",
        },
        {
            "name": "북촌한옥마을",
            "kind": "전통",
            "description": "한옥이 모여 있는 동네로 전통적인 서울의 모습을 느낄 수 있어요.",
            "tip": "실제 주민이 사는 곳이므로 조용히 둘러봐 주세요.",
        },
        {
            "name": "남산서울타워",
            "kind": "전망",
            "description": "서울의 풍경을 높은 곳에서 바라볼 수 있는 명소예요.",
            "tip": "해 질 무렵이나 야경 시간대가 인기가 많아요.",
        },
        {
            "name": "광장시장",
            "kind": "시장",
            "description": "다양한 한국 길거리 음식과 시장 분위기를 경험할 수 있어요.",
            "tip": "여러 음식을 조금씩 나누어 맛보는 것도 좋아요.",
        },
    ],
    "부산": [
        {
            "name": "해운대해수욕장",
            "kind": "바다",
            "description": "넓은 백사장과 바다 풍경으로 유명한 부산의 대표 명소예요.",
            "tip": "계절과 날씨에 맞는 옷을 준비해요.",
        },
        {
            "name": "감천문화마을",
            "kind": "문화",
            "description": "언덕을 따라 알록달록한 집과 예술 작품이 이어지는 마을이에요.",
            "tip": "주민 생활 공간을 존중하고 지정된 길로 다녀요.",
        },
        {
            "name": "자갈치시장",
            "kind": "시장",
            "description": "해산물과 부산의 활기찬 시장 문화를 경험할 수 있어요.",
            "tip": "음식 가격과 영업시간을 방문 전에 확인해요.",
        },
    ],
    "전주": [
        {
            "name": "전주한옥마을",
            "kind": "전통",
            "description": "전통 한옥과 공예, 한식을 경험할 수 있는 대표 관광지예요.",
            "tip": "한옥 골목에서는 다른 방문객과 주민을 배려해요.",
        },
        {
            "name": "경기전",
            "kind": "역사",
            "description": "조선 왕조의 역사와 관련된 유적을 살펴볼 수 있어요.",
            "tip": "관람 규칙과 촬영 안내를 확인해요.",
        },
    ],
    "제주": [
        {
            "name": "성산일출봉",
            "kind": "자연",
            "description": "화산 활동으로 만들어진 독특한 지형과 바다 풍경을 볼 수 있어요.",
            "tip": "탐방로와 기상 상황을 미리 확인해요.",
        },
        {
            "name": "협재해수욕장",
            "kind": "바다",
            "description": "맑은 바다와 아름다운 해변 풍경으로 잘 알려져 있어요.",
            "tip": "자연을 보호하고 쓰레기를 되가져가요.",
        },
        {
            "name": "동문시장",
            "kind": "시장",
            "description": "제주 특산물과 여러 먹거리를 둘러볼 수 있는 시장이에요.",
            "tip": "지역 특산물과 제철 음식을 찾아보세요.",
        },
    ],
    "경주": [
        {
            "name": "불국사",
            "kind": "역사",
            "description": "신라의 불교문화와 전통 건축을 살펴볼 수 있는 사찰이에요.",
            "tip": "조용히 관람하고 문화재를 만지지 않도록 해요.",
        },
        {
            "name": "첨성대",
            "kind": "역사",
            "description": "신라 시대
