
import random
from io import BytesIO

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

st.set_page_config(
    page_title="듀오RING GO",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- 디자인 ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    background: #f7f6f3;
    color: #171717;
    font-family: 'Nunito', 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 1250px;
    padding: 1.3rem 2rem 3rem;
}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.brand {
    font-size: 29px;
    font-weight: 900;
    letter-spacing: -1.5px;
    color: #f21e36;
    padding: 3px 0 12px;
}
.brand span { color: #222; }

.hero {
    padding: 36px;
    min-height: 290px;
    border-radius: 23px;
    color: white;
    background:
        radial-gradient(circle at 82% 20%, #7256ce 0, transparent 28%),
        linear-gradient(115deg, #151526, #302348 58%, #9c304c);
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: 15px 0 28px;
}
.hero-tag {
    color: #ffb6c0;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 2px;
}
.hero h1 {
    color: white;
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 900;
    line-height: 1.18;
    margin: 10px 0;
}
.hero p { color: #e9e6f2; font-size: 16px; }
.section-title {
    font-size: 22px;
    font-weight: 900;
    margin: 24px 0 5px;
}
.section-subtitle { color: #777; font-size: 13px; margin-bottom: 14px; }

div.stButton > button {
    border-radius: 12px;
    font-weight: 800;
    min-height: 43px;
    border: 1px solid #e9e9ee;
    transition: .2s;
}
div.stButton > button:hover {
    border-color: #f21e36;
    color: #f21e36;
}
div.stButton > button[kind="primary"] {
    background: #f21e36;
    color: white;
    border: none;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 18px;
    border: 1px solid #ececf0;
    padding: 14px;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 17px;
    border: 1px solid #ececf0;
    border-radius: 15px;
}
div[data-testid="stMetricValue"] { font-weight: 900; }
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; }
div[data-testid="stExpander"] {
    background: white;
    border-radius: 13px;
    border: 1px solid #e9e9ef;
}
</style>
""", unsafe_allow_html=True)

# ---------------- 데이터 ----------------
WORDS = [
    ("안녕하세요", "Hello", "인사", "안녕하세요? 만나서 반가워요."),
    ("감사합니다", "Thank you", "인사", "도와주셔서 감사합니다."),
    ("죄송합니다", "I'm sorry", "인사", "늦어서 죄송합니다."),
    ("괜찮아요", "It's okay", "일상", "걱정하지 마세요. 괜찮아요."),
    ("얼마예요?", "How much is it?", "쇼핑", "이것은 얼마예요?"),
    ("화장실", "Restroom", "장소", "화장실이 어디에 있어요?"),
    ("병원", "Hospital", "장소", "몸이 아파서 병원에 가요."),
    ("도와주세요", "Please help me", "긴급", "도움이 필요해요. 도와주세요."),
    ("천천히 말씀해 주세요", "Please speak slowly", "대화", "죄송하지만 천천히 말씀해 주세요."),
    ("잘 모르겠어요", "I don't understand", "대화", "이 표현을 잘 모르겠어요."),
    ("약국", "Pharmacy", "장소", "약국에서 약을 사요."),
    ("버스 정류장", "Bus stop", "교통", "버스 정류장은 저쪽에 있어요."),
    ("주민센터", "Community service center", "생활", "주민센터에서 서류를 발급받아요."),
    ("주소", "Address", "생활", "주소를 적어 주세요."),
    ("왼쪽", "Left", "방향", "왼쪽으로 가세요."),
    ("오른쪽", "Right", "방향", "오른쪽으로 가세요."),
    ("한국어", "Korean language", "학습", "저는 한국어를 공부해요."),
    ("약속", "Appointment / promise", "일상", "내일 친구와 약속이 있어요."),
]

GRAMMAR = [
    {
        "title": "은/는 — 주제 표시",
        "desc": "무엇에 대해 말하는지 나타내요. 받침이 없으면 는, 있으면 은을 사용해요.",
        "examples": ["저는 학생이에요.", "한국어는 재미있어요."],
        "q": "저___ 학생이에요.",
        "options": ["은", "는", "을", "에"],
        "answer": "는",
        "why": "‘저’에는 받침이 없으므로 ‘는’을 사용해요.",
    },
    {
        "title": "이/가 — 주어 표시",
        "desc": "누가 또는 무엇이 행동하거나 어떤 상태인지 나타내요.",
        "examples": ["친구가 와요.", "책이 있어요."],
        "q": "친구___ 학교에 와요.",
        "options": ["을", "가", "는", "에서"],
        "answer": "가",
        "why": "‘친구’에는 받침이 없으므로 ‘가’를 사용해요.",
    },
    {
        "title": "을/를 — 목적어 표시",
        "desc": "동작의 대상을 나타내요. 받침이 있으면 을, 없으면 를을 사용해요.",
        "examples": ["밥을 먹어요.", "물을 마셔요.", "한국어를 배워요."],
        "q": "물___ 마셔요.",
        "options": ["은", "가", "을", "에서"],
        "answer": "을",
        "why": "‘물’에는 받침 ㄹ이 있으므로 ‘을’을 사용해요.",
    },
    {
        "title": "에 — 시간·도착점",
        "desc": "시간이나 이동의 도착점을 나타내요.",
        "examples": ["오전에 만나요.", "학교에 가요."],
        "q": "학교___ 가요.",
        "options": ["에서", "에", "을", "는"],
        "answer": "에",
        "why": "학교는 이동의 도착점이므로 ‘에’를 사용해요.",
    },
    {
        "title": "에서 — 행동이 일어나는 장소",
        "desc": "어떤 행동이 일어나는 장소를 나타내요.",
        "examples": ["도서관에서 공부해요.", "집에서 쉬어요."],
        "q": "식당___ 밥을 먹어요.",
        "options": ["에", "를", "에서", "은"],
        "answer": "에서",
        "why": "밥을 먹는 행동이 일어나는 장소이므로 ‘에서’를 사용해요.",
    },
    {
        "title": "-고 싶어요 — 희망",
        "desc": "하고 싶은 일을 말할 때 사용해요.",
        "examples": ["한국어를 배우고 싶어요.", "한국 음식을 먹고 싶어요."],
        "q": "한국어를 배우___ 싶어요.",
        "options": ["고", "은", "에", "에서"],
        "answer": "고",
        "why": "동사 어간 뒤에 ‘-고 싶어요’를 붙여요.",
    },
]

TOPIK = [
    {
        "q": "‘도서관’은 무슨 뜻입니까?",
        "options": ["Hospital", "Library", "Restaurant", "Airport"],
        "answer": "Library",
        "why": "도서관은 책을 읽거나 빌릴 수 있는 곳이에요.",
    },
    {
        "q": "저는 매일 한국어를 ___.",
        "options": ["공부해요", "공부예요", "공부에서", "공부하고"],
        "answer": "공부해요",
        "why": "‘공부하다’의 현재형은 ‘공부해요’예요.",
    },
    {
        "q": "감사의 표현은 무엇입니까?",
        "options": ["안녕히 가세요", "감사합니다", "죄송합니다", "괜찮아요"],
        "answer": "감사합니다",
        "why": "‘감사합니다’는 고마움을 표현하는 말이에요.",
    },
    {
        "q": "약국에서 주로 무엇을 합니까?",
        "options": ["책을 빌립니다", "약을 삽니다", "버스를 탑니다", "운동을 합니다"],
        "answer": "약을 삽니다",
        "why": "약국에서는 약을 살 수 있어요.",
    },
    {
        "q": "학교___ 한국어를 배워요.",
        "options": ["에서", "을", "는", "와"],
        "answer": "에서",
        "why": "행동이 일어나는 장소이므로 ‘에서’를 사용해요.",
    },
    {
        "q": "‘천천히 말씀해 주세요’의 뜻은?",
        "options": ["Please wait here", "Please speak slowly", "Please write it", "Please come tomorrow"],
        "answer": "Please speak slowly",
        "why": "천천히 말해 달라고 부탁하는 표현이에요.",
    },
    {
        "q": "A: 감사합니다. B: ___.",
        "options": ["천만에요", "어디예요?", "얼마예요?", "잘 먹겠습니다"],
        "answer": "천만에요",
        "why": "‘천만에요’는 감사 인사에 답할 때 쓸 수 있어요.",
    },
    {
        "q": "병원에 가는 이유로 알맞은 것은?",
        "options": ["책을 빌리려고", "몸이 아파서", "버스를 타려고", "옷을 사려고"],
        "answer": "몸이 아파서",
        "why": "병원은 진료를 받기 위해 가는 곳이에요.",
    },
    {
        "q": "저는 물___ 마셔요.",
        "options": ["을", "에", "에서", "은"],
        "answer": "을",
        "why": "‘물’은 ‘마시다’의 목적어이므로 ‘을’을 사용해요.",
    },
    {
        "q": "‘오른쪽’의 반대말은 무엇입니까?",
        "options": ["위쪽", "왼쪽", "앞쪽", "안쪽"],
        "answer": "왼쪽",
        "why": "‘오른쪽’의 반대 방향은 ‘왼쪽’이에요.",
    },
]

LANGUAGES = {
    "영어": "en",
    "일본어": "ja",
    "중국어(간체)": "zh-CN",
    "베트남어": "vi",
    "태국어": "th",
    "인도네시아어": "id",
    "프랑스어": "fr",
    "스페인어": "es",
    "러시아어": "ru",
    "아랍어": "ar",
    "우즈베크어": "uz",
    "몽골어": "mn",
    "네팔어": "ne",
    "필리핀어": "tl",
    "독일어": "de",
}

# ---------------- 상태 ----------------
DEFAULTS = {
    "page": "홈",
    "learned": [],
    "saved": [],
    "word_score": 0,
    "word_total": 0,
    "grammar_score": 0,
    "grammar_total": 0,
    "exam_history": [],
    "translated": "",
    "word_q": None,
    "word_done": False,
    "grammar_q": None,
    "grammar_done": False,
    "exam_questions": [],
    "exam_answers": {},
    "exam_submitted": False,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

def go(page):
    st.session_state.page = page
    st.rerun()

def audio_for(text, lang="ko"):
    try:
        data = BytesIO()
        gTTS(text=text, lang=lang).write_to_fp(data)
        data.seek(0)
        return data
    except Exception:
        return None

def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="hero-tag">DUORING GO · KOREAN LEARNING</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def content_card(emoji, title, subtitle, target, color):
    with st.container(border=True):
        st.markdown(
            f'<div style="background:{color};border-radius:13px;padding:22px 10px;'
            f'text-align:center;font-size:42px">{emoji}</div>'
            f'<h3 style="margin:13px 0 4px">{title}</h3>'
            f'<p style="color:#777;font-size:13px;min-height:36px">{subtitle}</p>',
            unsafe_allow_html=True,
        )
        if st.button("지금 학습하기 →", key=f"card_{target}", use_container_width=True):
            go(target)

# ---------------- 상단 메뉴 ----------------
top1, top2 = st.columns([3, 7])
with top1:
    st.markdown('<div class="brand">듀오RING <span>GO</span></div>', unsafe_allow_html=True)
with top2:
    nav = st.columns(6)
    nav_items = [
        ("홈", "🏠 홈"),
        ("한글", "🔤 한글"),
        ("번역", "🌐 번역"),
        ("단어", "📚 단어"),
        ("문법", "🧩 문법"),
        ("시험", "📝 시험"),
    ]
    for col, (label, target) in zip(nav, nav_items):
        with col:
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                go(target)

st.divider()

# ---------------- 홈 ----------------
if st.session_state.page == "홈":
    st.markdown("""
    <div class="hero">
      <div class="hero-tag">YOUR KOREAN JOURNEY STARTS HERE</div>
      <h1>새로운 언어,<br>더 가까워지는 일상.</h1>
      <p>한국어를 배우고 문화를 이해하며 자신 있게 소통해요.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶  오늘의 학습 시작하기", type="primary", use_container_width=True):
        go("단어")

    st.markdown('<div class="section-title">오늘의 학습 코스</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">카드를 눌러 원하는 학습 공간으로 이동하세요.</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        content_card("🔤", "한글 스타트", "자음과 모음부터 시작해요.", "한글", "#e6ecff")
    with cols[1]:
        content_card("🌐", "번역 & 발음", "모르는 말을 한국어로 바꿔요.", "번역", "#ffe8e8")
    with cols[2]:
        content_card("📚", "생활 단어", "일상에서 쓰는 단어를 익혀요.", "단어", "#fff0d8")
    with cols[3]:
        content_card("🧩", "쉬운 문법", "예문과 퀴즈로 문법을 배워요.", "문법", "#e6f7ec")

    st.markdown('<div class="section-title">인기 학습 콘텐츠</div>', unsafe_allow_html=True)
    cols = st.columns([1, 1, 1])
    with cols[0]:
        st.markdown('<div class="panel"><div style="font-size:35px">💬</div><b>일상 대화</b><p style="color:#777">인사와 부탁 표현을 익혀요.</p></div>', unsafe_allow_html=True)
        if st.button("대화 단어 보기", key="daily_words", use_container_width=True):
            go("단어")
    with cols[1]:
        st.markdown('<div class="panel"><div style="font-size:35px">🎯</div><b>실전 모의시험</b><p style="color:#777">TOPIK 유형 연습 문제를 풀어요.</p></div>', unsafe_allow_html=True)
        if st.button("시험 보러 가기", key="daily_exam", use_container_width=True):
            go("시험")
    with cols[2]:
        st.markdown('<div class="panel"><div style="font-size:35px">📈</div><b>나의 학습 기록</b><p style="color:#777">학습 진도를 확인해요.</p></div>', unsafe_allow_html=True)
        if st.button("기록 확인하기", key="daily_stats", use_container_width=True):
            go("기록")

    st.markdown('<div class="section-title">나의 학습 현황</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    a.metric("학습한 단어", f"{len(st.session_state.learned)}개")
    b.metric("퀴즈 정답", f"{st.session_state.word_score + st.session_state.grammar_score}개")
    c.metric("시험 응시", f"{len(st.session_state.exam_history)}회")

# ---------------- 한글 ----------------
elif st.session_state.page == "한글":
    hero("한글 학습실", "자음과 모음을 익히고 글자를 읽는 연습을 해요.")
    tab1, tab2, tab3 = st.tabs(["자음", "모음", "글자 조합"])
    consonants = [
        ("ㄱ", "기역", "가방"), ("ㄴ", "니은", "나무"), ("ㄷ", "디귿", "다리"),
        ("ㄹ", "리을", "라디오"), ("ㅁ", "미음", "모자"), ("ㅂ", "비읍", "바나나"),
        ("ㅅ", "시옷", "사과"), ("ㅇ", "이응", "아이"), ("ㅈ", "지읒", "자동차"),
        ("ㅊ", "치읓", "친구"), ("ㅋ", "키읔", "커피"), ("ㅌ", "티읕", "토마토"),
        ("ㅍ", "피읖", "포도"), ("ㅎ", "히읗", "하늘"),
    ]
    vowels = [
        ("ㅏ", "아", "a"), ("ㅑ", "야", "ya"), ("ㅓ", "어", "eo"),
        ("ㅕ", "여", "yeo"), ("ㅗ", "오", "o"), ("ㅛ", "요", "yo"),
        ("ㅜ", "우", "u"), ("ㅠ", "유", "yu"), ("ㅡ", "으", "eu"),
        ("ㅣ", "이", "i"), ("ㅐ", "애", "ae"), ("ㅔ", "에", "e"),
    ]
    with tab1:
        cols = st.columns(4)
        for i, (letter, name, example) in enumerate(consonants):
            with cols[i % 4]:
                st.markdown(f'<div class="panel" style="text-align:center"><h1>{letter}</h1><b>{name}</b><p>{example}</p></div>', unsafe_allow_html=True)
    with tab2:
        cols = st.columns(4)
        for i, (letter, example, sound) in enumerate(vowels):
            with cols[i % 4]:
                st.markdown(f'<div class="panel" style="text-align:center"><h1>{letter}</h1><b>{example}</b><p>로마자: {sound}</p></div>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<div class="panel"><h2>ㄱ + ㅏ = 가</h2><h2>ㄴ + ㅏ = 나</h2><h2>ㅎ + ㅏ + ㄴ = 한</h2><h2>한 + 국 + 어 = 한국어</h2></div>', unsafe_allow_html=True)

# ---------------- 번역 ----------------
elif st.session_state.page == "번역":
    hero("번역 & 발음", "다른 언어를 한국어로 번역하고 발음을 들어 보세요.")
    language = st.selectbox("입력 언어", list(LANGUAGES.keys()))
    source = st.text_area("번역할 단어나 문장", placeholder="예: I need help.", height=130)
    if st.button("한국어로 번역하기", type="primary", use_container_width=True):
        if not source.strip():
            st.warning("먼저 번역할 내용을 입력해 주세요.")
        else:
            try:
                st.session_state.translated = GoogleTranslator(
                    source=LANGUAGES[language], target="ko"
                ).translate(source.strip())
            except Exception:
                st.error("번역에 실패했어요. 인터넷 연결을 확인해 주세요.")
    if st.session_state.translated:
        st.markdown("### 번역 결과")
        st.markdown(f'<div class="panel"><h2>{st.session_state.translated}</h2></div>', unsafe_allow_html=True)
        if st.button("🔊 한국어 발음 듣기", use_container_width=True):
            audio = audio_for(st.session_state.translated)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.warning("음성 생성에 실패했어요. 인터넷 연결을 확인해 주세요.")
        st.caption("자동 번역은 문맥에 따라 어색할 수 있으니 중요한 내용은 다시 확인해 주세요.")

# ---------------- 단어 ----------------
elif st.session_state.page == "단어":
    hero("생활 한국어 단어", "매일 자주 쓰는 단어를 배우고 발음을 연습해요.")
    search = st.text_input("단어 검색", placeholder="한국어 또는 영어로 검색")
    for ko, en, category, example in WORDS:
        if search and search.lower() not in ko.lower() and search.lower() not in en.lower():
            continue
        with st.expander(f"{ko}  ·  {en}"):
            st.caption(f"분류: {category}")
            st.write(f"예문: {example}")
            a, b = st.columns(2)
            with a:
                if st.button("학습 완료", key=f"learn_{ko}", use_container_width=True):
                    if ko not in st.session_state.learned:
                        st.session_state.learned.append(ko)
                    st.success("학습 기록에 추가했어요.")
            with b:
                if st.button("복습 목록에 저장", key=f"save_{ko}", use_container_width=True):
                    if ko not in st.session_state.saved:
                        st.session_state.saved.append(ko)
                    st.success("복습 목록에 저장했어요.")
            if st.button("🔊 발음 듣기", key=f"audio_{ko}"):
                audio = audio_for(ko)
                if audio:
                    st.audio(audio, format="audio/mp3")
                else:
                    st.warning("음성 생성에 실패했어요.")

    st.divider()
    st.markdown("### 단어 퀴즈")
    if st.button("새 문제 받기"):
        correct = random.choice(WORDS)
        wrong = random.sample([v for v in WORDS if v != correct], 3)
        options = [v[0] for v in wrong] + [correct[0]]
        random.shuffle(options)
        st.session_state.word_q = {"correct": correct, "options": options}
        st.session_state.word_done = False

    q = st.session_state.word_q
    if q:
        st.write(f"**‘{q['correct'][1]}’의 한국어 표현은 무엇일까요?**")
        choice = st.radio("정답 선택", q["options"], key="word_choice")
        if st.button("정답 확인", disabled=st.session_state.word_done):
            st.session_state.word_done = True
            st.session_state.word_total += 1
            if choice == q["correct"][0]:
                st.session_state.word_score += 1
                st.success("정답이에요! 🎉")
            else:
                st.error(f"정답은 ‘{q['correct'][0]}’예요.")
            st.info(q["correct"][3])

# ---------------- 문법 ----------------
elif st.session_state.page == "문법":
    hero("쉬운 한국어 문법", "설명과 예문으로 자연스러운 문장을 만들어 봐요.")
    for item in GRAMMAR:
        with st.expander(item["title"]):
            st.write(item["desc"])
            st.markdown("**예문**")
            for example in item["examples"]:
                st.write("• " + example)

    st.divider()
    st.markdown("### 문법 퀴즈")
    if st.button("새 문법 문제"):
        st.session_state.grammar_q = random.choice(GRAMMAR)
        st.session_state.grammar_done = False
    q = st.session_state.grammar_q
    if q:
        st.write(f"**{q['q']}**")
        choice = st.radio("알맞은 답을 고르세요.", q["options"], key="grammar_choice")
        if st.button("정답 확인", disabled=st.session_state.grammar_done):
            st.session_state.grammar_done = True
            st.session_state.grammar_total += 1
            if choice == q["answer"]:
                st.session_state.grammar_score += 1
                st.success("정답이에요! 🎉")
            else:
                st.error(f"정답은 ‘{q['answer']}’예요.")
            st.info(q["why"])

# ---------------- 모의시험 ----------------
elif st.session_state.page == "시험":
    hero("한국어 실전 모의시험", "TOPIK 유형을 참고해 새로 만든 연습 문제를 풀어 보세요.")
    st.caption("공식 TOPIK 기출문제가 아닌 자체 제작 연습 문제입니다.")
    count = st.selectbox("문제 수", [5, 8, 10])
    if st.button("시험 시작 / 새 시험", type="primary", use_container_width=True):
        st.session_state.exam_questions = random.sample(TOPIK, count)
        st.session_state.exam_submitted = False
        st.session_state.exam_answers = {}

    questions = st.session_state.exam_questions
    if questions:
        for i, q in enumerate(questions):
            st.markdown(f'<div class="panel"><b>문제 {i+1}. {q["q"]}</b></div>', unsafe_allow_html=True)
            st.session_state.exam_answers[i] = st.radio(
                f"{i+1}번 답", q["options"], index=None,
                key=f"exam_{len(questions)}_{i}",
            )
        if st.button("시험 제출", disabled=st.session_state.exam_submitted, use_container_width=True):
            st.session_state.exam_submitted = True
            score = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.exam_answers.get(i) == q["answer"]
            )
            st.session_state.exam_history.append({"score": score, "total": len(questions)})

        if st.session_state.exam_submitted:
            score = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.exam_answers.get(i) == q["answer"]
            )
            st.metric("시험 점수", f"{score} / {len(questions)}", f"{round(score / len(questions) * 100)}%")
            for i, q in enumerate(questions):
                chosen = st.session_state.exam_answers.get(i)
                if chosen == q["answer"]:
                    st.success(f"{i+1}번 정답: {q['answer']}")
                else:
                    st.error(f"{i+1}번 정답: {q['answer']} (내 답: {chosen or '미응답'})")
                st.caption(q["why"])
    else:
        st.info("시험 시작을 눌러 문제를 받아 보세요.")

# ---------------- 기록 ----------------
elif st.session_state.page == "기록":
    hero("나의 학습 기록", "지금까지의 학습 진도와 시험 결과를 확인해요.")
    a, b, c = st.columns(3)
    a.metric("학습한 단어", f"{len(st.session_state.learned)}개")
    b.metric("퀴즈 정답", f"{st.session_state.word_score + st.session_state.grammar_score}개")
    c.metric("시험 응시", f"{len(st.session_state.exam_history)}회")

    st.markdown("### 복습 단어")
    if st.session_state.saved:
        st.write(" · ".join(st.session_state.saved))
        if st.button("복습 목록 비우기"):
            st.session_state.saved = []
            st.rerun()
    else:
        st.caption("단어 화면에서 복습할 단어를 저장해 보세요.")

    total = st.session_state.word_total + st.session_state.grammar_total
    correct = st.session_state.word_score + st.session_state.grammar_score
    st.markdown("### 퀴즈 정답률")
    if total:
        st.progress(correct / total)
        st.write(f"{correct} / {total}문제 정답 ({round(correct / total * 100)}%)")
    else:
        st.caption("퀴즈를 풀면 결과가 여기에 표시돼요.")

    st.markdown("### 모의시험 기록")
    if st.session_state.exam_history:
        for i, result in enumerate(st.session_state.exam_history, 1):
            st.write(f"{i}. {result['score']} / {result['total']}점")
    else:
        st.caption("아직 응시한 시험이 없어요.")

    st.warning("학습 기록은 현재 세션에 저장되며 서버가 재시작되면 초기화될 수 있어요.")
