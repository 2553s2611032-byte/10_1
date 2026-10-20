import streamlit as st
import requests
import random

st.set_page_config(
    page_title="다정한 한국 - 우리문화 추천 및 번역",
    page_icon="🇰🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    min-height: 82px;
    font-size: 21px;
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
    color: #243746;
}
.main-card {
    background: #FFFFFF;
    border: 2px solid #243746;
    border-radius: 26px;
    padding: 26px;
    margin: 10px 0 18px 0;
}
</style>
""", unsafe_allow_html=True)

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
            "description": "신라 시대 천문 관측과 관련된 역사 유적이에요.",
            "tip": "주변 유적과 함께 천천히 둘러보세요.",
        },
    ],
}

if "menu" not in st.session_state:
    st.session_state.menu = "🏠 시작 화면"


def set_menu(name):
    st.session_state.menu = name


with st.sidebar:
    st.markdown("# 🇰🇷 다정한 한국")
    st.caption("한국 생활과 여행을 도와주는 작은 안내서")
    st.divider()

    menu_items = [
        ("🏠 시작 화면", "🏠  시작 화면"),
        ("🇰🇷 우리나라의 문화", "🇰🇷  우리나라의 문화"),
        ("🗣️ 생활 한국어", "🗣️  생활 한국어"),
        ("🌐 번역기", "🌐  번역기"),
        ("🍜 음식 추천", "🍜  음식 추천"),
        ("🗺️ 관광지 추천", "🗺️  관광지 추천"),
    ]

    for key, label in menu_items:
        if st.button(label, key=f"menu_{key}", use_container_width=True):
            set_menu(key)

    st.divider()
    st.caption("원하는 메뉴를 눌러 시작해 보세요.")
    st.caption("※ 번역은 외부 무료 번역 서비스를 이용해요.")

st.markdown("# 다정한 한국")
st.markdown("한국의 문화와 생활 표현을 배우고, 음식과 여행지를 찾아보세요.")

if st.session_state.menu == "🏠 시작 화면":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## 반가워요! 👋")
    st.write(
        "이곳에서는 한국 문화 예절을 알아보고, 여행지와 음식을 추천받고, "
        "간단한 번역도 할 수 있어요."
    )
    st.write("왼쪽의 **큰 메뉴 버튼**을 눌러 원하는 기능으로 이동해 보세요.")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🇰🇷 문화 배우기")
        st.write("인사, 식사 예절, 대중교통 등 한국 생활에서 알아두면 좋은 내용을 확인해요.")
        if st.button("문화 알아보기", key="home_culture", use_container_width=True):
            set_menu("🇰🇷 우리나라의 문화")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🌐 간단 번역")
        st.write("한국어와 여러 언어 사이의 문장을 번역해 볼 수 있어요.")
        if st.button("번역기 열기", key="home_translate", use_container_width=True):
            set_menu("🌐 번역기")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### 🗺️ 여행 추천")
        st.write("지역을 선택하면 대표 관광지와 여행 팁을 볼 수 있어요.")
        if st.button("여행지 찾아보기", key="home_places", use_container_width=True):
            set_menu("🗺️ 관광지 추천")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 이 앱에서 할 수 있는 일")
    st.info(
        "문화 예절 알아보기 · 생활 한국어 표현 익히기 · 문장 번역하기 · "
        "한국 음식 추천받기 · 지역별 관광지 둘러보기"
    )

elif st.session_state.menu == "🇰🇷 우리나라의 문화":
    st.markdown("## 🇰🇷 우리나라의 문화")
    st.write("한국 생활에서 자주 만나는 예절과 문화를 주제별로 살펴보세요.")

    selected_culture = st.selectbox("궁금한 주제를 선택하세요", list(CULTURE.keys()))
    info = CULTURE[selected_culture]

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"### {info['emoji']} {selected_culture}")
    st.write(info["summary"])
    st.markdown("**알아두면 좋은 점**")

    for point in info["points"]:
        st.markdown(f"- {point}")

    st.markdown("**이럴 때 쓸 수 있어요**")
    st.success(info["phrase"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "문화와 예절은 사람이나 상황에 따라 다를 수 있어요. "
        "상대방을 존중하며 자연스럽게 배워 보세요."
    )

elif st.session_state.menu == "🗣️ 생활 한국어":
    st.markdown("## 🗣️ 생활 한국어")
    st.write("일상에서 자주 사용하는 표현과 뜻을 확인해 보세요.")

    topic = st.selectbox("상황 선택", list(PHRASES.keys()))

    for i, (korean, english) in enumerate(PHRASES[topic], start=1):
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown(f"### {i}. {korean}")
        st.write(f"영어 뜻: {english}")

        if st.button("이 표현을 번역기에 넣기", key=f"phrase_{topic}_{i}"):
            st.session_state["translate_text"] = korean
            set_menu("🌐 번역기")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.info("팁: '주세요', '감사합니다', '실례합니다' 같은 표현은 여러 상황에서 유용해요.")

elif st.session_state.menu == "🌐 번역기":
    st.markdown("## 🌐 번역기")
    st.write("문장을 입력하고 언어를 선택하면 번역 결과를 확인할 수 있어요.")

    lang_names = list(LANGUAGES.keys())
    left, right = st.columns(2)

    with left:
        source_name = st.selectbox("입력 언어", lang_names, index=0)

    with right:
        target_name = st.selectbox(
            "번역할 언어",
            lang_names,
            index=lang_names.index("영어"),
        )

    default_text = st.session_state.get("translate_text", "")
    user_text = st.text_area(
        "번역할 문장",
        value=default_text,
        height=160,
        placeholder="예: 안녕하세요. 한국에 처음 왔어요.",
    )

    if st.button("번역하기", type="primary", use_container_width=True):
        if not user_text.strip():
            st.warning("먼저 번역할 문장을 입력해 주세요.")

        elif source_name == target_name:
            st.info("입력 언어와 번역할 언어가 같아요. 다른 언어를 선택해 주세요.")

        else:
            try:
                with st.spinner("번역 중이에요..."):
                    response = requests.get(
                        "https://api.mymemory.translated.net/get",
                        params={
                            "q": user_text,
                            "langpair": (
                                f"{LANGUAGES[source_name]}|"
                                f"{LANGUAGES[target_name]}"
                            ),
                        },
                        timeout=15,
                    )
                    response.raise_for_status()
                    data = response.json()
                    translated = data.get("responseData", {}).get(
                        "translatedText", ""
                    )

                if translated:
                    st.markdown('<div class="main-card">', unsafe_allow_html=True)
                    st.markdown("### 번역 결과")
                    st.write(translated)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.caption(
                        "자동 번역은 문맥이나 고유명사를 정확히 옮기지 못할 수 있으니 "
                        "중요한 내용은 다시 확인해 주세요."
                    )
                else:
                    st.error("번역 결과를 가져오지 못했어요. 잠시 후 다시 시도해 주세요.")

            except requests.RequestException:
                st.error(
                    "번역 서비스에 연결하지 못했어요. 인터넷 연결을 확인하고 "
                    "다시 시도해 주세요."
                )

            except (ValueError, TypeError, KeyError):
                st.error("번역 결과를 읽는 중 문제가 생겼어요. 다른 문장으로 다시 시도해 주세요.")

    st.caption("이 앱은 공식 파파고 API가 아닌 MyMemory 무료 번역 서비스를 사용합니다.")

elif st.session_state.menu == "🍜 음식 추천":
    st.markdown("## 🍜 한국 음식 추천")
    st.write("좋아하는 맛이나 음식 종류를 선택해 어울리는 한국 음식을 찾아보세요.")

    taste_options = ["상관없음", "달콤짭짤", "매콤", "담백", "고소", "국물"]
    type_options = ["상관없음"] + sorted(
        {item["type"] for item in FOODS.values()}
    )

    col1, col2 = st.columns(2)

    with col1:
        taste = st.selectbox("좋아하는 맛", taste_options)

    with col2:
        food_type = st.selectbox("먹고 싶은 종류", type_options)

    filtered = []

    for name, item in FOODS.items():
        taste_ok = (
            taste == "상관없음"
            or (taste == "달콤짭짤" and "달콤짭짤" in item["taste"])
            or (
                taste == "매콤"
                and ("매콤" in item["taste"] or "얼큰" in item["taste"])
            )
            or (taste == "담백" and "담백" in item["taste"])
            or (taste == "고소" and "고소" in item["taste"])
            or (
                taste == "국물"
                and ("국물" in item["good_for"] or item["type"] in ["찌개", "국물"])
            )
        )

        type_ok = food_type == "상관없음" or item["type"] == food_type

        if taste_ok and type_ok:
            filtered.append((name, item))

    if st.button("음식 추천받기", type="primary", use_container_width=True):
        if filtered:
            random.shuffle(filtered)
            st.session_state["food_results"] = filtered[:3]
        else:
            st.session_state["food_results"] = []

    results = st.session_state.get("food_results")

    if results is None:
        results = filtered[:3]

    if not results:
        st.warning("선택한 조건에 맞는 음식이 없어요. 다른 조건을 골라 보세요.")

    else:
        for name, item in results:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.markdown(f"### {item['emoji']} {name}")
            st.write(item["description"])
            st.write(f"**맛:** {item['taste']}")
            st.write(f"**추천 대상:** {item['good_for']}")
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "음식에 포함된 재료는 가게마다 다를 수 있어요. "
        "알레르기가 있다면 주문 전에 재료를 확인해 주세요."
    )

elif st.session_state.menu == "🗺️ 관광지 추천":
    st.markdown("## 🗺️ 한국 관광지 추천")
    st.write("방문하고 싶은 지역과 여행 스타일을 골라 보세요.")

    region = st.selectbox("지역 선택", list(PLACES.keys()))
    all_kinds = sorted(
        {place["kind"] for places in PLACES.values() for place in places}
    )
    style = st.selectbox("여행 스타일", ["모두 보기"] + all_kinds)

    places = PLACES[region]

    if style != "모두 보기":
        places = [place for place in places if place["kind"] == style]

    if not places:
        st.warning(
            "해당 지역에는 선택한 유형의 추천지가 아직 없어요. "
            "'모두 보기'를 선택해 주세요."
        )

    for place in places:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown(f"### 📍 {place['name']}")
        st.markdown(f"**유형:** {place['kind']}")
        st.write(place["description"])
        st.info(f"여행 팁: {place['tip']}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("방문 전 운영 시간, 입장료, 교통편과 현장 안내를 확인해 주세요.")

st.divider()
st.caption("다정한 한국 · 한국 문화와 생활을 더 쉽게 알아보는 안내 앱")
