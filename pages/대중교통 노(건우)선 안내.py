
import streamlit as st
from deep_translator import GoogleTranslator

LANGUAGES = {
    "한국어": "ko",
    "English": "en",
    "日本語": "ja",
    "中文": "zh-CN",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "العربية": "ar",
    "Tiếng Việt": "vi",
    "ไทย": "th"
}

@st.cache_data(show_spinner=False, ttl=3600)
def translate_text(text, target_language):
    if target_language == "ko":
        return text

    try:
        return GoogleTranslator(
            source="ko",
            target=target_language
        ).translate(text)
    except Exception:
        return text



def tr(key, target_language):
    return translate_text(TEXT[key], target_language)


# 사이드바 언어 선택
st.sidebar.header("🌐 언어 / Language")
language_name = st.sidebar.selectbox(
    "언어 선택 / Select language",
    options=list(LANGUAGES.keys()),
    index=0
)
target_language = LANGUAGES[language_name]

# 제목과 설명
st.title(tr("title", target_language))
st.write(tr("subtitle", target_language))
st.divider()

# 교통수단 선택
mode_keys = ["bus", "subway", "taxi", "walk", "plane", "ship"]
translated_modes = [tr(key, target_language) for key in mode_keys]
all_modes = tr("all", target_language)

# 입력 폼
with st.form("route_form"):
    col1, col2 = st.columns(2)

    with col1:
        start = st.text_input(
            tr("start", target_language),
            placeholder=tr("start_hint", target_language)
        )

    with col2:
        end = st.text_input(
            tr("end", target_language),
            placeholder=tr("end_hint", target_language)
        )

    transport = st.selectbox(
        tr("transport", target_language),
        [all_modes] + translated_modes
    )

    st.subheader(tr("access", target_language))
    c1, c2, c3 = st.columns(3)

    with c1:
        wheelchair = st.checkbox(tr("wheelchair", target_language))

    with c2:
        elevator = st.checkbox(tr("elevator", target_language))

    with c3:
        indoor = st.checkbox(tr("indoor", target_language))

    submitted = st.form_submit_button(
        tr("find", target_language),
        use_container_width=True
    )

# 결과 화면
if submitted:
    if not start.strip() or not end.strip():
        st.error(tr("error", target_language))
    else:
        st.success(f"{start} → {end}")
        st.info(tr("notice", target_language))
        st.caption(tr("last_walk", target_language))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader(tr("safe", target_language))
            st.write("• " + tr("safe1", target_language))
            st.write("• " + tr("safe2", target_language))

        with col2:
            st.subheader(tr("fast", target_language))
            st.write("• " + tr("fast1", target_language))
            st.write("• " + tr("fast2", target_language))

        with col3:
            st.subheader(tr("accessible", target_language))
            st.write("• " + tr("access1", target_language))
            st.write("• " + tr("access2", target_language))

        st.divider()
        st.subheader(tr("directions", target_language))
        st.write(f"1. {tr('step1', target_language)}: {start}")
        st.write(f"2. {tr('step2', target_language)}: {transport}")
        st.write(f"3. {tr('step3', target_language)}: {end}")

        if wheelchair or elevator:
            st.info(tr("access_notice", target_language))

        if indoor:
            st.info(tr("indoor_notice", target_language))

        st.subheader(tr("map", target_language))
        st.caption(tr("map_notice", target_language))

else:
    st.subheader(tr("features", target_language))
    for key in [
        "feature1", "feature2", "feature3",
        "feature4", "feature5", "feature6"
    ]:
        st.write("• " + tr(key, target_language))

st.divider()
st.caption(tr("footer", target_language))
