import streamlit as st
from datetime import date

st.set_page_config(
    page_title="대한민국 이주시민 안내",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 디자인 및 공통 데이터
# -----------------------------
BG = "#EAF4FC"
INK = "#183247"
BLUE = "#2F6F9F"
PALE_BLUE = "#D7E8F7"
WHITE = "#FFFFFF"

st.markdown(
    f"""
    <style>
      .stApp {{ background: {BG}; color: {INK}; }}
      [data-testid="stSidebar"] {{ background: #F5FAFE; }}
      .hero {{
        background: linear-gradient(120deg, #D3E8F8 0%, #F7FBFF 100%);
        border: 1px solid #8AAFCB; border-radius: 24px;
        padding: 1.7rem 2rem; margin-bottom: 1rem;
      }}
      .hero h1 {{ color: {INK}; font-size: 2rem; margin: 0 0 .45rem 0; }}
      .hero p {{ color: #35556D; margin: 0; font-size: 1rem; }}
      .panel {{
        background: rgba(255,255,255,.78); border: 1px solid #9DB9CE;
        border-radius: 18px; padding: 1rem 1.1rem; height: 100%;
      }}
      .panel h3 {{ color: {INK}; margin-top: 0; }}
      .small-note {{ color: #4F6B7F; font-size: .88rem; }}
      div.stButton > button {{
        border-radius: 12px; border: 1px solid #7D9FB8;
        min-height: 3rem; font-weight: 600;
      }}
      a {{ color: {BLUE} !important; }}
      [data-testid="stMetric"] {{
        background: white; border: 1px solid #D0E0EC;
        padding: 12px; border-radius: 14px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES = ["홈", "대중교통 안내", "우리 문화 홍보 및 번역", "우리말 교육"]

def go(page: str):
    st.session_state["page"] = page

def external_link(label: str, url: str):
    st.markdown(f"[{label}]({url})")

def page_title(title: str, subtitle: str):
    st.title(title)
    st.caption(subtitle)
    st.divider()

# -----------------------------
# 사이드바 메뉴
# -----------------------------
with st.sidebar:
    st.markdown("## 🌏 이주시민 안내")
    st.caption("한국 생활에 필요한 정보를 한곳에서")
    current = st.session_state.get("page", "홈")
    selected = st.radio(
        "메뉴",
        PAGES,
        index=PAGES.index(current) if current in PAGES else 0,
        label_visibility="collapsed",
    )
    st.session_state["page"] = selected
    st.divider()
    st.markdown("**긴급 상황**")
    st.markdown("- 긴급 신고: **112**")
    st.markdown("- 응급·구급: **119**")
    st.markdown("- 외국인종합안내센터: **1345**")
    st.caption("운영 시간 및 통역 지원 범위는 공식 안내에서 확인하세요.")

page = st.session_state.get("page", "홈")

# -----------------------------
# 홈 화면: 제공된 와이어프레임의 큰 구조를 반영
# -----------------------------
if page == "홈":
    st.markdown(
        """
        <div class="hero">
          <h1>정부 이주시민 지원사업 안내</h1>
          <p>한국 생활에 필요한 공공서비스와 정착 정보를 쉽고 편하게 찾아보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 이미지의 왼쪽 기능 메뉴 + 오른쪽 설명 영역 구조
    left, right = st.columns([0.9, 1.7], gap="large")
    with left:
        st.markdown("### 필요한 기능 바로가기")
        if st.button("🚌  대중교통 안내", use_container_width=True):
            go("대중교통 안내")
            st.rerun()
        if st.button("🗣️  우리 문화 홍보 및 번역", use_container_width=True):
            go("우리 문화 홍보 및 번역")
            st.rerun()
        if st.button("📚  우리말 교육", use_container_width=True):
            go("우리말 교육")
            st.rerun()
        st.markdown(
            '<p class="small-note">언어와 생활환경이 달라도 필요한 정보를 빠르게 찾을 수 있도록 구성했습니다.</p>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="panel">
              <h3>페이지 기능 설명</h3>
              <p><b>대중교통 안내</b> — 버스·지하철 이용 기본 정보와 공식 길찾기 서비스를 확인합니다.</p>
              <p><b>우리 문화 홍보 및 번역</b> — 한국의 생활문화와 자주 쓰는 생활 표현을 살펴봅니다.</p>
              <p><b>우리말 교육</b> — 상황별 기초 한국어 표현과 짧은 연습 문제를 제공합니다.</p>
              <hr>
              <p class="small-note">이 페이지는 정보 탐색을 돕는 안내 서비스입니다. 지원 자격, 신청 기간, 운영시간은 각 기관의 최신 공지를 확인하세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## 정부·공공기관 지원 정보")
    st.caption("아래 공식 사이트에서 체류, 생활, 가족 지원 관련 최신 정보를 확인할 수 있습니다.")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown(
            """
            <div class="panel">
              <h3>🏛️ 출입국·체류 안내</h3>
              <p>체류 자격, 민원, 외국인 종합 안내 정보를 확인하세요.</p>
              <p><a href="https://www.hikorea.go.kr/" target="_blank">하이코리아 바로가기 ↗</a></p>
              <p><a href="https://www.immigration.go.kr/" target="_blank">출입국·외국인정책본부 ↗</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="panel">
              <h3>👨‍👩‍👧 다누리·가족 지원</h3>
              <p>다문화가족 지원, 생활 정보, 다국어 상담 정보를 찾아보세요.</p>
              <p><a href="https://www.liveinkorea.kr/" target="_blank">다누리 포털 바로가기 ↗</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="panel">
              <h3>📋 정부 서비스 찾기</h3>
              <p>본인에게 해당하는 복지·생활 서비스를 검색하고 신청 조건을 확인하세요.</p>
              <p><a href="https://www.gov.kr/" target="_blank">정부24 바로가기 ↗</a></p>
              <p><a href="https://www.korea.kr/" target="_blank">대한민국 정책브리핑 ↗</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info("안내: 이 앱은 정부기관의 공식 서비스가 아닌 정보 안내용 예시 앱입니다. 지원사업의 신청 가능 여부를 보장하지 않습니다.")

# -----------------------------
# 대중교통 안내
# -----------------------------
elif page == "대중교통 안내":
    page_title("🚌 대중교통 안내", "한국에서 버스와 지하철을 이용할 때 알아두면 좋은 기본 정보")
    a, b = st.columns(2, gap="large")
    with a:
        st.markdown(
            """
            <div class="panel">
              <h3>교통카드와 요금</h3>
              <ul>
                <li>교통카드는 편의점이나 지하철역에서 구매·충전할 수 있습니다.</li>
                <li>버스에서는 승차할 때 카드를 단말기에 대고, 하차할 때도 태그해야 환승 할인이 적용될 수 있습니다.</li>
                <li>요금과 환승 규칙은 지역·노선에 따라 다릅니다.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            """
            <div class="panel">
              <h3>이용 예절과 안전</h3>
              <ul>
                <li>지하철에서는 내리는 승객이 먼저 내리도록 기다립니다.</li>
                <li>교통약자석은 필요한 승객을 배려합니다.</li>
                <li>분실물은 해당 교통기관 또는 경찰청 유실물 안내를 확인합니다.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("### 공식 길찾기·교통 정보")
    st.markdown("- [네이버 지도 — 대중교통 길찾기](https://map.naver.com/)")
    st.markdown("- [카카오맵 — 길찾기](https://map.kakao.com/)")
    st.markdown("- [경찰청 유실물 통합포털](https://www.lost112.go.kr/)")
    st.warning("출발 전 실제 운행 여부, 막차 시간, 요금은 지도 앱이나 해당 교통기관에서 확인하세요.")

# -----------------------------
# 문화 소개 + 생활 표현 번역 도움말
# -----------------------------
elif page == "우리 문화 홍보 및 번역":
    page_title("🗣️ 우리 문화 홍보 및 번역", "한국의 생활문화를 알아보고 일상에서 자주 쓰는 표현을 확인하세요.")
    culture = st.selectbox(
        "문화 주제 선택",
        ["인사와 존댓말", "식사 문화", "대중교통 예절", "분리배출"],
    )
    culture_info = {
        "인사와 존댓말": "처음 만난 사람이나 나이가 많은 사람에게는 존댓말을 쓰는 것이 일반적입니다. 상황에 따라 편한 말투가 달라질 수 있습니다.",
        "식사 문화": "함께 식사할 때는 다른 사람과 속도를 맞추고, 식사 전후에 인사를 건네면 좋습니다. 가정과 지역마다 차이가 있습니다.",
        "대중교통 예절": "대중교통에서는 큰 소리로 통화하지 않고, 내리는 사람을 먼저 배려하는 것이 좋습니다.",
        "분리배출": "쓰레기 배출 방법과 배출일은 지역마다 다릅니다. 거주지 지방자치단체의 안내를 확인하세요.",
    }
    st.markdown(
        f'<div class="panel"><h3>{culture}</h3><p>{culture_info[culture]}</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 생활 한국어 표현집")
    phrases = {
        "안녕하세요.": ("Hello.", "你好。", "Xin chào."),
        "감사합니다.": ("Thank you.", "谢谢。", "Cảm ơn."),
        "도와주세요.": ("Please help me.", "请帮帮我。", "Làm ơn giúp tôi."),
        "화장실이 어디예요?": ("Where is the restroom?", "洗手间在哪里？", "Nhà vệ sinh ở đâu?"),
        "천천히 말씀해 주세요.": ("Please speak slowly.", "请说慢一点。", "Xin hãy nói chậm lại."),
        "병원에 가고 싶어요.": ("I would like to go to a hospital.", "我想去医院。", "Tôi muốn đến bệnh viện."),
        "이 주소로 가 주세요.": ("Please take me to this address.", "请带我去这个地址。", "Xin hãy đưa tôi đến địa chỉ này."),
    }
    phrase = st.selectbox("한국어 표현", list(phrases.keys()))
    lang = st.radio("뜻 보기", ["영어", "중국어", "베트남어"], horizontal=True)
    lang_index = {"영어": 0, "중국어": 1, "베트남어": 2}[lang]
    st.success(f"**{lang}:** {phrases[phrase][lang_index]}")
    st.caption("간단한 참고용 표현집입니다. 중요한 행정·의료·법률 문서는 전문 통역 또는 공식 번역을 이용하세요.")
    st.markdown("### 다국어 지원 기관")
    st.markdown("- [다누리 포털](https://www.liveinkorea.kr/) — 다문화가족 및 생활 정보")
    st.markdown("- [외국인종합안내센터 1345](https://www.immigration.go.kr/) — 출입국·체류 관련 안내")

# -----------------------------
# 한국어 학습
# -----------------------------
elif page == "우리말 교육":
    page_title("📚 우리말 교육", "생활에서 바로 쓸 수 있는 기초 표현을 익혀 보세요.")
    level = st.selectbox("학습 주제", ["인사하기", "길 묻기", "가게에서", "도움 요청하기"])
    lessons = {
        "인사하기": [
            ("안녕하세요.", "Hello.", "처음 만났을 때 쓰는 기본 인사입니다."),
            ("감사합니다.", "Thank you.", "도움을 받거나 고마움을 표현할 때 씁니다."),
            ("죄송합니다.", "I'm sorry.", "사과하거나 양해를 구할 때 씁니다."),
        ],
        "길 묻기": [
            ("역이 어디예요?", "Where is the station?", "장소의 위치를 물어볼 때 씁니다."),
            ("여기서 가까워요?", "Is it near here?", "거리가 가까운지 물어볼 때 씁니다."),
            ("오른쪽으로 가세요.", "Go to the right.", "방향을 알려줄 때 쓰는 표현입니다."),
        ],
        "가게에서": [
            ("이거 얼마예요?", "How much is this?", "가격을 물어볼 때 씁니다."),
            ("카드로 결제할게요.", "I'll pay by card.", "카드 결제를 말할 때 씁니다."),
            ("봉투 주세요.", "A bag, please.", "봉투가 필요할 때 씁니다."),
        ],
        "도움 요청하기": [
            ("도와주세요.", "Please help me.", "도움이 필요할 때 쓰는 표현입니다."),
            ("다시 말씀해 주세요.", "Please say that again.", "잘 듣지 못했을 때 씁니다."),
            ("천천히 말씀해 주세요.", "Please speak slowly.", "말이 빠르게 느껴질 때 씁니다."),
        ],
    }
    for korean, english, explanation in lessons[level]:
        with st.container(border=True):
            st.markdown(f"**{korean}**")
            st.write(english)
            st.caption(explanation)

    st.markdown("### 짧은 복습 퀴즈")
    quiz = {
        "가격을 물어볼 때 알맞은 표현은?": {
            "options": ["이거 얼마예요?", "안녕히 주무세요.", "오른쪽으로 가세요."],
            "answer": "이거 얼마예요?",
            "explain": "‘이거 얼마예요?’는 물건의 가격을 물을 때 사용합니다.",
        },
        "상대방의 말을 잘 듣지 못했을 때는?": {
            "options": ["감사합니다.", "다시 말씀해 주세요.", "봉투 주세요."],
            "answer": "다시 말씀해 주세요.",
            "explain": "다시 말해 달라고 정중하게 부탁하는 표현입니다.",
        },
        "도움이 필요할 때는?": {
            "options": ["도와주세요.", "이거 얼마예요?", "역이 어디예요?"],
            "answer": "도와주세요.",
            "explain": "‘도와주세요.’는 도움이 필요할 때 쓰는 표현입니다.",
        },
    }
    question = st.selectbox("문제를 선택하세요", list(quiz.keys()))
    answer = st.radio("정답 선택", quiz[question]["options"], key="quiz_answer")
    if st.button("정답 확인", type="primary"):
        if answer == quiz[question]["answer"]:
            st.success("정답입니다! 잘하셨어요.")
        else:
            st.error("아직 정답이 아니에요. 표현을 다시 살펴보세요.")
        st.info(quiz[question]["explain"])

# -----------------------------
# 하단 공통 정보
# -----------------------------
st.divider()
st.caption(
    f"대한민국 이주시민 안내 · 정보 확인일 기준은 각 기관의 공지에 따릅니다 · © {date.today().year}"
)
