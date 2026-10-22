import os, zipfile, textwrap, json
base="/mnt/data/smartroute_no_translation_api"
os.makedirs(base, exist_ok=True)

app_code = r'''import os
import time
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from urllib.parse import quote

st.set_page_config(page_title="SmartRoute | 다국어 길찾기", page_icon="🧭", layout="wide")

# API 키 없이 사용할 수 있는 기본 UI 번역 사전입니다.
# 실제 대중교통 경로·시간표와 모든 언어의 자연스러운 번역을 보장하지는 않습니다.
LANGUAGES = {
    "한국어": "ko", "English": "en", "日本語": "ja", "简体中文": "zh-CN",
    "繁體中文": "zh-TW", "Español": "es", "Français": "fr", "Deutsch": "de",
    "Português": "pt", "Русский": "ru", "العربية": "ar", "हिन्दी": "hi",
    "Tiếng Việt": "vi", "ไทย": "th", "Bahasa Indonesia": "id", "Türkçe": "tr"
}
TEXT = {
"한국어": {
"title":"SmartRoute 길찾기", "subtitle":"출발지와 목적지를 입력하고 이동 방법을 비교해 보세요.",
"origin":"출발지", "destination":"목적지", "origin_ph":"예: 전주시청", "dest_ph":"예: 전주역",
"search":"길찾기", "map":"지도 미리보기", "modes":"이동 방법", "safe":"안전 우선", "fast":"빠른 이동",
"walk":"걷기", "transit":"버스·지하철", "taxi":"택시·자동차", "flight":"비행기", "boat":"배",
"access":"접근성·실내 길찾기", "access_note":"엘리베이터, 휠체어 이동로, 건물 내부 길은 건물별 데이터가 있어야 정확합니다. 아래 링크에서 확인하세요.",
"elevator":"엘리베이터·접근성 정보 검색", "indoor":"건물 내부 지도 검색", "route_links":"상세 경로 열기",
"not_found":"장소를 찾지 못했습니다. 주소, 도시 이름 또는 랜드마크를 더 구체적으로 입력해 주세요.",
"map_note":"지도에는 위치 표시와 참고 선이 나타납니다. 실제 보행 안전 경로, 대중교통 경로와 실내 동선은 해당 지도 서비스에서 확인하세요.",
"need_both":"출발지와 목적지를 모두 입력해 주세요.", "geocoding":"장소 검색 중…", "route_summary":"경로 비교",
"safe_desc":"큰길·밝은 길·보행자 통로를 우선 확인하고, 야간에는 인적이 있는 길을 선택하세요.",
"fast_desc":"이동 시간이 짧은 경로를 지도 서비스에서 비교하세요.",
"walk_desc":"마지막 정류장/역에서 목적지까지의 도보 경로를 함께 확인하세요.",
"transit_desc":"정확한 버스 번호, 환승, 시간표는 상세 경로에서 확인하세요.",
"flight_desc":"장거리 이동에 적합합니다. 공항 이동과 보안·탑승 시간을 추가로 고려하세요.",
"boat_desc":"항구와 운항 일정을 확인한 뒤 이동하세요.",
"taxi_desc":"차량 이동 경로를 지도에 표시합니다. 교통 상황에 따라 시간은 달라집니다.",
"disclaimer":"참고: 이 앱은 API 키 없이 공개 지오코딩/경로 서비스를 사용합니다. 공개 서비스의 이용 제한으로 검색이 잠시 실패할 수 있습니다."
},
"English": {
"title":"SmartRoute", "subtitle":"Enter your start and destination to compare travel options.",
"origin":"From", "destination":"To", "origin_ph":"e.g. City Hall", "dest_ph":"e.g. Central Station",
"search":"Find routes", "map":"Map preview", "modes":"Travel options", "safe":"Safety first", "fast":"Fastest",
"walk":"Walking", "transit":"Bus / subway", "taxi":"Taxi / car", "flight":"Flight", "boat":"Ferry / boat",
"access":"Accessibility & indoor directions", "access_note":"Accurate elevators, wheelchair routes, and indoor paths require building-specific data. Check the links below.",
"elevator":"Search elevators & accessibility", "indoor":"Search indoor maps", "route_links":"Open detailed directions",
"not_found":"Place not found. Try a more specific address, city, or landmark.",
"map_note":"The map shows locations and a reference line. Check the map service for actual safe walking, transit, and indoor routes.",
"need_both":"Enter both a start and a destination.", "geocoding":"Searching for places…", "route_summary":"Route comparison",
"safe_desc":"Prefer well-lit, busy streets and pedestrian paths; choose populated routes at night.",
"fast_desc":"Compare estimated travel times in a maps service.",
"walk_desc":"Check the walking route from the final stop or station to your destination.",
"transit_desc":"Check exact bus numbers, transfers, and schedules in detailed directions.",
"flight_desc":"Useful for long distances. Include airport transfers, security, and boarding time.",
"boat_desc":"Check ports and sailing schedules before travelling.",
"taxi_desc":"The map displays a driving route. Travel time varies with traffic.",
"disclaimer":"Note: This app uses public geocoding/routing services without an API key. Temporary failures or usage limits may occur."
},
"日本語": {
"title":"SmartRoute", "subtitle":"出発地と目的地を入力して移動方法を比較します。",
"origin":"出発地", "destination":"目的地", "origin_ph":"例：市役所", "dest_ph":"例：中央駅",
"search":"経路を検索", "map":"地図プレビュー", "modes":"移動方法", "safe":"安全優先", "fast":"最速",
"walk":"徒歩", "transit":"バス・地下鉄", "taxi":"タクシー・車", "flight":"飛行機", "boat":"船",
"access":"バリアフリー・屋内経路", "access_note":"エレベーター、車いす経路、屋内経路の正確な情報には建物ごとのデータが必要です。",
"elevator":"バリアフリー情報を検索", "indoor":"屋内地図を検索", "route_links":"詳しい経路を開く",
"not_found":"場所が見つかりません。住所やランドマークを詳しく入力してください。",
"map_note":"地図は場所と参考線を表示します。実際の徒歩・公共交通・屋内経路は地図サービスで確認してください。",
"need_both":"出発地と目的地を入力してください。", "geocoding":"場所を検索中…", "route_summary":"経路の比較",
"safe_desc":"明るく人通りの多い道や歩道を優先してください。", "fast_desc":"地図サービスで所要時間を比較してください。",
"walk_desc":"最後の停留所・駅から目的地までの徒歩経路も確認してください。",
"transit_desc":"バス番号、乗り換え、時刻表は詳細経路で確認してください。",
"flight_desc":"長距離向けです。空港までの移動や搭乗時間も考慮してください。",
"boat_desc":"港と運航スケジュールを確認してください。", "taxi_desc":"車の経路を表示します。所要時間は交通状況で変わります。",
"disclaimer":"APIキー不要の公開サービスを使用します。利用制限などで検索に失敗する場合があります。"
}
}
# For languages without a full dictionary, English is used as a stable fallback.
def tr(key):
    lang = st.session_state.get("ui_lang", "한국어")
    dictionary = TEXT.get(lang, TEXT["English"])
    return dictionary.get(key, TEXT["English"].get(key, TEXT["한국어"].get(key, key)))

def geocode(place, language_code):
    try:
        geolocator = Nominatim(user_agent="SmartRouteStudentApp/1.0 (Streamlit demo)")
        return geolocator.geocode(place, language=language_code, timeout=12)
    except Exception:
        return None

def maps_url(origin, destination, mode):
    # Google Maps directions links provide current transit and travel directions.
    modes = {"walk":"walking", "transit":"transit", "taxi":"driving", "flight":"transit", "boat":"transit"}
    return "https://www.google.com/maps/dir/?api=1&origin=" + quote(origin) + "&destination=" + quote(destination) + "&travelmode=" + modes.get(mode, "transit")

def search_url(query):
    return "https://www.google.com/search?q=" + quote(query)

st.session_state.setdefault("ui_lang", "한국어")
with st.sidebar:
    st.selectbox("Language / 언어", list(LANGUAGES.keys()), key="ui_lang")
    st.caption("기본 번역은 API 키 없이 제공됩니다. 일부 언어는 영어로 표시될 수 있습니다.")

st.title("🧭 " + tr("title"))
st.write(tr("subtitle"))
st.caption(tr("disclaimer"))

with st.form("route_form"):
    c1, c2 = st.columns(2)
    with c1:
        origin = st.text_input(tr("origin"), placeholder=tr("origin_ph"))
    with c2:
        destination = st.text_input(tr("destination"), placeholder=tr("dest_ph"))
    submitted = st.form_submit_button("🔎 " + tr("search"), use_container_width=True)

if submitted:
    if not origin.strip() or not destination.strip():
        st.warning(tr("need_both"))
    else:
        lang_code = LANGUAGES.get(st.session_state.ui_lang, "en")
        with st.spinner(tr("geocoding")):
            start_loc = geocode(origin.strip(), lang_code)
            time.sleep(1.0)  # Be considerate to the public Nominatim service.
            end_loc = geocode(destination.strip(), lang_code)
        if not start_loc or not end_loc:
            st.error(tr("not_found"))
        else:
            st.session_state["route_result"] = {
                "origin": origin.strip(), "destination": destination.strip(),
                "start": [start_loc.latitude, start_loc.longitude],
                "end": [end_loc.latitude, end_loc.longitude],
                "start_name": start_loc.address, "end_name": end_loc.address
            }

result = st.session_state.get("route_result")
if result:
    origin = result["origin"]
    destination = result["destination"]
    start = result["start"]
    end = result["end"]

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("🗺️ " + tr("map"))
        center = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        m = folium.Map(location=center, zoom_start=12, control_scale=True, tiles="OpenStreetMap")
        folium.Marker(start, tooltip=tr("origin"), popup=folium.Popup(result["start_name"], max_width=280),
                      icon=folium.Icon(color="green", icon="play")).add_to(m)
        folium.Marker(end, tooltip=tr("destination"), popup=folium.Popup(result["end_name"], max_width=280),
                      icon=folium.Icon(color="red", icon="flag")).add_to(m)
        # Reference line only; not represented as a walkable road route.
        folium.PolyLine([start, end], color="#4263eb", weight=4, opacity=0.7,
                        dash_array="8, 10", tooltip="Reference line (not a navigable route)").add_to(m)
        bounds = [start, end]
        m.fit_bounds(bounds, padding=(30, 30))
        st_folium(m, use_container_width=True, height=480, returned_objects=[])
        st.caption(tr("map_note"))
    with right:
        st.subheader("🧭 " + tr("route_summary"))
        mode_cards = [
            ("walk", "🚶", "walk_desc"),
            ("transit", "🚌", "transit_desc"),
            ("taxi", "🚕", "taxi_desc"),
            ("flight", "✈️", "flight_desc"),
            ("boat", "⛴️", "boat_desc"),
        ]
        for mode, emoji, desc in mode_cards:
            title = tr(mode)
            with st.container(border=True):
                st.markdown(f"**{emoji} {title}**")
                st.write(tr(desc))
                st.link_button(tr("route_links"), maps_url(origin, destination, mode), use_container_width=True)

        st.markdown("**" + tr("safe") + " / " + tr("fast") + "**")
        st.write("🛡️ " + tr("safe_desc"))
        st.write("⚡ " + tr("fast_desc"))

    st.divider()
    st.subheader("♿ " + tr("access"))
    st.write(tr("access_note"))
    a, b = st.columns(2)
    with a:
        st.link_button("♿ " + tr("elevator"), search_url(f"{destination} elevator wheelchair accessible route"))
    with b:
        st.link_button("🏢 " + tr("indoor"), search_url(f"{destination} indoor map floor plan elevator"))

st.divider()
with st.expander("ℹ️ 앱 사용 시 알아둘 점"):
    st.markdown("""
- **API 키 없이 번역:** 자주 쓰는 화면 문구는 내장 번역 사전으로 표시합니다. 사전에 없는 언어/문장은 영어 또는 한국어로 대체될 수 있습니다.
- **지도:** 출발지와 목적지의 위치를 앱 안에서 볼 수 있습니다. 점선은 두 지점 사이의 참고선이며 실제 도로·보행 경로가 아닙니다.
- **실제 경로:** 버스·지하철 환승, 실시간 도착, 보행자 안전 경로, 엘리베이터, 휠체어 전용 경로, 건물 내부 길은 전문 데이터/API가 필요합니다. 상세 경로 버튼에서 지도 서비스의 최신 정보를 확인하세요.
- **안전:** 앱의 안전 우선 안내는 일반적인 조언이며, 현장 안전을 보장하거나 검증된 안전 경로를 계산하지 않습니다.
- **비행기·배:** 항공편/선박 시간표와 예약은 운항사 또는 지도·검색 서비스에서 확인해야 합니다.
""")
'''
requirements = """streamlit>=1.32,<2.0
folium>=0.15,<1.0
streamlit-folium>=0.20,<1.0
geopy>=2.4,<3.0
requests>=2.31,<3.0
"""
readme = r'''# SmartRoute — Streamlit Community Cloud

API 키 없이 시작할 수 있는 다국어 길찾기 데모 앱입니다.

## 기능
- 출발지/목적지 검색 및 앱 안의 OpenStreetMap 지도
- 걷기, 버스/지하철, 택시/자동차, 비행기, 배 옵션별 상세 경로 링크
- 안전 우선/빠른 이동을 고려할 때 참고할 안내
- 엘리베이터·접근성 및 건물 내부 지도 검색 링크
- API 키 없는 기본 화면 번역(한국어, 영어, 일본어 사전 제공, 기타 언어는 영어 fallback)

## GitHub에 올리기
1. ZIP 압축을 풉니다.
2. `app.py`, `requirements.txt`, `README.md`를 GitHub 저장소 최상위 폴더에 올립니다.
3. Streamlit Community Cloud에서 저장소와 `app.py`를 선택해 배포합니다.
4. Secrets 설정은 필요하지 않습니다.

## 중요 한계
- 지도는 위치를 앱 안에 표시합니다. 점선은 참고용 직선이며 실제 도로나 보행 경로가 아닙니다.
- 대중교통의 실제 노선/환승/시간표, 정확한 도보 경로, 안전 경로, 엘리베이터·휠체어 접근성, 실내 길찾기는 별도 데이터/API가 필요합니다.
- 공개 Nominatim 지오코딩 서비스를 사용하므로 사용량 제한이나 일시적 오류가 발생할 수 있습니다. 대량 요청에는 사용하지 마세요.
- Google Maps의 상세 경로 버튼은 외부 페이지를 엽니다. 대중교통/항공/선박의 실제 이용 가능 여부는 목적지와 지역에 따라 달라집니다.
- 앱은 경로의 안전성이나 접근성을 보장하지 않습니다.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```
'''
with open(os.path.join(base,"app.py"),"w",encoding="utf-8") as f: f.write(app_code)
with open(os.path.join(base,"requirements.txt"),"w",encoding="utf-8") as f: f.write(requirements)
with open(os.path.join(base,"README.md"),"w",encoding="utf-8") as f: f.write(readme)
zip_path="/mnt/data/smartroute_no_translation_api.zip"
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for fn in ["app.py","requirements.txt","README.md"]:
        z.write(os.path.join(base,fn), arcname=fn)
print(zip_path, os.path.getsize(zip_path), os.listdir(base))
