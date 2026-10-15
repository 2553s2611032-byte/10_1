
import streamlit as st

st.set_page_config(
    page_title="스마트 길찾기",
    page_icon="🧭",
    layout="wide"
)

# 다국어 지원
LANGUAGES = {
    "한국어": {
        "title": "🧭 스마트 길찾기",
        "subtitle": "빠르고 안전하며 편리한 길을 찾아보세요!",
        "start": "출발지",
        "end": "도착지",
        "transport": "이동 수단",
        "all": "모든 교통수단 비교",
        "modes": ["버스", "지하철", "택시", "걷기", "비행기", "배"],
        "find": "길찾기 시작",
        "access": "접근성 설정",
        "wheelchair": "휠체어·무장애 경로",
        "elevator": "엘리베이터 이용",
        "indoor": "건물 내부 길찾기",
        "safe": "🛡️ 안전한 길",
        "fast": "⚡ 빠른 길",
        "accessible": "♿ 무장애 경로",
        "error": "출발지와 도착지를 모두 입력해주세요.",
        "notice": "현재는 시연용 앱입니다. 실제 경로와 이동 시간을 표시하려면 지도 및 교통 API 연결이 필요합니다.",
        "directions": "이동 안내",
        "map": "지도",
        "indoor_notice": "건물 내부 길찾기를 위해서는 건물별 층별 지도와 엘리베이터·출입구 데이터가 필요합니다.",
        "last_walk": "역이나 정류장에서 목적지까지 남은 거리는 도보로 연결하도록 설계합니다."
    },
    "English": {
        "title": "🧭 Smart Route Finder",
        "subtitle": "Find fast, safe, and accessible routes!",
        "start": "Starting point",
        "end": "Destination",
        "transport": "Transportation",
        "all": "Compare all transportation",
        "modes": ["Bus", "Subway", "Taxi", "Walking", "Airplane", "Ship"],
        "find": "Find a route",
        "access": "Accessibility settings",
        "wheelchair": "Wheelchair-accessible route",
        "elevator": "Use elevators",
        "indoor": "Indoor navigation",
        "safe": "🛡️ Safer route",
        "fast": "⚡ Fastest route",
        "accessible": "♿ Accessible route",
        "error": "Please enter both the starting point and destination.",
        "notice": "This is a demo. Map and transit APIs are needed for real routes and travel times.",
        "directions": "Directions",
        "map": "Map",
        "indoor_notice": "Indoor navigation requires floor maps, elevator locations, and entrance data.",
        "last_walk": "The remaining distance from a station or stop can be completed on foot."
    }
}

# 언어 선택
language = st.sidebar.selectbox(
    "Language / 언어",
    ["한국어", "English"]
)

t = LANGUAGES[language]

st.title(t["title"])
st.write(t["subtitle"])
st.divider()

# 출발지와 도착지 입력
with st.form("route_form"):
    col1, col2 = st.columns(2)

    with col1:
        start = st.text_input(
            t["start"],
            placeholder="예: 서울역" if language == "한국어"
            else "e.g. Seoul Station"
        )

    with col2:
        end = st.text_input(
            t["end"],
            placeholder="예: 서울시청" if language == "한국어"
            else "e.g. Seoul City Hall"
        )

    transport = st.selectbox(
        t["transport"],
        [t["all"]] + t["modes"]
    )

    st.subheader(t["access"])

    col3, col4, col5 = st.columns(3)

    with col3:
        wheelchair = st.checkbox(t["wheelchair"])

    with col4:
        elevator = st.checkbox(t["elevator"])

    with col5:
        indoor = st.checkbox(t["indoor"])

    submitted = st.form_submit_button(
        t["find"],
        use_container_width=True
    )

# 길찾기 결과
if submitted:
    if not start.strip() or not end.strip():
        st.error(t["error"])

    else:
        st.success(f"{start} → {end}")
        st.info(t["notice"])

        st.caption(t["last_walk"])

        # 경로 비교
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader(t["safe"])
            if language == "한국어":
                st.write("• 보행로와 횡단보도 우선")
                st.write("• 보행 안전 정보를 고려")
            else:
                st.write("• Prefer sidewalks and crossings")
                st.write("• Consider pedestrian safety data")

        with col2:
            st.subheader(t["fast"])
            if language == "한국어":
                st.write("• 이동 시간 최소화")
                st.write("• 대중교통과 도보 조합")
            else:
                st.write("• Minimize travel time")
                st.write("• Combine transit and walking")

        with col3:
            st.subheader(t["accessible"])
            if language == "한국어":
                st.write("• 계단 없는 길 우선")
                st.write("• 엘리베이터와 경사로 고려")
            else:
                st.write("• Prefer step-free routes")
                st.write("• Consider elevators and ramps")

        st.divider()
        st.subheader(t["directions"])

        st.write(f"1. {t['start']}: {start}")
        st.write(f"2. {t['transport']}: {transport}")
        st.write(f"3. {t['end']}: {end}")

        if wheelchair or elevator:
            st.info(
                "무장애 경로를 실제로 안내하려면 "
                "엘리베이터 위치, 계단, 경사로 및 "
                "시설 운영 정보를 연결해야 합니다."
                if language == "한국어"
                else
                "Real accessible routing requires elevator, "
                "stair, ramp, and facility-status data."
            )

        if indoor:
            st.info(t["indoor_notice"])

        st.subheader(t["map"])
        st.caption(
            "실제 지도를 표시하려면 지도 API를 연결하세요."
            if language == "한국어"
            else "Connect a map API to display real maps."
        )

else:
    st.subheader(
        "✨ 주요 기능" if language == "한국어"
        else "✨ Main Features"
    )

    st.markdown("""
    - 🚌 버스, 지하철, 택시, 걷기, 비행기, 배 비교
    - 🛡️ 안전한 길과 빠른 길 비교
    - 🚶 역이나 정류장에서 목적지까지 도보 연결
    - ♿ 엘리베이터 및 무장애 경로 옵션
    - 🏢 건물 내부 길찾기 옵션
    - 🌐 한국어와 영어 지원
    """ if language == "한국어" else """
    - 🚌 Compare bus, subway, taxi, walking, airplane, and ship
    - 🛡️ Compare safer and faster routes
    - 🚶 Walk from the nearest stop or station to the destination
    - ♿ Accessibility and elevator options
    - 🏢 Indoor navigation options
    - 🌐 Korean and English support
    """)

st.divider()

st.caption(
    "스마트 길찾기 | Streamlit 프로토타입"
    if language == "한국어"
    else "Smart Route Finder | Streamlit Prototype"
)
