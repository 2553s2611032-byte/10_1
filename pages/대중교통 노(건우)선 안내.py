
import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Smart Route Finder",
    page_icon="🧭",
    layout="wide"
)

# 지원 언어와 번역 코드
LANGUAGES = {
    "한국어": "ko",
    "English": "en",
    "日本語": "ja",
    "简体中文": "zh-CN",
    "繁體中文": "zh-TW",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "Português": "pt",
    "Русский": "ru",
    "العربية": "ar",
    "हिन्दी": "hi",
    "বাংলা": "bn",
    "اردو": "ur",
    "Türkçe": "tr",
    "Tiếng Việt": "vi",
    "ไทย": "th",
    "Bahasa Indonesia": "id",
    "Bahasa Melayu": "ms",
    "Filipino": "tl",
    "Nederlands": "nl",
    "Polski": "pl",
    "Українська": "uk",
    "Ελληνικά": "el",
    "עברית": "iw",
    "فارسی": "fa",
    "Svenska": "sv",
    "Norsk": "no",
    "Dansk": "da",
    "Suomi": "fi",
    "Čeština": "cs",
    "Magyar": "hu",
    "Română": "ro",
    "Български": "bg",
    "Српски": "sr",
    "Hrvatski": "hr",
    "Slovenčina": "sk",
    "Slovenščina": "sl",
    "Lietuvių": "lt",
    "Latviešu": "lv",
    "Eesti": "et",
    "Català": "ca",
    "Kiswahili": "sw",
    "Afrikaans": "af",
    "Shqip": "sq",
    "Հայերեն": "hy",
    "नेपाली": "ne",
    "मराठी": "mr",
    "ગુજરાતી": "gu",
    "தமிழ்": "ta",
    "తెలుగు": "te",
    "ಕನ್ನಡ": "kn",
    "മലയാളം": "ml",
    "ລາວ": "lo",
    "ខ្មែរ": "km",
    "မြန်မာ": "my",
    "Монгол": "mn",
    "Қазақша": "kk",
    "O‘zbek": "uz",
    "ქართული": "ka",
    "Azərbaycanca": "az",
    "Bosanski": "bs",
    "Македонски": "mk",
    "Íslenska": "is",
    "Gaeilge": "ga",
    "Cymraeg": "cy",
    "Esperanto": "eo",
}

# 기본 문구: 한국어
TEXT = {
    "title": "🧭 스마트 길찾기",
    "subtitle": "빠르고 안전하며 편리한 길을 찾아보세요!",
    "start": "출발지",
    "end": "도착지",
    "start_hint": "예: 서울역",
    "end_hint": "예: 서울시청",
    "transport": "이동 수단",
    "all": "모든 교통수단 비교",
    "bus": "버스",
    "subway": "지하철",
    "taxi": "택시",
    "walk": "걷기",
    "plane": "비행기",
    "ship": "배",
    "find": "길찾기 시작",
    "access": "접근성 설정",
    "wheelchair": "휠체어·무장애 경로 우선",
    "elevator": "엘리베이터 이용 가능 경로",
    "indoor": "건물 내부 길찾기",
    "safe": "🛡️ 안전한 길",
    "fast": "⚡ 빠른 길",
    "accessible": "♿ 무장애 경로",
    "error": "출발지와 도착지를 모두 입력해주세요.",
    "notice": "현재는 시연용 앱입니다. 실제 경로와 이동 시간을 표시하려면 지도 및 교통 API 연결이 필요합니다.",
    "directions": "이동 안내",
    "map": "지도",
    "map_notice": "실제 지도를 표시하려면 지도 API를 연결하세요.",
    "last_walk": "역이나 정류장에서 목적지까지 남은 거리는 도보로 연결하도록 설계합니다.",
    "safe1": "보행로와 표시된 횡단보도를 우선합니다.",
    "safe2": "도로 안전 정보가 제공되면 이를 고려합니다.",
    "fast1": "예상 이동 시간이 짧은 경로를 우선합니다.",
    "fast2": "대중교통과 도보 구간을 조합할 수 있습니다.",
    "access1": "계단 없는 길과 접근 가능한 출입구를 우선합니다.",
    "access2": "엘리베이터와 경사로 정보를 확인합니다.",
    "indoor_notice": "건물 내부 길찾기에는 층별 지도, 출입구, 복도 및 엘리베이터 데이터가 필요합니다.",
    "access_notice": "실제 무장애 경로를 확인하려면 엘리베이터 위치와 운영 상태, 계단, 경사로 및 출입구 데이터가 필요합니다.",
    "step1": "출발지",
    "step2": "선택한 이동 수단",
    "step3": "도착지",
    "features": "✨ 주요 기능",
    "feature1": "버스, 지하철, 택시, 도보, 비행기, 배 비교",
    "feature2": "안전한 길과 빠른 길 비교",
    "feature3": "역이나 정류장에서 목적지까지 도보 연결",
    "feature4": "엘리베이터와 무장애 경로 옵션",
    "feature5": "건물 내부 길찾기 옵션",
    "feature6": "다국어 지원",
    "translation_error": "자동 번역에 실패했습니다. 인터넷 연결을 확인하고 다시 시도해주세요.",
    "footer": "스마트 길찾기 | 다국어 Streamlit 프로토타입",
}

# 번역 결과 캐시: 같은 문장을 매번 다시 번역하지 않음
@st.cache_data(show_spinner=False, ttl=86400)
def translate(text, target):
    if target == "ko":
        return text

    try:
        return GoogleTranslator(
            source="ko",
            target=target
        ).translate(text)
    except Exception:
        return text


def tr(key, target):
    return translate(TEXT[key], target)


# 언어 선택
st.sidebar.header("🌐 Language / 언어")
language_name = st.sidebar.selectbox(
    "원하는 언어를 선택하세요",
    list(LANGUAGES.keys())
)
lang = LANGUAGES[language_name]

st.title(tr("title", lang))
st.write(tr("subtitle", lang))
st.divider()

# 교통수단 이름 번역
mode_keys = [
    "bus", "subway", "taxi",
    "walk", "plane", "ship"
]
modes = [tr(key, lang) for key in mode_keys]
all_modes = tr("all", lang)

# 입력 화면
with st.form("route_form"):
    col1, col2 = st.columns(2)

    with col1:
        start = st.text_input(
            tr("start", lang),
            placeholder=tr("start_hint", lang)
        )

    with col2:
        end = st.text_input(
            tr("end", lang),
            placeholder=tr("end_hint", lang)
        )

    transport = st.selectbox(
        tr("transport", lang),
        [all_modes] + modes
    )

    st.subheader(tr("access", lang))
    c1, c2, c3 = st.columns(3)

    with c1:
        wheelchair = st.checkbox(
            tr("wheelchair", lang)
        )

    with c2:
        elevator = st.checkbox(
            tr("elevator", lang)
        )

    with c3:
        indoor = st.checkbox(
            tr("indoor", lang)
        )

    submitted = st.form_submit_button(
        tr("find", lang),
        use_container_width=True
    )

# 결과 화면
if submitted:
    if not start.strip() or not end.strip():
        st.error(tr("error", lang))

    else:
        st.success(f"{start} → {end}")
        st.info(tr("notice", lang))
        st.caption(tr("last_walk", lang))

        c1, c2, c3 = st.columns(3)

        with c1:
            st.subheader(tr("safe", lang))
            st.write("• " + tr("safe1", lang))
            st.write("• " + tr("safe2", lang))

        with c2:
            st.subheader(tr("fast", lang))
            st.write("• " + tr("fast1", lang))
            st.write("• " + tr("fast2", lang))

        with c3:
            st.subheader(tr("accessible", lang))
            st.write("• " + tr("access1", lang))
            st.write("• " + tr("access2", lang))

        st.divider()
        st.subheader(tr("directions", lang))
        st.write(f"1. {tr('step1', lang)}: {start}")
        st.write(f"2. {tr('step2', lang)}: {transport}")
        st.write(f"3. {tr('step3', lang)}: {end}")

        if wheelchair or elevator:
            st.info(tr("access_notice", lang))

        if indoor:
            st.info(tr("indoor_notice", lang))

        st.subheader(tr("map", lang))
        st.caption(tr("map_notice", lang))

else:
    st.subheader(tr("features", lang))

    for key in [
        "feature1", "feature2", "feature3",
        "feature4", "feature5", "feature6"
    ]:
        st.write("• " + tr(key, lang))

st.divider()
st.caption(tr("footer", lang))
