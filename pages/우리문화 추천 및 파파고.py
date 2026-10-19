
import streamlit as st
import requests
from urllib.parse import quote

st.set_page_config(
    page_title="다정한 한국 | K-Culture Bridge",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 디자인 ----------
st.markdown("""
<style>
.stApp {
    background: #F7F8F5;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: #234E43;
    color: white;
    padding: 2rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
}
.hero h1 {
    color: white;
    font-size: 2.2rem;
}
.hero p {
    color: #E4EEE8;
    font-size: 1rem;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E5E9E3;
}
.tip {
    background: #EAF2EC;
    border-left: 4px solid #477B65;
    padding: 12px 16px;
    border-radius: 8px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- 기본 데이터 ----------
ETIQUETTE = {
    "인사와 존댓말": [
        ("처음 만났을 때", "가볍게 고개를 숙여 인사하고 처음에는 존댓말을 사용해요.",
         "친해지기 전부터 반말을 쓰면 무례하게 느껴질 수 있어요.",
         "안녕하세요. 만나서 반갑습니다."),
        ("어른을 만났을 때", "상대방의 나이가 많거나 공식적인 자리라면 공손한 말투를 사용해요.",
         "나이만으로 상대의 관계를 단정하지 말고 상황을 살펴보세요.",
         "처음 뵙겠습니다."),
        ("감사와 사과", "도움을 받으면 감사 인사를 하고 실수했을 때는 정중하게 사과해요.",
         "고마운 마음이나 미안한 마음을 표현하는 것을 잊지 마세요.",
         "감사합니다. / 죄송합니다."),
    ],
    "식사 예절": [
        ("식사 시작", "함께 식사할 때는 어른이나 다른 사람이 식사를 시작하는지 살펴보면 좋아요.",
         "모든 가정과 상황에서 똑같은 규칙이 적용되는 것은 아니에요.",
         "먼저 드셔도 됩니다."),
        ("식사 도구", "밥과 국에는 보통 숟가락을, 반찬에는 젓가락을 사용해요.",
         "숟가락과 젓가락을 동시에 한 손에 쥐고 먹는 것은 일반적으로 피하는 편이에요.",
         "이 음식은 어떻게 먹나요?"),
        ("함께 나누어 먹기", "공용 음식은 집게나 공용 숟가락이 있다면 사용하는 것이 위생적이에요.",
         "음식 알레르기나 먹지 못하는 재료가 있다면 미리 알려주세요.",
         "이 음식에 어떤 재료가 들어 있나요?"),
    ],
    "공공장소": [
        ("대중교통", "버스나 지하철에서는 큰 소리의 통화나 음악을 피하고 줄을 지켜요.",
         "내리려는 사람을 먼저 보내면 서로 편해요.",
         "실례합니다. 지나가겠습니다."),
        ("줄 서기", "가게나 관공서에서는 차례를 기다리고 다른 사람의 순서를 존중해요.",
         "급하더라도 새치기는 피하는 것이 좋아요.",
         "마지막 순서가 어디인가요?"),
        ("쓰레기 분리배출", "지역과 건물의 분리배출 안내를 확인하고 종류별로 버려요.",
         "음식물 쓰레기와 일반 쓰레기의 구분은 지역별 안내를 확인하세요.",
         "이 쓰레기는 어디에 버리면 되나요?"),
    ],
    "학교와 직장": [
        ("시간 약속", "약속 시간에 맞춰 도착하고 늦을 것 같으면 미리 알려요.",
         "연락할 때는 늦는 이유와 도착 예정 시간을 알려주면 좋아요.",
         "죄송합니다. 조금 늦을 것 같습니다."),
        ("부탁하기", "상대방에게 요청할 때는 정중한 표현을 사용해요.",
         "부탁을 받는 사람의 상황도 존중해 주세요.",
         "도와주실 수 있을까요?"),
        ("잘 이해하지 못했을 때", "이해하지 못한 부분을 다시 설명해 달라고 요청해도 괜찮아요.",
         "모른다고 말하는 것은 잘못이 아니에요.",
         "죄송하지만, 다시 설명해 주시겠어요?"),
    ],
}

FOODS = [
    {"name": "비빔밥", "tags": ["채소", "담백한 맛", "밥"],
     "spice": "조절 가능", "desc": "밥과 여러 채소를 함께 먹는 음식이에요. 고추장을 따로 요청할 수 있어요.",
     "caution": "고추장, 달걀, 고기 등 재료를 확인하세요."},
    {"name": "불고기", "tags": ["달콤한 맛", "고기", "밥"],
     "spice": "대체로 맵지 않음", "desc": "얇게 썬 고기를 달콤짭짤한 양념에 재워 익혀요.",
     "caution": "일반적으로 소고기를 사용해요. 양념과 조리법을 확인하세요."},
    {"name": "김밥", "tags": ["밥", "간편식", "채소"],
     "spice": "제품에 따라 다름", "desc": "김에 밥과 여러 재료를 넣어 말아 만든 음식이에요.",
     "caution": "햄, 달걀, 어묵, 참기름 등이 들어갈 수 있어요."},
    {"name": "삼계탕", "tags": ["고기", "담백한 맛", "국물"],
     "spice": "대체로 맵지 않음", "desc": "닭과 찹쌀 등을 넣어 끓인 따뜻한 국물 요리예요.",
     "caution": "닭고기와 한약재 등 사용 재료를 확인하세요."},
    {"name": "잡채", "tags": ["채소", "달콤한 맛", "면"],
     "spice": "대체로 맵지 않음", "desc": "당면과 채소 등을 볶아 만드는 음식이에요.",
     "caution": "간장 양념에 밀이나 대두 성분이 포함될 수 있어요."},
    {"name": "김치찌개", "tags": ["매콤한 맛", "국물", "밥"],
     "spice": "매운 편", "desc": "김치를 넣어 끓이는 찌개로 밥과 함께 먹어요.",
     "caution": "돼지고기, 참치, 젓갈 등이 들어갈 수 있어요."},
    {"name": "칼국수", "tags": ["면", "국물", "담백한 맛"],
     "spice": "대체로 맵지 않음", "desc": "넓적한 밀가루 면을 국물에 넣어 끓인 음식이에요.",
     "caution": "밀이 포함되며 육수 재료도 확인하세요."},
    {"name": "떡볶이", "tags": ["매콤한 맛", "간식"],
     "spice": "매운 편", "desc": "떡을 양념에 졸여 만드는 인기 있는 간식이에요.",
     "caution": "고추장 양념이 맵고 어묵이나 밀 성분이 들어갈 수 있어요."},
]

PLACES = [
    {"name": "경복궁", "area": "서울", "type": "전통문화",
     "desc": "조선 시대의 궁궐을 둘러보며 한국의 역사와 건축을 배울 수 있어요.",
     "tip": "방문 시간과 휴궁일을 공식 안내에서 확인하세요."},
    {"name": "북촌한옥마을", "area": "서울", "type": "전통문화",
     "desc": "전통 한옥이 있는 동네예요. 실제 주민이 생활하는 공간도 있어요.",
     "tip": "조용히 관람하고 주거 공간의 사생활을 존중하세요."},
    {"name": "국립중앙박물관", "area": "서울", "type": "전통문화",
     "desc": "한국의 역사와 유물을 실내에서 알아보기 좋은 박물관이에요.",
     "tip": "전시 일정과 운영시간을 확인하세요."},
    {"name": "해운대해수욕장", "area": "부산", "type": "자연",
     "desc": "넓은 해변과 바다 풍경을 즐길 수 있어요.",
     "tip": "해수욕 가능 기간과 안전 안내를 확인하세요."},
    {"name": "감천문화마을", "area": "부산", "type": "도시체험",
     "desc": "알록달록한 집과 예술 작품으로 알려진 마을이에요.",
     "tip": "주민이 사는 곳이므로 소음과 촬영에 주의하세요."},
    {"name": "전주한옥마을", "area": "전주", "type": "전통문화",
     "desc": "한옥과 전통 음식, 공예 문화를 경험할 수 있는 곳이에요.",
     "tip": "주말에는 혼잡할 수 있으니 이동 시간을 여유 있게 잡으세요."},
    {"name": "제주 올레길", "area": "제주", "type": "자연",
     "desc": "제주의 바다와 마을 풍경을 걸으며 만날 수 있는 길이에요.",
     "tip": "코스 난이도와 날씨, 안전 정보를 확인하세요."},
    {"name": "인사동", "area": "서울", "type": "도시체험",
     "desc": "전통 공예품, 갤러리, 차 문화를 만날 수 있는 거리예요.",
     "tip": "상점별 운영시간과 가격을 확인하세요."},
]

LANGUAGES = {
    "영어": "en",
    "중국어(간체)": "zh-CN",
    "베트남어": "vi",
    "태국어": "th",
    "인도네시아어": "id",
    "일본어": "ja",
    "몽골어": "mn",
    "네팔어": "ne",
    "우즈베크어": "uz",
    "러시아어": "ru",
    "필리핀어": "tl",
    "한국어": "ko",
}

PHRASES = {
    "병원": [
        ("어디가 아프세요?", "Where does it hurt?"),
        ("알레르기가 있어요.", "I have an allergy."),
        ("통역이 필요합니다.", "I need an interpreter."),
    ],
    "학교": [
        ("다시 설명해 주세요.", "Please explain it again."),
        ("숙제는 언제까지인가요?", "When is the homework due?"),
        ("잘 이해하지 못했습니다.", "I didn't understand clearly."),
    ],
    "식당": [
        ("맵지 않게 해 주세요.", "Please make it not spicy."),
        ("고기를 빼 주세요.", "Please leave out the meat."),
        ("알레르기 유발 식재료가 있나요?", "Does this contain any allergens?"),
    ],
    "관공서": [
        ("이 서류를 작성하는 방법을 알려 주세요.", "Please tell me how to fill out this form."),
        ("통역을 요청할 수 있나요?", "Can I request an interpreter?"),
        ("예약이 필요하나요?", "Do I need an appointment?"),
    ],
}

# ---------- 사이드바 ----------
with st.sidebar:
    st.markdown("## 🌿 다정한 한국")
    st.caption("K-Culture Bridge")
    page = st.radio(
        "메뉴",
        ["홈", "한국 예절 배우기", "음식 추천", "관광지 추천", "생활 한국어 번역"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("서로 다른 문화가 편안하게 만나는 곳")
    st.caption("정보는 일반적인 안내이며, 지역·기관·개인에 따라 다를 수 있어요.")

# ---------- 공통 화면 ----------
def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def show_home():
    hero("한국 생활, 조금 더 편안하게 🌿",
         "한국의 문화와 일상을 알아보고, 나에게 맞는 음식과 여행지를 찾아보세요.")
    st.write("처음이라 낯설어도 괜찮아요. 필요한 정보를 하나씩 살펴봐요.")
    c1, c2, c3 = st.columns(3)
    c1.metric("문화 예절", "상황별 안내")
    c2.metric("한국 여행", "맞춤 추천")
    c3.metric("생활 한국어", "다국어 번역")
    st.markdown("### 무엇을 도와드릴까요?")
    a, b = st.columns(2)
    with a:
        if st.button("🙇 한국 예절 알아보기", use_container_width=True):
            st.session_state["page_jump"] = "한국 예절 배우기"
            st.rerun()
        if st.button("🍲 내 입맛에 맞는 음식 찾기", use_container_width=True):
            st.session_state["page_jump"] = "음식 추천"
            st.rerun()
    with b:
        if st.button("🗺️ 관광지 추천받기", use_container_width=True):
            st.session_state["page_jump"] = "관광지 추천"
            st.rerun()
        if st.button("💬 한국어 번역하기", use_container_width=True):
            st.session_state["page_jump"] = "생활 한국어 번역"
            st.rerun()
    st.markdown("### 오늘의 생활 표현")
    st.markdown('<div class="tip">“천천히 말씀해 주시겠어요?”<br>'
                '상대방의 말을 알아듣기 어려울 때 정중하게 사용할 수 있어요.</div>',
                unsafe_allow_html=True)

def show_etiquette():
    hero("🙇 한국 예절 배우기", "일상에서 자주 만나는 상황별 예절을 알아봐요.")
    category = st.selectbox("배우고 싶은 상황", list(ETIQUETTE.keys()))
    for title, good, avoid, phrase in ETIQUETTE[category]:
        with st.expander(title, expanded=True):
            st.success("이렇게 해 보세요: " + good)
            st.info("기억할 점: " + avoid)
            st.markdown(f"**쓸 수 있는 표현:** “{phrase}”")

def show_food():
    hero("🍲 내 입맛에 맞는 한국 음식", "매운맛과 식사 취향을 선택하면 음식 목록을 골라볼 수 있어요.")
    spice = st.selectbox("매운 음식은 어떤가요?",
                         ["모두 괜찮아요", "맵지 않은 음식", "매운 음식"])
    diet = st.selectbox("선호하는 음식 유형",
                        ["모두", "채소 중심", "고기 포함", "면 요리", "밥 요리"])
    taste = st.selectbox("좋아하는 맛",
                         ["상관없음", "담백한 맛", "달콤한 맛", "매콤한 맛"])
    results = []
    for food in FOODS:
        if spice == "맵지 않은 음식" and food["spice"] == "매운 편":
            continue
        if spice == "매운 음식" and food["spice"] != "매운 편":
            continue
        if diet == "채소 중심" and "채소" not in food["tags"]:
            continue
        if diet == "고기 포함" and "고기" not in food["tags"]:
            continue
        if diet == "면 요리" and "면" not in food["tags"]:
            continue
        if diet == "밥 요리" and "밥" not in food["tags"]:
            continue
        if taste != "상관없음" and taste not in food["tags"]:
            continue
        results.append(food)

    st.markdown(f"### 추천 음식 {len(results)}가지")
    if not results:
        st.warning("선택한 조건에 맞는 음식이 없어요. 다른 취향을 선택해 보세요.")
    for food in results:
        with st.container(border=True):
            st.subheader(food["name"])
            st.caption(f'맵기: {food["spice"]} · 특징: {", ".join(food["tags"])}')
            st.write(food["desc"])
            st.warning("재료 확인: " + food["caution"])
    st.caption("음식의 조리법은 식당마다 다를 수 있어요. 알레르기·종교·식단 제한이 있다면 주문 전 직원에게 꼭 확인하세요.")

def show_places():
    hero("🗺️ 나에게 맞는 한국 여행", "관심 있는 지역과 여행 스타일을 선택해 보세요.")
    area = st.selectbox("지역", ["전체", "서울", "부산", "전주", "제주"])
    kind = st.selectbox("여행 스타일", ["전체", "전통문화", "자연", "도시체험"])
    results = [
        p for p in PLACES
        if (area == "전체" or p["area"] == area)
        and (kind == "전체" or p["type"] == kind)
    ]
    st.markdown(f"### 추천 장소 {len(results)}곳")
    if not results:
        st.info("조건에 맞는 장소가 없어요. 선택을 바꿔보세요.")
    for place in results:
        with st.container(border=True):
            st.subheader(place["name"])
            st.caption(f'{place["area"]} · {place["type"]}')
            st.write(place["desc"])
            st.info("방문 팁: " + place["tip"])
            search_url = "https://www.google.com/maps/search/?api=1&query=" + quote(place["name"] + " 대한민국")
            st.link_button("지도에서 위치 찾기", search_url)
    st.caption("방문 전 공식 사이트에서 운영시간, 휴무일, 입장료와 교통편을 확인하세요.")

def translate_text(text, target_code):
    """무료 번역 서비스 요청. 실패 시 호출한 화면에서 오류를 안내합니다."""
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"ko|{target_code}",
    }
    response = requests.get(url, params=params, timeout=12)
    response.raise_for_status()
    data = response.json()
    translated = data.get("responseData", {}).get("translatedText")
    if not translated:
        raise ValueError("번역 결과가 비어 있습니다.")
    if data.get("responseStatus", 200) != 200:
        raise ValueError("번역 서비스에서 요청을 처리하지 못했습니다.")
    return translated

def show_translate():
    hero("💬 생활 한국어 번역", "한국어 표현을 다른 언어로 바꾸고, 생활에 필요한 문장도 찾아보세요.")
    st.caption("무료 외부 번역 서비스를 사용합니다. 민감한 개인정보나 비밀번호는 입력하지 마세요.")
    target_name = st.selectbox("번역할 언어", list(LANGUAGES.keys()))
    target_code = LANGUAGES[target_name]

    with st.form("translation_form"):
        source = st.text_area(
            "번역할 한국어",
            placeholder="예: 병원에 가고 싶은데 어디로 가야 하나요?",
            max_chars=3000,
            height=140,
        )
        submitted = st.form_submit_button("번역하기", use_container_width=True)

    if submitted:
        if not source.strip():
            st.warning("번역할 문장을 입력해 주세요.")
        elif len(source.strip()) > 3000:
            st.warning("문장을 3000자 이내로 입력해 주세요.")
        elif target_code == "ko":
            st.info("한국어를 선택했어요. 원문을 그대로 확인하세요.")
            st.text_area("결과", source.strip(), height=120)
        else:
            with st.spinner("번역 중입니다..."):
                try:
                    result = translate_text(source.strip(), target_code)
                    st.markdown("### 번역 결과")
                    st.text_area("번역된 문장", result, height=140)
                    st.caption("자동 번역 결과는 부정확할 수 있어요. 중요한 안내는 담당자나 전문 통역사에게 확인하세요.")
                except requests.Timeout:
                    st.error("번역 요청 시간이 초과됐어요. 잠시 후 다시 시도해 주세요.")
                except requests.RequestException:
                    st.error("번역 서비스에 연결할 수 없어요. 인터넷 연결을 확인한 뒤 다시 시도해 주세요.")
                except (ValueError, TypeError, KeyError):
                    st.error("번역 결과를 읽을 수 없어요. 다른 문장으로 다시 시도해 주세요.")
                except Exception:
                    st.error("예상하지 못한 오류가 발생했어요. 잠시 후 다시 시도해 주세요.")

    st.divider()
    st.markdown("### 상황별 바로 쓰는 표현")
    situation = st.selectbox("상황 선택", list(PHRASES.keys()))
    for korean, english in PHRASES[situation]:
        with st.container(border=True):
            st.write("🇰🇷 " + korean)
            st.caption("영어 참고 표현: " + english)
            st.button(
                "이 문장을 번역 입력창에 사용",
                key=f"use_{situation}_{korean}",
                on_click=lambda sentence=korean: st.session_state.update({
                    "phrase_to_translate": sentence
                }),
            )
    if "phrase_to_translate" in st.session_state:
        st.info("선택한 표현: " + st.session_state["phrase_to_translate"])
        st.caption("위 번역 입력창에 복사해 사용해 보세요.")

# ---------- 페이지 표시 ----------
if "page_jump" in st.session_state:
    selected_page = st.session_state.pop("page_jump")
else:
    selected_page = page

if selected_page == "홈":
    show_home()
elif selected_page == "한국 예절 배우기":
    show_etiquette()
elif selected_page == "음식 추천":
    show_food()
elif selected_page == "관광지 추천":
    show_places()
elif selected_page == "생활 한국어 번역":
    show_translate()

st.divider()
st.caption("다정한 한국 · 문화 안내는 참고용이며, 번역은 공식 통역을 대체하지 않습니다.")

