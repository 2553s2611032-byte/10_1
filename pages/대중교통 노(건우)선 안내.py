import streamlit as st
from urllib.parse import quote, urlencode
import html

st.set_page_config(
    page_title="SmartRoute | 다국어 길찾기",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

LANGUAGES = {
    "한국어": "ko", "English": "en", "日本語": "ja", "中文（简体）": "zh-CN",
    "中文（繁體）": "zh-TW", "Español": "es", "Français": "fr", "Deutsch": "de",
    "हिन्दी": "hi", "العربية": "ar", "Português": "pt", "Русский": "ru",
    "Tiếng Việt": "vi", "ไทย": "th", "Bahasa Indonesia": "id", "Türkçe": "tr",
    "Italiano": "it", "বাংলা": "bn", "اردو": "ur", "မြန်မာ": "my",
    "नेपाली": "ne", "Filipino": "tl", "Українська": "uk", "فارسی": "fa",
    "Kiswahili": "sw", "Nederlands": "nl", "Polski": "pl", "Svenska": "sv",
    "עברית": "he", "Ελληνικά": "el", "ಕನ್ನಡ": "kn", "தமிழ்": "ta",
    "తెలుగు": "te", "मराठी": "mr", "ગુજરાતી": "gu", "ಕನ್ನಡ": "kn",
}

TEXT = {
    "한국어": {
        "tagline": "버스·지하철부터 도보·항공·선박까지, 이동 방법을 한곳에서 비교하세요.",
        "origin": "출발지", "destination": "도착지", "lang": "화면 언어",
        "mode": "이동 수단", "all": "모든 이동 수단 비교", "find": "길찾기 만들기",
        "tip": "장소 이름과 도시/지역을 함께 입력하면 더 정확합니다. 예: 서울역, 서울",
        "routes": "추천 경로", "open": "지도에서 길찾기 열기", "fast": "빠른 경로",
        "safe": "안전 우선 확인", "access": "접근성·건물 내부 길찾기",
        "access_note": "엘리베이터, 휠체어 경로, 건물 내부 통로 정보는 지도 데이터와 장소에 따라 제공 여부가 다릅니다. 아래 검색 링크에서 현장 정보를 확인하세요.",
        "limitations": "중요한 안내", "limit_note": "이 앱은 지도 서비스로 연결해 경로를 확인하도록 돕습니다. 실제 안전도, 엘리베이터 작동 여부, 건물 내부 길을 독자적으로 검증하거나 보장하지 않습니다. 출발 전 현지 표지판과 운영 정보를 확인하세요.",
        "walk": "도보", "transit": "버스·지하철", "drive": "자동차·택시", "bike": "자전거",
        "flight": "비행기", "boat": "배·페리", "choose": "원하는 이동 수단을 선택하세요.",
        "access_search": "접근성·엘리베이터 정보 검색", "indoor_search": "건물 내부 길찾기 정보 검색",
        "flight_note": "항공편은 날짜, 공항, 항공사에 따라 달라집니다. 항공편 검색을 열어 확인하세요.",
        "boat_note": "배·페리는 운항 노선이 있는 지역에서만 이용할 수 있습니다. 노선과 시간표를 확인하세요.",
        "empty": "출발지와 도착지를 모두 입력한 다음 버튼을 눌러 주세요.",
    },
    "English": {
        "tagline": "Compare bus, subway, taxi, walking, flights, and ferries in one place.",
        "origin": "Starting point", "destination": "Destination", "lang": "Interface language",
        "mode": "Travel mode", "all": "Compare all modes", "find": "Build my route",
        "tip": "Include a city or region for better results. Example: Seoul Station, Seoul",
        "routes": "Route options", "open": "Open directions in Maps", "fast": "Fast route",
        "safe": "Safety-first check", "access": "Accessibility and indoor navigation",
        "access_note": "Elevator, wheelchair-accessible, and indoor-route data varies by place and map provider. Check the links below for local details.",
        "limitations": "Important note", "limit_note": "This app links to map services; it does not independently verify or guarantee safety, elevator availability, or indoor directions. Check local signs and operating information before travelling.",
        "walk": "Walking", "transit": "Bus / subway", "drive": "Car / taxi", "bike": "Bicycle",
        "flight": "Flight", "boat": "Boat / ferry", "choose": "Choose a travel mode.",
        "access_search": "Search accessibility and elevators", "indoor_search": "Search indoor navigation",
        "flight_note": "Flights depend on dates, airports, and airlines. Open a flight search to check options.",
        "boat_note": "Boats and ferries are available only where routes operate. Check routes and timetables.",
        "empty": "Enter both locations, then press the button.",
    },
}
# For languages without a hand-written interface translation, the app keeps the interface in English.
# The chosen language is still used as a Google Maps language hint where supported.

MODE_LABELS = {
    "도보 / Walking": "walking",
    "버스·지하철 / Transit": "transit",
    "자동차·택시 / Car or taxi": "driving",
    "자전거 / Bicycle": "bicycling",
    "비행기 / Flight search": "flight",
    "배·페리 / Boat or ferry": "boat",
}

def maps_directions_url(origin, destination, mode, lang_code):
    params = {"api": "1", "origin": origin, "destination": destination}
    if mode in ("walking", "transit", "driving", "bicycling"):
        params["travelmode"] = mode
    if lang_code:
        params["hl"] = lang_code
    return "https://www.google.com/maps/dir/?" + urlencode(params)

def maps_search_url(query, lang_code):
    params = {"api": "1", "query": query}
    if lang_code:
        params["hl"] = lang_code
    return "https://www.google.com/maps/search/?" + urlencode(params)

def google_flights_url(origin, destination):
    # Search link rather than an invented route or fare.
    q = quote(f"flights from {origin} to {destination}")
    return f"https://www.google.com/search?q={q}"

def ferry_search_url(origin, destination):
    q = quote(f"ferry or boat from {origin} to {destination}")
    return f"https://www.google.com/search?q={q}"

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1200px;}
.hero {padding: 1.4rem 1.5rem; border-radius: 18px; background: linear-gradient(120deg,#e8f4ff,#f1fbf5); border: 1px solid #d9e8ee;}
.hero h1 {margin:0; font-size:2.15rem; color:#163a50;}
.hero p {margin:.45rem 0 0 0; color:#315466;}
.small-note {font-size:.92rem; color:#52616b;}
</style>
<div class="hero">
  <h1>🧭 SmartRoute</h1>
  <p>여러 이동 수단과 접근성 정보를 한곳에서 확인하는 다국어 길찾기 도우미</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ 설정")
    language_name = st.selectbox("화면 언어 / Interface language", list(LANGUAGES.keys()), index=0)
    st.caption("지원 언어는 지도 서비스의 언어 지원 범위에 따라 달라질 수 있습니다.")
    st.divider()
    st.markdown("**사용 팁**")
    st.write("• 건물명만 입력하기보다 도시와 주소를 함께 적어 보세요.")
    st.write("• 항공·선박은 실제 운항 노선과 시간표를 별도로 확인해야 합니다.")

t = TEXT.get(language_name, TEXT["English"])
lang_code = LANGUAGES.get(language_name, "en")
st.caption(t["tagline"])

with st.form("route_form"):
    c1, c2 = st.columns(2)
    with c1:
        origin = st.text_input(t["origin"], placeholder="예: 서울역 / Seoul Station")
    with c2:
        destination = st.text_input(t["destination"], placeholder="예: 인천국제공항 / Incheon Airport")
    mode_choice = st.selectbox(
        t["mode"],
        ["모든 이동 수단 비교"] + list(MODE_LABELS.keys()),
        index=0
    )
    submitted = st.form_submit_button(t["find"], type="primary", use_container_width=True)

st.caption(t["tip"])

if submitted:
    origin = origin.strip()
    destination = destination.strip()
    if not origin or not destination:
        st.warning(t["empty"])
    elif origin.casefold() == destination.casefold():
        st.warning("출발지와 도착지가 같습니다. 서로 다른 장소를 입력해 주세요.")
    else:
        st.session_state["route_request"] = {
            "origin": origin, "destination": destination, "mode": mode_choice,
            "language": language_name, "lang_code": lang_code
        }

if "route_request" in st.session_state:
    req = st.session_state["route_request"]
    o, d = req["origin"], req["destination"]
    chosen = req["mode"]
    code = req["lang_code"]
    st.divider()
    st.subheader(t["routes"])

    modes_to_show = list(MODE_LABELS.items()) if chosen == "모든 이동 수단 비교" else [
        (chosen, MODE_LABELS[chosen])
    ]
    cards = st.columns(2)
    for idx, (label, mode) in enumerate(modes_to_show):
        with cards[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {label}")
                if mode in ("walking", "transit", "driving", "bicycling"):
                    url = maps_directions_url(o, d, mode, code)
                    st.link_button(t["open"], url, use_container_width=True)
                    if mode == "walking":
                        st.markdown(f"**⚡ {t['fast']}**")
                        st.write("지도에서 예상 소요 시간과 대체 경로를 비교하세요." if language_name == "한국어" else "Compare estimated time and alternate routes in Maps.")
                        st.link_button(
                            "🚶 " + t["fast"],
                            maps_directions_url(o, d, "walking", code),
                            use_container_width=True,
                        )
                        st.markdown(f"**🛡️ {t['safe']}**")
                        st.write("조명이 밝은 큰길, 보도 유무, 공사·통행 제한을 지도와 현장에서 직접 확인하세요." if language_name == "한국어" else "Check lighting, sidewalks, closures, and local conditions yourself.")
                        st.link_button(
                            "🗺️ " + t["safe"],
                            maps_search_url(f"well-lit pedestrian route sidewalks {o} to {d}", code),
                            use_container_width=True,
                        )
                elif mode == "flight":
                    st.info(t["flight_note"])
                    st.link_button("✈️ Search flights", google_flights_url(o, d), use_container_width=True)
                elif mode == "boat":
                    st.info(t["boat_note"])
                    st.link_button("⛴️ Search boats / ferries", ferry_search_url(o, d), use_container_width=True)

    st.divider()
    st.subheader(t["access"])
    st.write(t["access_note"])
    ac1, ac2 = st.columns(2)
    with ac1:
        st.link_button(
            "♿ " + t["access_search"],
            maps_search_url(f"wheelchair accessible route elevator near {o} {d}", code),
            use_container_width=True,
        )
    with ac2:
        st.link_button(
            "🏢 " + t["indoor_search"],
            maps_search_url(f"indoor maps navigation {d}", code),
            use_container_width=True,
        )
    st.info(t["limit_note"])

st.divider()
st.markdown("#### 🌐 번역과 언어")
st.write(
    "화면은 한국어와 영어를 기본 제공하며, 다른 언어를 선택하면 지도 링크에 해당 언어 설정을 전달합니다. "
    "Google Maps 및 검색 결과의 번역·음성 안내 지원은 언어와 지역에 따라 다르므로 모든 언어를 완벽히 지원한다고 보장할 수는 없습니다."
    if language_name == "한국어" else
    "The interface is provided in Korean and English. Other language choices are passed to Maps as a language hint where supported. Translation and voice guidance vary by language and region, so universal support cannot be guaranteed."
)
st.caption("SmartRoute는 경로 검색을 돕는 데모 앱이며, 지도 서비스의 데이터·약관·가용성에 따라 결과가 달라질 수 있습니다.")
