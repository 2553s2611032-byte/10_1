import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from urllib.parse import quote
import os

st.set_page_config(
    page_title="SmartRoute 길찾기",
    page_icon="🧭",
    layout="wide"
)

# 다국어 기본 번역
LANGUAGES = {
    "한국어": "ko",
    "English": "en",
    "日本語": "ja",
    "简体中文": "zh-CN",
    "繁體中文": "zh-TW",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Português": "pt",
    "Русский": "ru",
    "العربية": "ar",
    "हिन्दी": "hi",
    "Tiếng Việt": "vi",
    "ไทย": "th",
    "Bahasa Indonesia": "id",
    "Türkçe": "tr"
}

TRANSLATIONS = {
    "한국어": {
        "title": "SmartRoute 길찾기",
        "desc": "출발지와 목적지를 입력하면 이동 방법을 비교합니다.",
        "origin": "출발지",
        "destination": "목적지",
        "search": "길찾기",
        "map": "지도",
        "walk": "걷기",
        "transit": "버스·지하철",
        "taxi": "택시·자동차",
        "flight": "비행기",
        "boat": "배",
        "safe": "안전 우선",
        "fast": "빠른 이동",
        "access": "장애인 접근성 및 실내 길찾기",
        "elevator": "엘리베이터·접근성 정보 검색",
        "indoor": "건물 내부 지도 검색",
        "error": "장소를 찾지 못했습니다. 주소를 더 자세히 입력하세요.",
        "missing": "출발지와 목적지를 모두 입력하세요.",
        "note": "점선은 참고용 직선이며 실제 도로 경로가 아닙니다."
    },
    "English": {
        "title": "SmartRoute",
        "desc": "Enter your origin and destination to compare travel options.",
        "origin": "Origin",
        "destination": "Destination",
        "search": "Find routes",
        "map": "Map",
        "walk": "Walking",
        "transit": "Bus / Subway",
        "taxi": "Taxi / Car",
        "flight": "Flight",
        "boat": "Boat / Ferry",
        "safe": "Safety first",
        "fast": "Fastest route",
        "access": "Accessibility and indoor directions",
        "elevator": "Search accessibility information",
        "indoor": "Search indoor maps",
        "error": "Place not found. Enter a more specific address.",
        "missing": "Enter both origin and destination.",
        "note": "The dashed line is for reference only, not a real road."
    },
    "日本語": {
        "title": "SmartRoute 経路案内",
        "desc": "出発地と目的地を入力して移動方法を比較します。",
        "origin": "出発地",
        "destination": "目的地",
        "search": "経路検索",
        "map": "地図",
        "walk": "徒歩",
        "transit": "バス・地下鉄",
        "taxi": "タクシー・車",
        "flight": "飛行機",
        "boat": "船",
        "safe": "安全優先",
        "fast": "最速",
        "access": "バリアフリー・屋内経路",
        "elevator": "アクセシビリティ情報を検索",
        "indoor": "屋内地図を検索",
        "error": "場所が見つかりません。詳しい住所を入力してください。",
        "missing": "出発地と目的地を入力してください。",
        "note": "点線は参考線であり、実際の道路ではありません。"
    }
}

st.sidebar.header("🌐 Language / 언어")
language = st.sidebar.selectbox(
    "언어 선택",
    list(LANGUAGES.keys())
)

T = TRANSLATIONS.get(language, TRANSLATIONS["English"])

st.title("🧭 " + T["title"])
st.write(T["desc"])

with st.form("route_form"):
    col1, col2 = st.columns(2)

    with col1:
        origin = st.text_input(
            T["origin"],
            placeholder="예: 전주시청"
        )

    with col2:
        destination = st.text_input(
            T["destination"],
            placeholder="예: 전주역"
        )

    submitted = st.form_submit_button(
        "🔎 " + T["search"],
        use_container_width=True
    )


def get_location(address, lang):
    try:
        geolocator = Nominatim(
            user_agent="SmartRouteApp/1.0"
        )
        return geolocator.geocode(
            address,
            language=lang,
            timeout=15
        )
    except Exception:
        return None


def google_maps_url(start, end, mode):
    modes = {
        "walk": "walking",
        "transit": "transit",
        "taxi": "driving",
        "flight": "transit",
        "boat": "transit"
    }

    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={quote(start)}"
        f"&destination={quote(end)}"
        f"&travelmode={modes[mode]}"
    )


def search_url(query):
    return "https://www.google.com/search?q=" + quote(query)


if submitted:
    if not origin.strip() or not destination.strip():
        st.warning(T["missing"])
    else:
        with st.spinner("장소를 검색하고 있습니다..."):
            start_location = get_location(
                origin.strip(),
                LANGUAGES[language]
            )
            end_location = get_location(
                destination.strip(),
                LANGUAGES[language]
            )

        if start_location is None or end_location is None:
            st.error(T["error"])
        else:
            st.session_state["route_data"] = {
                "origin": origin.strip(),
                "destination": destination.strip(),
                "start": [
                    start_location.latitude,
                    start_location.longitude
                ],
                "end": [
                    end_location.latitude,
                    end_location.longitude
                ],
                "start_address": start_location.address,
                "end_address": end_location.address
            }


data = st.session_state.get("route_data")

if data:
    origin = data["origin"]
    destination = data["destination"]
    start = data["start"]
    end = data["end"]

    col_map, col_routes = st.columns([1.3, 1])

    with col_map:
        st.subheader("🗺️ " + T["map"])

        center = [
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2
        ]

        map_view = folium.Map(
            location=center,
            zoom_start=12,
            control_scale=True
        )

        folium.Marker(
            start,
            tooltip=T["origin"],
            popup=data["start_address"],
            icon=folium.Icon(color="green")
        ).add_to(map_view)

        folium.Marker(
            end,
            tooltip=T["destination"],
            popup=data["end_address"],
            icon=folium.Icon(color="red")
        ).add_to(map_view)

        folium.PolyLine(
            [start, end],
            color="blue",
            weight=3,
            dash_array="8, 8"
        ).add_to(map_view)

        map_view.fit_bounds([start, end])

        st_folium(
            map_view,
            use_container_width=True,
            height=450,
            returned_objects=[]
        )

        st.caption(T["note"])

    with col_routes:
        st.subheader("🚏 " + T["safe"] + " / " + T["fast"])

        modes = [
            ("walk", "🚶"),
            ("transit", "🚌"),
            ("taxi", "🚕"),
            ("flight", "✈️"),
            ("boat", "⛴️")
        ]

        for mode, icon in modes:
            st.markdown(f"### {icon} {T[mode]}")

            st.link_button(
                T["search"],
                google_maps_url(origin, destination, mode),
                use_container_width=True,
                key=None
            )

        st.info(
            "🛡️ 안전 우선: 밝고 사람이 다니는 길과 보행자 통로를 확인하세요."
        )
        st.info(
            "⚡ 빠른 이동: 지도 서비스에서 예상 시간과 환승을 비교하세요."
        )

    st.divider()

    st.subheader("♿ " + T["access"])

    col_a, col_b = st.columns(2)

    with col_a:
        st.link_button(
            "♿ " + T["elevator"],
            search_url(
                destination + " 엘리베이터 휠체어 접근성 경로"
            ),
            use_container_width=True
        )

    with col_b:
        st.link_button(
            "🏢 " + T["indoor"],
            search_url(
                destination + " 건물 내부 지도 층별 안내"
            ),
            use_container_width=True
        )

st.divider()

st.caption(
    "SmartRoute | 공개 지도 서비스 사용 | API 키 없이 실행"
)

with st.expander("ℹ️ 안내"):
    st.write(
        "지도 점선은 실제 길이 아닌 참고선입니다. "
        "실제 도보 경로, 버스·지하철 환승, 시간표, "
        "안전 경로, 엘리베이터와 건물 내부 길은 "
        "상세 경로 링크에서 확인하세요. "
        "실내 길찾기와 접근성 정보는 건물별 데이터가 있어야 정확합니다."
    )
