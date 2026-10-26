
import streamlit as st
import random

st.set_page_config(
    page_title="다정한 한국 - 우리문화 추천",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------
# 디자인
# --------------------------------
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
div[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    min-height: 72px;
    font-size: 19px;
    font-weight: 700;
    border-radius: 16px;
    border: 2px solid #243746;
    background: white;
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
    background: white;
    border: 2px solid #C7DCEC;
    border-radius: 22px;
    padding: 22px;
    margin: 10px 0 18px 0;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #A9C8DE;
    border-radius: 15px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------
# 한국 문화 자료
# --------------------------------
CULTURE = {
    "인사와 예절": {
        "emoji": "🙇",
        "summary": "한국에서는 인사와 상대방을 존중하는 태도를 중요하게 여겨요.",
        "points": [
            "처음 만난 사람에게는 '안녕하세요'라고 인사해요.",
            "어른이나 처음 만난 사람에게는 존댓말을 쓰는 것이 무난해요.",
            "감사하거나 사과할 때는 말로 마음을 표현해요.",
            "악수나 인사 방식은 상대방의 상황과 문화를 존중해요.",
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
        "tip": "음식을 함께 먹을 때는 다른 사람의 식사 속도도 배려해요.",
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
    "명절과 전통문화": {
        "emoji": "🎎",
        "summary": "설날과 추석은 가족과 함께 보내는 대표적인 한국 명절이에요.",
        "points": [
            "설날에는 떡국을 먹거나 가족끼리 새해 인사를 나누기도 해요.",
            "추석에는 송편을 먹고 가족과 시간을 보내기도 해요.",
            "한복은 한국의 전통 의상이에요.",
            "세배는 설날에 어른께 새해 인사를 드리는 전통이에요.",
            "명절을 보내는 방식은 가정마다 다를 수 있어요.",
        ],
        "tip": "전통문화를 체험할 때는 각 장소의 안내와 규칙을 확인해요.",
    },
    "집과 이웃 생활": {
        "emoji": "🏡",
        "summary": "공동주택이 많은 한국에서는 이웃과 생활 공간을 배려하는 것이 중요해요.",
        "points": [
            "다른 사람의 집에 방문하기 전에는 미리 연락해요.",
            "집에 들어갈 때 신발을 벗는 경우가 많아요.",
            "아파트와 공동주택에서는 늦은 시간의 큰 소음을 피해요.",
            "공용 공간은 깨끗하게 사용해요.",
            "물건을 사용하기 전에는 주인의 허락을 구해요.",
        ],
        "tip": "집마다 규칙이 다를 수 있으니 집주인에게 먼저 확인해요.",
    },
    "쓰레기 분리배출": {
        "emoji": "♻️",
        "summary": "한국에서는 쓰레기를 종류에 따라 나누어 버리는 경우가 많아요.",
        "points": [
            "일반 쓰레기와 재활용품을 구분해요.",
            "종이, 유리, 금속, 플라스틱 등은 지역의 배출 기준에 따라 분리해요.",
            "음식물 쓰레기는 지역별 기준에 맞게 배출해요.",
            "종량제 봉투 사용 여부와 배출 장소를 확인해요.",
            "배출 요일과 세부 규칙은 지역마다 다를 수 있어요.",
        ],
        "tip": "거주하는 지역의 구청이나 시청 홈페이지에서 배출 규칙을 확인해요.",
    },
    "한국의 대중적인 문화": {
        "emoji": "🎤",
        "summary": "한국에서는 다양한 대중문화와 여가 활동을 즐길 수 있어요.",
        "points": [
            "K-팝과 한국 드라마는 해외에서도 널리 알려져 있어요.",
            "노래방은 친구나 가족과 노래를 즐기는 공간이에요.",
            "전통시장에서는 지역 음식과 생활 문화를 경험할 수 있어요.",
            "공원과 산책로에서 걷거나 운동하는 사람도 많아요.",
            "모든 사람이 같은 취미나 문화를 좋아하는 것은 아니에요.",
        ],
        "tip": "관심 있는 문화부터 체험하면 한국 생활을 더 즐겁게 알아갈 수 있어요.",
    },
}


# --------------------------------
# 음식 추천 자료
# --------------------------------
FOODS = {
    "불고기": {
        "emoji": "🥩",
        "type": "고기",
        "taste": ["달콤짭짤", "담백"],
        "description": "얇게 썬 고기를 간장 양념에 재워 굽거나 볶는 음식이에요.",
        "good_for": "맵지 않은 고기 요리를 좋아하는 사람",
        "caution": "고기 종류와 양념 재료를 확인해요.",
    },
    "비빔밥": {
        "emoji": "🥗",
        "type": "밥",
        "taste": ["담백", "고소", "매콤"],
        "description": "밥에 채소와 여러 재료를 올려 양념과 함께 비벼 먹어요.",
        "good_for": "다양한 채소와 재료를 함께 먹고 싶은 사람",
        "caution": "고추장은 따로 요청할 수 있는지 확인해요.",
    },
    "김밥": {
        "emoji": "🍙",
        "type": "간편식",
        "taste": ["담백", "고소"],
        "description": "김에 밥과 채소, 달걀 등 여러 재료를 넣어 말아요.",
        "good_for": "간편하게 식사하거나 간식을 먹고 싶은 사람",
        "caution": "햄, 달걀, 참기름 등 포함 재료를 확인해요.",
    },
    "잡채": {
        "emoji": "🍜",
        "type": "면",
        "taste": ["달콤짭짤", "고소"],
        "description": "당면과 채소 등을 볶아 만든 음식으로 잔치에도 자주 등장해요.",
        "good_for": "쫄깃한 면과 채소를 좋아하는 사람",
        "caution": "고기나 간장 등 양념 재료를 확인해요.",
    },
    "삼계탕": {
        "emoji": "🍲",
        "type": "국물",
        "taste": ["담백"],
        "description": "닭 안에 찹쌀 등을 넣고 푹 끓여 만든 음식이에요.",
        "good_for": "따뜻하고 담백한 국물을 좋아하는 사람",
        "caution": "닭고기와 사용된 약재 등 재료를 확인해요.",
    },
    "김치찌개": {
        "emoji": "🥘",
        "type": "찌개",
        "taste": ["매콤"],
        "description": "김치와 두부, 고기 등을 넣고 끓이는 대표적인 찌개예요.",
        "good_for": "매콤하고 따뜻한 국물을 좋아하는 사람",
        "caution": "김치와 양념이 맵거나 짤 수 있어요.",
    },
    "떡볶이": {
        "emoji": "🍢",
        "type": "간식",
        "taste": ["매콤", "달콤짭짤"],
        "description": "떡을 양념에 넣고 조리하는 인기 있는 한국 간식이에요.",
        "good_for": "매콤달콤한 길거리 음식을 맛보고 싶은 사람",
        "caution": "매운 정도를 확인하고 어묵 등 재료도 살펴봐요.",
    },
    "파전": {
        "emoji": "🥞",
        "type": "간식",
        "taste": ["고소", "담백"],
        "description": "파와 반죽을 부쳐 만드는 음식으로 해산물을 넣기도 해요.",
        "good_for": "고소한 부침 요리를 좋아하는 사람",
        "caution": "밀가루, 달걀, 해산물 포함 여부를 확인해요.",
    },
    "갈비탕": {
        "emoji": "🍲",
        "type": "국물",
        "taste": ["담백"],
        "description": "소갈비를 넣고 푹 끓여 만드는 국물 음식이에요.",
        "good_for": "고기와 맑은 국물을 좋아하는 사람",
        "caution": "소고기와 육수 재료를 확인해요.",
    },
    "팥빙수": {
        "emoji": "🍧",
        "type": "디저트",
        "taste": ["달콤짭짤"],
        "description": "얼음을 곱게 갈고 팥이나 과일 등 여러 재료를 올린 디저트예요.",
        "good_for": "시원하고 달콤한 간식을 좋아하는 사람",
        "caution": "우유나 견과류 등 토핑 재료를 확인해요.",
    },
}


# --------------------------------
# 관광지 추천 자료
# --------------------------------
PLACES = {
    "서울": [
        {
            "name": "경복궁",
            "kind": "역사",
            "description": "조선 시대의 대표적인 궁궐로 전통 건축과 역사를 살펴볼 수 있어요.",
            "tip": "방문 전 휴관일과 관람 시간을 확인해요.",
        },
        {
            "name": "북촌한옥마을",
            "kind": "전통",
            "description": "전통 한옥이 모여 있어 옛 서울의 분위기를 느낄 수 있어요.",
            "tip": "주민이 실제로 생활하는 곳이므로 조용히 둘러봐요.",
        },
        {
            "name": "남산서울타워",
            "kind": "자연·전망",
            "description": "서울 시내 풍경과 야경을 감상할 수 있는 명소예요.",
            "tip": "날씨와 교통편을 확인하고 방문해요.",
        },
        {
            "name": "광장시장",
            "kind": "시장·음식",
            "description": "한국의 전통시장 분위기와 여러 가지 먹거리를 경험할 수 있어요.",
            "tip": "음식 가격과 영업시간을 미리 확인해요.",
        },
        {
            "name": "국립중앙박물관",
            "kind": "역사",
            "description": "한국을 비롯한 다양한 문화와 역사 유물을 살펴볼 수 있어요.",
            "tip": "전시와 관람 정보를 홈페이지에서 확인해요.",
        },
    ],
    "부산": [
        {
            "name": "해운대해수욕장",
            "kind": "자연·바다",
            "description": "넓은 백사장과 바다 풍경으로 유명한 부산의 명소예요.",
            "tip": "해수욕장 이용 기간과 안전 안내를 확인해요.",
        },
        {
            "name": "감천문화마을",
            "kind": "전통·문화",
            "description": "언덕을 따라 다양한 색상의 집과 예술 작품이 이어져요.",
            "tip": "주민 생활 공간을 존중하며 지정된 길로 다녀요.",
        },
        {
            "name": "자갈치시장",
            "kind": "시장·음식",
            "description": "부산의 해산물과 활기찬 시장 문화를 경험할 수 있어요.",
            "tip": "음식 가격과 영업시간을 확인해요.",
        },
        {
            "name": "광안리해수욕장",
            "kind": "자연·바다",
            "description": "바다와 광안대교의 풍경으로 잘 알려져 있어요.",
            "tip": "야간 방문 시 귀가 교통편을 확인해요.",
        },
    ],
    "전주": [
        {
            "name": "전주한옥마을",
            "kind": "전통·문화",
            "description": "전통 한옥과 공예, 한국 음식을 경험할 수 있어요.",
            "tip": "한옥 골목에서 주민과 다른 방문객을 배려해요.",
        },
        {
            "name": "경기전",
            "kind": "역사",
            "description": "조선 왕조와 관련된 역사와 유적을 살펴볼 수 있어요.",
            "tip": "관람 규칙과 촬영 안내를 확인해요.",
        },
        {
            "name": "전주 남부시장",
            "kind": "시장·음식",
            "description": "지역 먹거리와 전통시장의 분위기를 즐길 수 있어요.",
            "tip": "시장 운영 시간과 점포별 영업 여부를 확인해요.",
        },
    ],
    "제주": [
        {
            "name": "성산일출봉",
            "kind": "자연·바다",
            "description": "화산 활동으로 만들어진 독특한 지형과 바다 풍경을 볼 수 있어요.",
            "tip": "탐방로 운영 여부와 기상 상황을 확인해요.",
        },
        {
            "name": "협재해수욕장",
            "kind": "자연·바다",
            "description": "맑은 바다와 아름다운 해변 풍경으로 알려져 있어요.",
            "tip": "자연을 보호하고 쓰레기를 되가져가요.",
        },
        {
            "name": "동문시장",
            "kind": "시장·음식",
            "description": "제주 특산물과 다양한 먹거리를 둘러볼 수 있어요.",
            "tip": "제철 음식과 지역 특산물을 찾아보세요.",
        },
    ],
    "경주": [
        {
            "name": "불국사",
            "kind": "역사",
            "description": "신라의 불교문화와 전통 건축을 살펴볼 수 있는 사찰이에요.",
            "tip": "조용히 관람하고 문화재를 소중히 다뤄요.",
        },
        {
            "name": "첨성대",
            "kind": "역사",
            "description": "신라 시대의 천문 관측과 관련된 역사 유적이에요.",
            "tip": "주변 유적과 함께 둘러보면 좋아요.",
        },
        {
            "name": "동궁과 월지",
            "kind": "역사·자연",
            "description": "신라 왕궁의 별궁 터와 아름다운 연못을 볼 수 있어요.",
            "tip": "야간 관람 여부와 운영 시간을 확인해요.",
        },
    ],
}


# --------------------------------
# 메뉴 관리
# --------------------------------
MENU_ITEMS = [
    "🏠 시작 화면",
    "🇰🇷 한국 문화와 예절",
    "🍜 맞춤 음식 추천",
    "🗺️ 관광지 추천",
]

if "menu" not in st.session_state:
    st.session_state.menu = "🏠 시작 화면"


def set_menu(name):
    st.session_state.menu = name


with st.sidebar:
    st.markdown("# 🇰🇷 다정한 한국")
    st.caption("한국 문화와 생활을 알아보는 안내서")
    st.divider()

    for item in MENU_ITEMS:
        if st.button(
            item,
            key=f"menu_{item}",
            use_container_width=True,
        ):
            set_menu(item)
            st.rerun()

    st.divider()
    st.caption("문화와 예절을 배우고")
    st.caption("나에게 맞는 음식과 여행지를 찾아보세요!")


# --------------------------------
# 공통 상단
# --------------------------------
st.markdown("# 다정한 한국")
st.markdown(
    "한국의 문화를 이해하고, 새로운 음식과 여행지를 발견해 보세요."
)


# --------------------------------
# 시작 화면
# --------------------------------
if st.session_state.menu == "🏠 시작 화면":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## 반가워요! 👋")
    st.write(
        "한국에서 생활하거나 한국을 여행하는 사람들을 위해 "
        "문화와 예절, 음식, 관광지 정보를 소개하는 공간이에요."
    )
    st.write(
        "왼쪽 메뉴에서 궁금한 내용을 선택하거나 "
        "아래 버튼을 눌러 시작해 보세요."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🇰🇷 문화와 예절")
        st.write("인사, 식사, 명절, 주거 생활과 분리배출을 알아봐요.")
        if st.button("문화 알아보기", key="home_culture",
                     use_container_width=True):
            set_menu("🇰🇷 한국 문화와 예절")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🍜 음식 추천")
        st.write("좋아하는 맛과 음식 종류에 맞는 한국 음식을 찾아요.")
        if st.button("음식 추천받기", key="home_food",
                     use_container_width=True):
            set_menu("🍜 맞춤 음식 추천")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🗺️ 여행지 추천")
        st.write("지역과 여행 스타일에 맞는 관광지를 살펴봐요.")
        if st.button("여행지 둘러보기", key="home_places",
                     use_container_width=True):
            set_menu("🗺️ 관광지 추천")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 이 앱의 주요 기능")
    st.info(
        "한국 문화 배우기 · 생활 예절 확인하기 · "
        "취향별 한국 음식 추천 · 지역별 관광지 찾기"
    )

    st.markdown("## 한국 생활 첫걸음")
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 기억하면 좋은 세 가지")
    st.write("🙇 인사할 때는 '안녕하세요'라고 말해요.")
    st.write("♻️ 쓰레기는 지역별 분리배출 규칙을 확인해요.")
    st.write("🚌 대중교통에서는 차례와 다른 사람을 배려해요.")
    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------
# 한국 문화와 예절
# --------------------------------
elif st.session_state.menu == "🇰🇷 한국 문화와 예절":
    st.markdown("## 🇰🇷 한국 문화와 예절")
    st.write(
        "한국 생활에서 자주 접하는 문화를 주제별로 살펴보세요."
    )

    topic = st.selectbox(
        "알아보고 싶은 주제",
        list(CULTURE.keys()),
    )
    info = CULTURE[topic]

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"### {info['emoji']} {topic}")
    st.write(info["summary"])

    st.markdown("#### 알아두면 좋은 내용")
    for point in info["points"]:
        st.markdown(f"- {point}")

    st.markdown("#### 생활 속 실천 팁")
    st.info(info["tip"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "문화와 예절은 가정과 개인, 상황에 따라 다를 수 있어요. "
        "서로의 차이를 존중하며 알아가 보세요."
    )


# --------------------------------
# 맞춤 음식 추천
# --------------------------------
elif st.session_state.menu == "🍜 맞춤 음식 추천":
    st.markdown("## 🍜 나에게 맞는 한국 음식")
    st.write("원하는 맛과 음식 종류를 선택해 보세요.")

    col1, col2 = st.columns(2)

    with col1:
        taste = st.selectbox(
            "좋아하는 맛",
            ["상관없음", "달콤짭짤", "매콤", "담백", "고소"],
        )

    with col2:
        food_type = st.selectbox(
            "먹고 싶은 음식 종류",
            ["상관없음"] + sorted(
                {food["type"] for food in FOODS.values()}
            ),
        )

    if st.button(
        "음식 추천받기",
        type="primary",
        use_container_width=True,
    ):
        results = []

        for name, food in FOODS.items():
            taste_ok = (
                taste == "상관없음"
                or taste in food["taste"]
            )
            type_ok = (
                food_type == "상관없음"
                or food["type"] == food_type
            )

            if taste_ok and type_ok:
                results.append((name, food))

        random.shuffle(results)
        st.session_state.food_results = results[:4]

    # 선택 조건이 바뀌면 이전 결과를 그대로 보여주지 않도록
    # 현재 조건으로 결과를 다시 계산해 표시해요.
    results = []

    for name, food in FOODS.items():
        taste_ok = (
            taste == "상관없음"
            or taste in food["taste"]
        )
        type_ok = (
            food_type == "상관없음"
            or food["type"] == food_type
        )
        if taste_ok and type_ok:
            results.append((name, food))

    if "food_results" in st.session_state:
        saved = st.session_state.food_results
        valid_names = {name for name, food in results}
        saved = [
            (name, food) for name, food in saved
            if name in valid_names
        ]
        if saved:
            results = saved

    if not results:
        st.warning(
            "조건에 맞는 음식이 없어요. 다른 맛이나 종류를 선택해 보세요."
        )
    else:
        for name, food in results:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.markdown(f"### {food['emoji']} {name}")
            st.write(food["description"])
            st.write(f"**음식 종류:** {food['type']}")
            st.write(f"**맛:** {', '.join(food['taste'])}")
            st.write(f"**추천 대상:** {food['good_for']}")
            st.warning(f"**재료 확인:** {food['caution']}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "음식의 조리법과 재료는 가게마다 다를 수 있어요. "
        "알레르기나 식단 제한이 있다면 주문 전에 꼭 확인해 주세요."
    )


# --------------------------------
# 관광지 추천
# --------------------------------
elif st.session_state.menu == "🗺️ 관광지 추천":
    st.markdown("## 🗺️ 한국 관광지 추천")
    st.write("방문하고 싶은 지역과 여행 스타일을 선택해 보세요.")

    col1, col2 = st.columns(2)

    with col1:
        region = st.selectbox(
            "방문할 지역",
            list(PLACES.keys()),
        )

    with col2:
        all_kinds = sorted({
            place["kind"]
            for places in PLACES.values()
            for place in places
        })
        style = st.selectbox(
            "여행 스타일",
            ["모두 보기"] + all_kinds,
        )

    places = PLACES[region]

    if style != "모두 보기":
        places = [
            place for place in places
            if style in place["kind"]
        ]

    st.markdown(f"### 📍 {region} 추천 장소")

    if not places:
        st.warning("해당 조건에 맞는 장소가 없어요.")
    else:
        for place in places:
            st.markdown(
                '<div class="main-card">',
                unsafe_allow_html=True,
            )
            st.markdown(f"### 📌 {place['name']}")
            st.write(f"**여행 유형:** {place['kind']}")
            st.write(place["description"])
            st.info(f"여행 팁: {place['tip']}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "관광지의 운영 시간, 입장료, 교통편은 변경될 수 있어요. "
        "방문 전에 공식 안내를 확인해 주세요."
    )


# --------------------------------
# 하단 안내
# --------------------------------
st.divider()
st.caption(
    "다정한 한국 | 한국 문화와 생활을 알아보고 "
    "음식과 여행지를 추천받는 안내 앱"
)
