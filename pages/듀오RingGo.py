
import random
from io import BytesIO

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

st.set_page_config(
    page_title="듀오RING GO",
    page_icon="🌏",
    layout="wide",
)

st.markdown("""
<style>
.stApp { background: #f5f7ff; }
.block-container { max-width: 1100px; padding-top: 2rem; }
.hero {
    background: linear-gradient(120deg, #3457d5, #8054d8);
    padding: 32px; border-radius: 24px; color: white;
    margin-bottom: 24px;
}
.hero h1 { font-size: 38px; }
.panel {
    background: white; padding: 20px; border-radius: 16px;
    border: 1px solid #e7eaf4; margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

WORDS = [
    ("안녕하세요", "Hello", "안녕하세요? 만나서 반가워요."),
    ("감사합니다", "Thank you", "도와주셔서 감사합니다."),
    ("죄송합니다", "I'm sorry", "늦어서 죄송합니다."),
    ("괜찮아요", "It's okay", "걱정하지 마세요. 괜찮아요."),
    ("얼마예요?", "How much is it?", "이것은 얼마예요?"),
    ("화장실", "Restroom", "화장실이 어디에 있어요?"),
    ("병원", "Hospital", "몸이 아파서 병원에 가요."),
    ("도와주세요", "Please help me", "길을 잃었어요. 도와주세요."),
    ("천천히 말씀해 주세요", "Please speak slowly", "천천히 말씀해 주세요."),
    ("이해했어요", "I understood", "네, 이해했어요."),
    ("잘 모르겠어요", "I don't understand", "죄송하지만 잘 모르겠어요."),
    ("약국", "Pharmacy", "약국에서 약을 사요."),
    ("버스 정류장", "Bus stop", "버스 정류장은 저쪽에 있어요."),
    ("주민센터", "Community service center", "주민센터에 가요."),
    ("약속", "Appointment / promise", "내일 약속이 있어요."),
    ("주소", "Address", "주소를 적어 주세요."),
    ("왼쪽", "Left", "왼쪽으로 가세요."),
    ("오른쪽", "Right", "오른쪽으로 가세요."),
    ("도움", "Help", "도움이 필요해요."),
    ("한국어", "Korean language", "저는 한국어를 공부해요."),
]

GRAMMAR = [
    {
        "title": "은/는 — 주제 표시",
        "description": "문장에서 무엇에 대해 말하는지 나타내요. 받침이 없으면 는, 있으면 은을 사용해요.",
        "examples": ["저는 학생이에요.", "한국어는 재미있어요."],
        "question": "저___ 학생이에요.",
        "options": ["은", "는", "을", "에"],
        "answer": "는",
        "explanation": "‘저’에는 받침이 없어서 ‘는’을 사용해요.",
    },
    {
        "title": "이/가 — 주어 표시",
        "description": "누가 또는 무엇이 행동하거나 어떤 상태인지 나타내요.",
        "examples": ["친구가 와요.", "책이 있어요."],
        "question": "친구___ 학교에 와요.",
        "options": ["을", "가", "는", "에서"],
        "answer": "가",
        "explanation": "‘친구’에는 받침이 없으므로 ‘가’를 사용해요.",
    },
    {
        "title": "을/를 — 목적어 표시",
        "description": "동작의 대상을 나타내요. 받침이 있으면 을, 없으면 를을 사용해요.",
        "examples": ["밥을 먹어요.", "물을 마셔요.", "한국어를 배워요."],
        "question": "물___ 마셔요.",
        "options": ["은", "가", "을", "에서"],
        "answer": "을",
        "explanation": "‘물’에는 받침 ㄹ이 있어서 ‘을’을 사용해요.",
    },
    {
        "title": "에 — 시간·도착점",
        "description": "시간이나 이동의 도착점을 나타내요.",
        "examples": ["오전에 만나요.", "학교에 가요."],
        "question": "학교___ 가요.",
        "options": ["에서", "에", "을", "는"],
        "answer": "에",
        "explanation": "학교는 이동의 도착점이므로 ‘에’를 사용해요.",
    },
    {
        "title": "에서 — 행동이 일어나는 장소",
        "description": "행동이 일어나는 장소를 나타내요.",
        "examples": ["도서관에서 공부해요.", "집에서 쉬어요."],
        "question": "식당___ 밥을 먹어요.",
        "options": ["에", "를", "에서", "은"],
        "answer": "에서",
        "explanation": "밥을 먹는 행동이 일어나는 장소이므로 ‘에서’를 사용해요.",
    },
    {
        "title": "-고 싶어요 — 희망",
        "description": "하고 싶은 일을 말할 때 사용해요.",
        "examples": ["한국어를 배우고 싶어요.", "한국 음식을 먹고 싶어요."],
        "question": "한국어를 배우___ 싶어요.",
        "options": ["고", "은", "에", "에서"],
        "answer": "고",
        "explanation": "동사 어간 뒤에 ‘-고 싶어요’를 붙여요.",
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
        "why": "배우는 행동이 일어나는 장소이므로 ‘에서’를 사용해요.",
    },
    {
        "q": "‘천천히 말씀해 주세요’의 뜻은 무엇입니까?",
        "options": [
            "Please wait here",
            "Please speak slowly",
            "Please write it",
            "Please come tomorrow",
        ],
        "answer": "Please speak slowly",
        "why": "상대방에게 천천히 말해 달라고 부탁하는 표현이에요.",
    },
    {
        "q": "A: 감사합니다. B: ___.",
        "options": ["천만에요", "어디예요?", "얼마예요?", "잘 먹겠습니다"],
        "answer": "천만에요",
        "why": "‘천만에요’는 감사 인사에 답할 때 쓸 수 있어요.",
    },
    {
        "q": "병원에 가는 이유로 알맞은 것은 무엇입니까?",
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

if "learned" not in st.session_state:
    st.session_state.learned = []
if "saved" not in st.session_state:
    st.session_state.saved = []
if "word_score" not in st.session_state:
    st.session_state.word_score = 0
if "word_total" not in st.session_state:
    st.session_state.word_total = 0
if "grammar_score" not in st.session_state:
    st.session_state.grammar_score = 0
if "grammar_total" not in st.session_state:
    st.session_state.grammar_total = 0
if "exam_history" not in st.session_state:
    st.session_state.exam_history = []
if "translated" not in st.session_state:
    st.session_state.translated = ""
if "word_q" not in st.session_state:
    st.session_state.word_q = None
if "word_done" not in st.session_state:
    st.session_state.word_done = False
if "grammar_q" not in st.session_state:
    st.session_state.grammar_q = None
if "grammar_done" not in st.session_state:
    st.session_state.grammar_done = False
if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False

def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def audio_for(text, lang="ko"):
    try:
        output = BytesIO()
        gTTS(text=text, lang=lang).write_to_fp(output)
        output.seek(0)
        return output
    except Exception:
        return None

with st.sidebar:
    st.markdown("## 🌏 듀오RING GO")
    st.caption("언어를 잇고, 문화를 이해하다")
    page = st.radio(
        "메뉴",
        [
            "🏠 대시보드",
            "🔤 한글 학습",
            "🌐 번역 & 발음",
            "📚 단어 학습",
            "🧩 문법 학습",
            "📝 모의시험",
            "📈 학습 기록",
        ],
    )
    st.divider()
    st.caption("작은 한마디가 큰 이해를 만들어요.")

if page == "🏠 대시보드":
    hero("안녕하세요! 듀오RING GO 🌏", "한국어를 배우고 일상에서 자신 있게 소통해요.")
    st.markdown("### 오늘의 학습")
    a, b, c = st.columns(3)
    a.metric("학습한 단어", f"{len(st.session_state.learned)}개")
    b.metric("누적 퀴즈 정답", f"{st.session_state.word_score + st.session_state.grammar_score}개")
    c.metric("모의시험 응시", f"{len(st.session_state.exam_history)}회")

    st.markdown('<div class="panel"><h2>오늘의 표현</h2><h3>천천히 말씀해 주세요.</h3><p>Please speak slowly.</p><p>상대방의 말을 이해하기 어려울 때 정중하게 부탁할 수 있어요.</p></div>', unsafe_allow_html=True)
    if st.button("오늘의 표현 발음 듣기"):
        audio = audio_for("천천히 말씀해 주세요.")
        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.warning("음성 생성에 실패했어요. 인터넷 연결을 확인해 주세요.")

    st.info("학습 팁: 하루에 단어 5개와 문법 1개씩 공부해 보세요.")

elif page == "🔤 한글 학습":
    hero("한글 학습실 🔤", "자음과 모음을 익히고 글자를 읽는 연습을 해요.")
    tab1, tab2, tab3 = st.tabs(["자음", "모음", "글자 조합"])
    consonants = [
        ("ㄱ", "기역", "가방"), ("ㄴ", "니은", "나무"),
        ("ㄷ", "디귿", "다리"), ("ㄹ", "리을", "라디오"),
        ("ㅁ", "미음", "모자"), ("ㅂ", "비읍", "바나나"),
        ("ㅅ", "시옷", "사과"), ("ㅇ", "이응", "아이"),
        ("ㅈ", "지읒", "자동차"), ("ㅊ", "치읓", "친구"),
        ("ㅋ", "키읔", "커피"), ("ㅌ", "티읕", "토마토"),
        ("ㅍ", "피읖", "포도"), ("ㅎ", "히읗", "하늘"),
    ]
    vowels = [
        ("ㅏ", "아", "a"), ("ㅑ", "야", "ya"),
        ("ㅓ", "어", "eo"), ("ㅕ", "여", "yeo"),
        ("ㅗ", "오", "o"), ("ㅛ", "요", "yo"),
        ("ㅜ", "우", "u"), ("ㅠ", "유", "yu"),
        ("ㅡ", "으", "eu"), ("ㅣ", "이", "i"),
        ("ㅐ", "애", "ae"), ("ㅔ", "에", "e"),
    ]
    with tab1:
        cols = st.columns(4)
        for i, (letter, name, example) in enumerate(consonants):
            with cols[i % 4]:
                st.markdown(
                    f'<div class="panel"><h1 style="text-align:center">{letter}</h1><p style="text-align:center">{name}</p><p style="text-align:center">{example}</p></div>',
                    unsafe_allow_html=True,
                )
    with tab2:
        cols = st.columns(4)
        for i, (letter, example, sound) in enumerate(vowels):
            with cols[i % 4]:
                st.markdown(
                    f'<div class="panel"><h1 style="text-align:center">{letter}</h1><p style="text-align:center">{example}</p><p style="text-align:center">로마자: {sound}</p></div>',
                    unsafe_allow_html=True,
                )
    with tab3:
        st.markdown("""
        <div class="panel">
        <h2>ㄱ + ㅏ = 가</h2>
        <h2>ㄴ + ㅏ = 나</h2>
        <h2>ㅎ + ㅏ + ㄴ = 한</h2>
        <h2>한 + 국 + 어 = 한국어</h2>
        </div>
        """, unsafe_allow_html=True)
        st.caption("로마자 표기는 발음을 이해하기 위한 참고예요.")

elif page == "🌐 번역 & 발음":
    hero("번역 & 발음 🌐", "다른 언어의 단어나 문장을 한국어로 바꾸고 발음을 들어 보세요.")
    language = st.selectbox("입력 언어", list(LANGUAGES.keys()))
    source = st.text_area("번역할 문장", placeholder="예: I need help.")
    if st.button("한국어로 번역하기", type="primary"):
        if not source.strip():
            st.warning("번역할 문장을 입력해 주세요.")
        else:
            try:
                st.session_state.translated = GoogleTranslator(
                    source=LANGUAGES[language], target="ko"
                ).translate(source.strip())
            except Exception:
                st.error("번역에 실패했어요. 인터넷 연결을 확인해 주세요.")
    if st.session_state.translated:
        st.markdown("### 번역 결과")
        st.markdown(
            f'<div class="panel"><h2>{st.session_state.translated}</h2></div>',
            unsafe_allow_html=True,
        )
        if st.button("한국어 발음 듣기"):
            audio = audio_for(st.session_state.translated)
            if audio:
                st.audio(audio, format="audio/mp3")
            else:
                st.warning("음성 생성에 실패했어요. 인터넷 연결을 확인해 주세요.")
        st.caption("자동 번역은 문맥에 따라 다를 수 있어요. 중요한 내용은 확인해 주세요.")

elif page == "📚 단어 학습":
    hero("단어 학습실 📚", "일상에서 자주 쓰는 한국어 표현을 익혀요.")
    categories = sorted(set(v[0] for v in WORDS))
    search = st.text_input("단어 검색", placeholder="한국어 또는 영어")
    for ko, en, example in WORDS:
        if search and search.lower() not in ko.lower() and search.lower() not in en.lower():
            continue
        with st.expander(f"{ko} — {en}"):
            st.write(f"예문: {example}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("학습 완료", key=f"learn_{ko}"):
                    if ko not in st.session_state.learned:
                        st.session_state.learned.append(ko)
                    st.success("학습 기록에 추가했어요.")
            with col2:
                if st.button("복습 저장", key=f"save_{ko}"):
                    if ko not in st.session_state.saved:
                        st.session_state.saved.append(ko)
                    st.success("복습 목록에 저장했어요.")
            with col3:
                if st.button("발음 듣기", key=f"sound_{ko}"):
                    audio = audio_for(ko)
                    if audio:
                        st.audio(audio, format="audio/mp3")
                    else:
                        st.warning("음성을 만들지 못했어요.")

    st.divider()
    st.markdown("### 단어 퀴즈")
    if st.button("새 단어 문제"):
        correct = random.choice(WORDS)
        wrong = random.sample([v for v in WORDS if v != correct], 3)
        options = [v[0] for v in wrong] + [correct[0]]
        random.shuffle(options)
        st.session_state.word_q = {"correct": correct, "options": options}
        st.session_state.word_done = False

    q = st.session_state.word_q
    if q:
        st.write(f"‘{q['correct'][1]}’의 한국어 표현은 무엇일까요?")
        choice = st.radio("정답 선택", q["options"], key="word_choice")
        if st.button("정답 확인", disabled=st.session_state.word_done):
            st.session_state.word_done = True
            st.session_state.word_total += 1
            if choice == q["correct"][0]:
                st.session_state.word_score += 1
                st.success("정답이에요! 🎉")
            else:
                st.error(f"정답은 {q['correct'][0]}예요.")
            st.info(q["correct"][2])

elif page == "🧩 문법 학습":
    hero("문법 학습실 🧩", "설명과 예문으로 자연스러운 문장을 만들어 봐요.")
    for item in GRAMMAR:
        with st.expander(item["title"]):
            st.write(item["description"])
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
        st.write(q["question"])
        choice = st.radio("알맞은 답을 고르세요.", q["options"], key="grammar_choice")
        if st.button("문법 정답 확인", disabled=st.session_state.grammar_done):
            st.session_state.grammar_done = True
            st.session_state.grammar_total += 1
            if choice == q["answer"]:
                st.session_state.grammar_score += 1
                st.success("정답이에요! 🎉")
            else:
                st.error(f"정답은 ‘{q['answer']}’예요.")
            st.info(q["explanation"])

elif page == "📝 모의시험":
    hero("한국어 실전 모의시험 📝", "TOPIK 유형을 참고해 새로 만든 연습 문제예요. 공식 시험 문항은 아니에요.")
    count = st.selectbox("문제 수", [5, 8, 10])
    if st.button("시험 시작 / 새 시험", type="primary"):
        st.session_state.exam_questions = random.sample(TOPIK, count)
        st.session_state.exam_submitted = False
        st.session_state.exam_answers = {}

    questions = st.session_state.exam_questions
    if questions:
        if "exam_answers" not in st.session_state:
            st.session_state.exam_answers = {}
        for i, q in enumerate(questions):
            st.markdown(f"**문제 {i + 1}. {q['q']}**")
            st.session_state.exam_answers[i] = st.radio(
                f"{i + 1}번 답",
                q["options"],
                index=None,
                key=f"exam_{i}_{len(questions)}",
            )
        if st.button("시험 제출", disabled=st.session_state.exam_submitted):
            st.session_state.exam_submitted = True
            score = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.exam_answers.get(i) == q["answer"]
            )
            st.session_state.exam_history.append(
                {"score": score, "total": len(questions)}
            )
        if st.session_state.exam_submitted:
            score = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.exam_answers.get(i) == q["answer"]
            )
            st.metric("시험 점수", f"{score} / {len(questions)}", f"{round(score / len(questions) * 100)}%")
            for i, q in enumerate(questions):
                chosen = st.session_state.exam_answers.get(i)
                if chosen == q["answer"]:
                    st.success(f"{i + 1}번 정답: {q['answer']}")
                else:
                    st.error(f"{i + 1}번 정답: {q['answer']} (내 답: {chosen or '미응답'})")
                st.caption(q["why"])
    else:
        st.info("시험 시작 버튼을 눌러 문제를 받아 보세요.")

elif page == "📈 학습 기록":
    hero("나의 학습 기록 📈", "지금까지의 학습과 시험 결과를 확인해요.")
    a, b, c = st.columns(3)
    a.metric("학습한 단어", f"{len(st.session_state.learned)}개")
    b.metric("퀴즈 정답", f"{st.session_state.word_score + st.session_state.grammar_score}개")
    c.metric("모의시험 응시", f"{len(st.session_state.exam_history)}회")

    st.markdown("### 복습 단어")
    if st.session_state.saved:
        st.write(" · ".join(st.session_state.saved))
        if st.button("복습 목록 비우기"):
            st.session_state.saved = []
            st.rerun()
    else:
        st.caption("단어 학습실에서 복습할 단어를 저장해 보세요.")

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
        st.caption("아직 모의시험 기록이 없어요.")

    st.warning("학습 기록은 현재 세션에 저장되며 서버가 재시작되면 초기화될 수 있어요.")
