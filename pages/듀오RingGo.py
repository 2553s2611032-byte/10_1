import streamlit as st
import html
import urllib.parse
import urllib.request
import json
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#12251b">
<title>듀오RINGGO | 한국어 학습</title>
<style>
:root{--dark:#12251b;--green:#c4f477;--bg:#f5f7f2;--white:#fff;--muted:#7b857c;--line:#e5e9e1}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:#1b281f;font-family:Arial,"Noto Sans KR",sans-serif}
button,input,select,textarea{font:inherit}
button{cursor:pointer}
button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #82ae54;outline-offset:2px}
.app{max-width:1200px;margin:auto;padding:20px}
header{display:flex;justify-content:space-between;align-items:center;padding:8px 0 25px}
.brand{font-size:23px;font-weight:900;letter-spacing:-1px}
.brand span{color:#709f36}
.logo{display:inline-grid;place-items:center;background:var(--dark);color:var(--green);width:42px;height:42px;border-radius:14px;margin-right:9px}
.streak{background:white;border:1px solid var(--line);padding:11px 15px;border-radius:30px;font-size:13px}
.layout{display:grid;grid-template-columns:205px minmax(0,1fr);gap:25px}
aside{display:flex;flex-direction:column;gap:7px}
.label{font-size:10px;color:var(--muted);letter-spacing:2px;font-weight:bold;padding:17px 12px 8px}
.nav{border:0;background:transparent;text-align:left;padding:14px;border-radius:12px;color:#647067;font-weight:bold;font-size:14px}
.nav.active{background:var(--dark);color:white}
.nav.active .ico{color:var(--green)}
.ico{display:inline-block;width:27px;font-size:18px}
.goal{background:#e8f4d9;padding:18px;border-radius:17px;margin-top:25px;font-size:12px;line-height:1.7}
.goal strong{font-size:14px}
.progress{height:6px;background:#e1e7dc;border-radius:20px;overflow:hidden;margin:12px 0}
.progress div{height:100%;width:0;background:#7ba848;transition:width .2s}
main{min-width:0}
.page{display:none}
.page.active{display:block;animation:appear .2s}
@keyframes appear{from{opacity:.5;transform:translateY(4px)}to{opacity:1;transform:none}}
.hero{background:var(--dark);color:white;padding:34px;border-radius:25px;position:relative;overflow:hidden}
.hero:after{content:"가";position:absolute;right:30px;top:-65px;font-size:230px;font-weight:bold;color:#ffffff0b}
.eyebrow{font-size:11px;letter-spacing:2px;color:#b8eb7c;font-weight:bold}
h1{font-size:clamp(29px,4vw,43px);letter-spacing:-1.5px;line-height:1.25;margin:16px 0}
.hero p{font-size:13px;line-height:1.9;color:#d0d9d0}
.primary,.secondary{border:0;border-radius:11px;padding:12px 17px;font-size:13px;font-weight:bold}
.primary{background:var(--green);color:#1d321c}
.secondary{background:white;border:1px solid var(--line);color:#28352b}
.hero .primary{margin-top:9px}
.section-head{display:flex;justify-content:space-between;align-items:center;margin:28px 0 14px}
.section-head h2{font-size:18px;margin:0}
.section-head p{font-size:12px;color:var(--muted);margin:6px 0 0}
.stats,.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.stat,.card,.panel{background:white;border:1px solid var(--line);border-radius:18px;padding:19px}
.stat strong{display:block;font-size:26px;margin:13px 0 5px}
.stat small{font-size:11px;color:var(--muted)}
.card{transition:transform .15s}
.card:hover{transform:translateY(-2px)}
.card-icon{width:43px;height:43px;display:grid;place-items:center;background:#eef5e5;border-radius:13px;font-size:22px}
.card h3{font-size:15px;margin:14px 0 8px}
.card p{font-size:12px;color:var(--muted);line-height:1.8;min-height:45px}
.card button{border:0;background:none;color:#5b8b32;font-size:12px;font-weight:bold;padding:0}
.page-title{font-size:31px;letter-spacing:-1px;margin:12px 0}
.subtitle{font-size:13px;line-height:1.9;color:var(--muted);margin-bottom:23px}
.field-label{display:block;font-size:12px;font-weight:bold;margin:17px 0 8px}
.field{width:100%;padding:13px;border:1px solid #dfe5dc;border-radius:11px;background:white;color:#1b281f}
textarea.field{min-height:115px;resize:vertical;line-height:1.7}
.row{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin-top:13px}
.hint{font-size:11px;color:var(--muted);line-height:1.8;margin-top:12px}
.result{background:#f0f6e9;padding:20px;border-radius:16px;margin-top:20px;overflow-wrap:anywhere}
.result h3{font-size:11px;color:#648b40}
.big-result{font-size:27px;font-weight:bold;line-height:1.6}
.result-meta{font-size:12px;color:#6b7765;margin-top:9px}
.tabs{display:flex;gap:7px;flex-wrap:wrap;margin:16px 0}
.tab{background:white;border:1px solid var(--line);padding:9px 14px;border-radius:30px;font-size:12px;font-weight:bold}
.tab.active{background:var(--dark);color:white}
.hangul-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:9px}
.letter{border:1px solid var(--line);border-radius:13px;padding:12px 3px;text-align:center;background:white}
.letter strong{font-size:28px;display:block}
.letter small{font-size:10px;color:var(--muted);display:block;margin-top:5px}
.letter button{border:0;background:none;color:#598833;font-size:11px;margin-top:7px}
.grammar-item{background:white;border:1px solid var(--line);border-radius:15px;padding:18px;margin-top:11px}
.grammar-item h3{font-size:16px;margin:13px 0 7px}
.grammar-item p{font-size:13px;color:var(--muted);line-height:1.8}
.example{background:#f4f6f0;padding:13px;border-radius:10px;font-size:13px;line-height:1.9;white-space:pre-line}
.pill{background:#edf4e6;padding:6px 10px;border-radius:20px;font-size:11px}
.quiz-top{display:flex;justify-content:space-between;color:var(--muted);font-size:12px}
.question{font-size:20px;line-height:1.8;font-weight:bold;margin:23px 0}
.choices{display:grid;gap:9px}
.choice{padding:14px;text-align:left;border:1px solid var(--line);border-radius:12px;background:white;font-size:14px}
.choice:hover:not(:disabled){border-color:#8eae70}
.choice.correct{background:#eaf7e2;border-color:#77ac50}
.choice.wrong{background:#fff0ec;border-color:#d88b78}
.feedback{padding:14px;border-radius:12px;margin-top:14px;font-size:13px;line-height:1.8}
.good{background:#eaf7e2;color:#315d25}
.bad{background:#fff0ec;color:#854337}
.note{background:#f0f3ed;border-radius:12px;padding:15px;font-size:12px;line-height:1.9;color:#687267;margin-top:16px}
footer{text-align:center;color:#9aa39a;font-size:11px;padding:30px 0 10px}
.mobile-nav{display:none}
@media(max-width:800px){
 .app{padding:13px 14px 90px}.layout{display:block}aside{display:none}
 .mobile-nav{display:flex;position:fixed;z-index:10;bottom:0;left:0;right:0;background:white;border-top:1px solid var(--line);justify-content:space-around;padding:8px 2px max(8px,env(safe-area-inset-bottom))}
 .mobile-nav .nav{display:flex;flex-direction:column;align-items:center;padding:5px 8px;gap:3px;font-size:10px}
 .mobile-nav .ico{width:auto;font-size:18px}
 .cards{grid-template-columns:repeat(2,minmax(0,1fr))}
 .hero{padding:25px}.hero:after{right:0;font-size:170px}
}
@media(max-width:430px){
 .app{padding-left:10px;padding-right:10px}
 .brand{font-size:19px}.logo{width:36px;height:36px}
 .stats{gap:7px}.stat{padding:12px}.stat strong{font-size:21px}
 .stat small{font-size:10px}.cards{gap:8px}.card{padding:13px}
 .panel{padding:15px}.hangul-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
 .hero h1{font-size:29px}
}
</style>
</head>
<body>
<div class="app">
<header>
 <div class="brand"><span class="logo">ㄱ</span>듀오<span>RINGGO</span></div>
 <div class="streak">🔥 <b id="streak">0</b>일 학습</div>
</header>

<div class="layout">
<aside>
 <div class="label">LEARNING SPACE</div>
 <button class="nav active" data-page="home"><span class="ico">⌂</span>학습 홈</button>
 <button class="nav" data-page="translate"><span class="ico">文</span>번역 & 발음</button>
 <button class="nav" data-page="hangul"><span class="ico">가</span>한글 배우기</button>
 <button class="nav" data-page="grammar"><span class="ico">✎</span>한국어 문법</button>
 <button class="nav" data-page="quiz"><span class="ico">◎</span>TOPIK 연습</button>
 <div class="goal"><strong>🌱 오늘의 목표</strong><p>매일 조금씩 한국어와 가까워져요.</p><div class="progress"><div id="sideProgress"></div></div><span id="sideCount">0</span> / 5개 학습 활동</div>
</aside>

<main>
<section class="page active" id="page-home">
 <div class="hero">
  <div class="eyebrow">YOUR KOREAN JOURNEY</div>
  <h1>안녕! 한국어,<br>오늘도 한 걸음. ✳</h1>
  <p>단어부터 문법, TOPIK까지.<br>나만의 속도로 한국어를 완성해 봐요.</p>
  <button class="primary" onclick="go('translate')">학습 시작하기 ↗</button>
 </div>
 <div class="section-head"><div><h2>나의 학습 현황</h2><p>작은 성취가 실력이 돼요.</p></div></div>
 <div class="stats">
  <div class="stat">📚<strong id="statWords">0</strong><small>번역한 단어</small></div>
  <div class="stat">🎯<strong id="statQuiz">0%</strong><small>퀴즈 정답률</small></div>
  <div class="stat">🌿<strong id="statLessons">0</strong><small>학습 활동</small></div>
 </div>
 <div class="section-head"><div><h2>무엇을 배워 볼까요?</h2><p>원하는 코스를 선택하세요.</p></div></div>
 <div class="cards">
  <article class="card"><div class="card-icon">🌐</div><h3>번역 & 발음</h3><p>다른 언어의 단어를 한국어로 알아보고 발음을 들어요.</p><button onclick="go('translate')">학습 시작 →</button></article>
  <article class="card"><div class="card-icon">🔤</div><h3>한글 마스터</h3><p>자음과 모음부터 읽고 쓰는 기초를 익혀요.</p><button onclick="go('hangul')">학습 시작 →</button></article>
  <article class="card"><div class="card-icon">📝</div><h3>문법 한 스푼</h3><p>자주 쓰는 문법을 예문과 함께 배워요.</p><button onclick="go('grammar')">학습 시작 →</button></article>
  <article class="card"><div class="card-icon">🏆</div><h3>TOPIK 챌린지</h3><p>한국어능력시험 유형의 문제를 풀어 봐요.</p><button onclick="go('quiz')">도전하기 →</button></article>
  <article class="card"><div class="card-icon">💬</div><h3>오늘의 표현</h3><p>안녕하세요, 감사합니다. 일상 표현을 연습해요.</p><button onclick="speak('안녕하세요. 감사합니다. 만나서 반갑습니다.')">🔊 발음 듣기</button></article>
  <article class="card"><div class="card-icon">✨</div><h3>꾸준한 학습</h3><p>오늘 배운 내용을 다시 확인하고 실력을 쌓아요.</p><button onclick="go('quiz')">복습하기 →</button></article>
 </div>
</section>

<section class="page" id="page-translate">
 <div class="eyebrow" style="color:#719b43;margin-top:12px">LANGUAGE BRIDGE</div>
 <h1 class="page-title">번역 & 발음</h1>
 <p class="subtitle">모르는 단어나 문장을 입력해 보세요.<br>한국어 뜻을 알아보고 소리로 들어 보세요.</p>
 <div class="panel">
  <label class="field-label" for="sourceLang">입력 언어</label>
  <select class="field" id="sourceLang">
   <option value="en">영어 · English</option>
   <option value="ja">일본어 · 日本語</option>
   <option value="zh-CN">중국어 · 中文</option>
   <option value="es">스페인어 · Español</option>
   <option value="fr">프랑스어 · Français</option>
   <option value="de">독일어 · Deutsch</option>
   <option value="vi">베트남어 · Tiếng Việt</option>
   <option value="th">태국어 · ไทย</option>
  </select>
  <label class="field-label" for="sourceText">번역할 단어 또는 문장</label>
  <textarea class="field" id="sourceText" placeholder="예: Hello, nice to meet you!"></textarea>
  <div class="row">
   <button class="primary" id="translateBtn" onclick="translateText()">한국어로 번역하기 ↗</button>
   <button class="secondary" onclick="document.getElementById('sourceText').value='';document.getElementById('translationResult').hidden=true">초기화</button>
  </div>
  <p class="hint">인터넷 연결이 필요해요. 무료 번역 서비스의 사용량 제한에 따라 결과가 제공되지 않을 수 있어요.</p>
  <div id="translationResult" class="result" hidden aria-live="polite">
   <h3>KOREAN TRANSLATION 🇰🇷</h3>
   <div class="big-result" id="translatedText"></div>
   <div class="result-meta" id="translationMeta"></div>
   <div class="row"><button class="primary" onclick="speak(document.getElementById('translatedText').textContent)">🔊 발음 듣기</button><button class="secondary" onclick="copyTranslation()">복사하기</button></div>
  </div>
 </div>
 <div class="section-head"><div><h2>자주 쓰는 한국어</h2><p>버튼을 눌러 발음을 들어 보세요.</p></div></div>
 <div class="cards">
  <article class="card"><div class="card-icon">👋</div><h3>안녕하세요</h3><p>Hello · 인사 표현</p><button onclick="speak('안녕하세요')">🔊 듣기</button></article>
  <article class="card"><div class="card-icon">🙏</div><h3>감사합니다</h3><p>Thank you · 감사 표현</p><button onclick="speak('감사합니다')">🔊 듣기</button></article>
  <article class="card"><div class="card-icon">💛</div><h3>사랑</h3><p>Love · 아끼는 마음</p><button onclick="speak('사랑')">🔊 듣기</button></article>
 </div>
</section>

<section class="page" id="page-hangul">
 <div class="eyebrow" style="color:#719b43;margin-top:12px">HANGUL STUDIO</div>
 <h1 class="page-title">한글 배우기</h1>
 <p class="subtitle">자음과 모음을 결합해 음절을 만들어요.<br>글자를 선택하면 발음을 들을 수 있어요.</p>
 <div class="panel">
  <h2 style="font-size:17px">기본 자음</h2><div class="hangul-grid" id="consonants"></div>
  <h2 style="font-size:17px;margin-top:27px">기본 모음</h2><div class="hangul-grid" id="vowels"></div>
  <h2 style="font-size:17px;margin-top:27px">음절 만들기</h2>
  <p class="subtitle">자음과 모음을 선택해 보세요.</p>
  <div class="row">
   <select class="field" style="flex:1" id="makeConsonant"></select>
   <select class="field" style="flex:1" id="makeVowel"></select>
   <button class="primary" onclick="makeSyllable()">만들기</button>
  </div>
  <div id="syllableResult" class="result" hidden>
   <div class="big-result" id="syllableLetter" style="font-size:45px"></div>
   <div id="syllableInfo" class="result-meta"></div>
   <button class="secondary" style="margin-top:12px" onclick="speak(document.getElementById('syllableLetter').textContent)">🔊 발음 듣기</button>
  </div>
  <div class="note">학습 팁: ㄱ + ㅏ = 가. 자음과 모음의 조합을 익히고 소리 내어 읽어 보세요.</div>
 </div>
</section>

<section class="page" id="page-grammar">
 <div class="eyebrow" style="color:#719b43;margin-top:12px">GRAMMAR LAB</div>
 <h1 class="page-title">한국어 문법</h1>
 <p class="subtitle">문법 규칙을 이해하고 예문으로 익혀요.</p>
 <div class="tabs" id="grammarTabs">
  <button class="tab active" data-level="전체">전체</button>
  <button class="tab" data-level="입문">입문</button>
  <button class="tab" data-level="초급">초급</button>
 </div>
 <div id="grammarList"></div>
</section>

<section class="page" id="page-quiz">
 <div class="eyebrow" style="color:#719b43;margin-top:12px">TOPIK PRACTICE</div>
 <h1 class="page-title">TOPIK 챌린지</h1>
 <p class="subtitle">어휘와 문법, 읽기 문제를 풀고 해설을 확인하세요.</p>
 <div class="panel" id="quizPanel">
  <div class="quiz-top"><span id="quizCategory">초급 · 어휘</span><span id="quizCount">1 / 10</span></div>
  <div class="progress"><div id="quizProgress"></div></div>
  <div class="question" id="quizQuestion"></div>
  <div class="choices" id="quizChoices"></div>
  <div id="quizFeedback" aria-live="polite"></div>
  <div class="row" style="justify-content:space-between">
   <span id="quizScore" class="hint">이번 도전 0점</span>
   <button class="primary" id="quizNext" onclick="nextQuestion()" disabled>다음 문제 →</button>
  </div>
 </div>
 <div class="note">이 문제는 학습용으로 자체 제작한 TOPIK 유형 연습 문항이며, 공식 기출문제가 아닙니다.</div>
</section>
<footer>DUO RINGGO · Learn Korean, connect the world.</footer>
</main>
</div>

<nav class="mobile-nav">
 <button class="nav active" data-page="home"><span class="ico">⌂</span>홈</button>
 <button class="nav" data-page="translate"><span class="ico">文</span>번역</button>
 <button class="nav" data-page="hangul"><span class="ico">가</span>한글</button>
 <button class="nav" data-page="grammar"><span class="ico">✎</span>문법</button>
 <button class="nav" data-page="quiz"><span class="ico">◎</span>TOPIK</button>
</nav>
</div>

<script>
const $=id=>document.getElementById(id);
const STORAGE='duoringgo-data-v2';
const defaults={words:0,correct:0,answered:0,lessons:[],streak:0,lastDay:''};
let stats={...defaults};
try{stats={...defaults,...JSON.parse(localStorage.getItem(STORAGE)||'{}')}}catch(e){}

function save(){
 try{localStorage.setItem(STORAGE,JSON.stringify(stats))}catch(e){}
 updateStats();
}
function markLesson(name){
 if(!stats.lessons.includes(name))stats.lessons.push(name);
 const today=new Date().toLocaleDateString('en-CA');
 if(stats.lastDay!==today){
  const yesterday=new Date(Date.now()-86400000).toLocaleDateString('en-CA');
  stats.streak=stats.lastDay===yesterday?stats.streak+1:1;
  stats.lastDay=today;
 }
 save();
}
function updateStats(){
 $('statWords').textContent=stats.words;
 $('statQuiz').textContent=stats.answered?Math.round(stats.correct/stats.answered*100)+'%':'0%';
 $('statLessons').textContent=stats.lessons.length;
 $('streak').textContent=stats.streak;
 $('sideCount').textContent=Math.min(stats.lessons.length,5);
 $('sideProgress').style.width=Math.min(stats.lessons.length/5*100,100)+'%';
}
function go(page){
 document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id==='page-'+page));
 document.querySelectorAll('.nav[data-page]').forEach(b=>b.classList.toggle('active',b.dataset.page===page));
 window.scrollTo({top:0,behavior:'smooth'});
 if(page==='hangul')markLesson('hangul');
 if(page==='grammar')markLesson('grammar');
 if(page==='quiz')renderQuiz();
}
document.querySelectorAll('.nav[data-page]').forEach(b=>b.addEventListener('click',()=>go(b.dataset.page)));

function speak(text){
 if(!('speechSynthesis' in window)){alert('이 브라우저는 음성 재생을 지원하지 않아요.');return}
 speechSynthesis.cancel();
 const utterance=new SpeechSynthesisUtterance(text);
 utterance.lang='ko-KR';utterance.rate=.85;
 const voice=speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().startsWith('ko'));
 if(voice)utterance.voice=voice;
 speechSynthesis.speak(utterance);
}

async function translateText(){
 const input=$('sourceText').value.trim();
 if(!input){alert('번역할 단어나 문장을 입력해 주세요.');return}
 const btn=$('translateBtn');
 btn.disabled=true;btn.textContent='번역 중…';
 $('translationResult').hidden=true;
 try{
  const lang=$('sourceLang').value;
  const url='https://api.mymemory.translated.net/get?q='+encodeURIComponent(input)+'&langpair='+encodeURIComponent(lang+'|ko');
  const response=await fetch(url);
  if(!response.ok)throw Error('Translation request failed');
  const data=await response.json();
  const translated=data.responseData&&data.responseData.translatedText;
  if(data.responseStatus!==200||!translated||/MYMEMORY WARNING|PLEASE SELECT/i.test(translated))throw Error('No translation');
  $('translatedText').textContent=translated;
  $('translationMeta').textContent='입력: '+input;
  $('translationResult').hidden=false;
  stats.words++;
  markLesson('translate');
 }catch(e){
  alert('번역에 실패했어요. 인터넷 연결을 확인하고 다시 시도해 주세요. 무료 번역 서비스의 사용량 제한일 수도 있어요.');
 }finally{
  btn.disabled=false;btn.textContent='한국어로 번역하기 ↗';
 }
}
function copyTranslation(){
 const text=$('translatedText').textContent;
 if(navigator.clipboard&&window.isSecureContext){
  navigator.clipboard.writeText(text).then(()=>alert('복사했어요.')).catch(()=>prompt('아래 내용을 복사하세요.',text));
 }else prompt('아래 내용을 복사하세요.',text);
}

const cons=[
 ['ㄱ','g / k'],['ㄴ','n'],['ㄷ','d / t'],['ㄹ','r / l'],['ㅁ','m'],
 ['ㅂ','b / p'],['ㅅ','s'],['ㅇ','무음 / ng'],['ㅈ','j'],['ㅊ','ch'],
 ['ㅋ','k'],['ㅌ','t'],['ㅍ','p'],['ㅎ','h'],['ㄲ','kk'],
 ['ㄸ','tt'],['ㅃ','pp'],['ㅆ','ss'],['ㅉ','jj']
];
const vows=[
 ['ㅏ','a'],['ㅐ','ae'],['ㅑ','ya'],['ㅒ','yae'],['ㅓ','eo'],
 ['ㅔ','e'],['ㅕ','yeo'],['ㅖ','ye'],['ㅗ','o'],['ㅘ','wa'],
 ['ㅙ','wae'],['ㅚ','oe'],['ㅛ','yo'],['ㅜ','u'],['ㅝ','wo'],
 ['ㅞ','we'],['ㅟ','wi'],['ㅠ','yu'],['ㅡ','eu'],['ㅢ','ui'],['ㅣ','i']
];
function renderLetters(id,data){
 const grid=$(id);
 data.forEach(([letter,sound])=>{
  const item=document.createElement('div');item.className='letter';
  const strong=document.createElement('strong');strong.textContent=letter;
  const small=document.createElement('small');small.textContent=sound;
  const button=document.createElement('button');button.textContent='🔊 듣기';
  button.addEventListener('click',()=>speak(letter));
  item.append(strong,small,button);grid.append(item);
 });
}
renderLetters('consonants',cons);renderLetters('vowels',vows);
$('makeConsonant').innerHTML=cons.slice(0,14).map(x=>'<option value="'+x[0]+'">'+x[0]+'</option>').join('');
$('makeVowel').innerHTML=vows.map(x=>'<option value="'+x[0]+'">'+x[0]+'</option>').join('');

function makeSyllable(){
 const c=$('makeConsonant').value,v=$('makeVowel').value;
 const leads=['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'];
 const medias=['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'];
 const li=leads.indexOf(c),mi=medias.indexOf(v);
 if(li<0||mi<0){alert('지원하지 않는 조합이에요.');return}
 const syllable=String.fromCharCode(44032+li*588+mi*28);
 $('syllableLetter').textContent=syllable;
 $('syllableInfo').textContent=c+' + '+v+' = '+syllable+' · 발음을 듣고 따라 해 보세요.';
 $('syllableResult').hidden=false;
 markLesson('hangul');
}

const grammar=[
 {level:'입문',title:'은 / 는 — 주제 나타내기',desc:'문장에서 무엇에 대해 이야기하는지 나타내요. 받침이 있으면 은, 없으면 는을 사용해요.',ex:'저는 학생이에요. (I am a student.)\n오늘은 날씨가 좋아요. (The weather is nice today.)',sound:'저는 학생이에요.'},
 {level:'입문',title:'이 / 가 — 주어 나타내기',desc:'문장의 주어를 표시하는 조사예요. 받침이 있으면 이, 없으면 가를 사용해요.',ex:'책이 있어요. (There is a book.)\n친구가 와요. (My friend is coming.)',sound:'친구가 와요.'},
 {level:'입문',title:'이에요 / 예요 — 정중한 표현',desc:'명사 뒤에 붙여 정중하게 설명해요. 받침이 있으면 이에요, 없으면 예요를 써요.',ex:'저는 의사예요. (I am a doctor.)\n여기는 학교예요. (This is a school.)',sound:'저는 의사예요.'},
 {level:'초급',title:'을 / 를 — 목적어 나타내기',desc:'동작의 대상을 나타내요. 받침이 있으면 을, 없으면 를을 사용해요.',ex:'책을 읽어요. (I read a book.)\n커피를 마셔요. (I drink coffee.)',sound:'책을 읽어요.'},
 {level:'초급',title:'-아요 / -어요 — 현재형',desc:'동사와 형용사를 일상적인 정중한 말투로 활용해요.',ex:'가다 → 가요. (go)\n먹다 → 먹어요. (eat)',sound:'먹어요.'},
 {level:'초급',title:'-고 싶어요 — 희망 표현',desc:'하고 싶은 행동을 표현할 때 동사 어간 뒤에 붙여요.',ex:'한국어를 배우고 싶어요. (I want to learn Korean.)\n한국에 가고 싶어요. (I want to go to Korea.)',sound:'한국어를 배우고 싶어요.'},
 {level:'초급',title:'-았어요 / -었어요 — 과거형',desc:'과거에 일어난 일을 표현해요.',ex:'어제 영화를 봤어요. (I watched a movie yesterday.)\n밥을 먹었어요. (I ate.)',sound:'어제 영화를 봤어요.'},
 {level:'초급',title:'-(으)세요 — 정중한 요청',desc:'정중하게 부탁하거나 권유할 때 사용해요.',ex:'여기 앉으세요. (Please sit here.)\n천천히 말하세요. (Please speak slowly.)',sound:'여기 앉으세요.'}
];
function renderGrammar(level='전체'){
 const list=$('grammarList');list.replaceChildren();
 grammar.filter(g=>level==='전체'||g.level===level).forEach(g=>{
  const article=document.createElement('article');article.className='grammar-item';
  const pill=document.createElement('span');pill.className='pill';pill.textContent=g.level;
  const play=document.createElement('button');play.className='secondary';play.textContent='🔊 예문 듣기';play.style.float='right';
  play.addEventListener('click',()=>speak(g.sound));
  const title=document.createElement('h3');title.textContent=g.title;
  const desc=document.createElement('p');desc.textContent=g.desc;
  const example=document.createElement('div');example.className='example';example.textContent=g.ex;
  article.append(pill,play,title,desc,example);list.append(article);
 });
}
document.querySelectorAll('#grammarTabs button').forEach(b=>b.addEventListener('click',()=>{
 document.querySelectorAll('#grammarTabs button').forEach(t=>t.classList.remove('active'));
 b.classList.add('active');renderGrammar(b.dataset.level);
}));
renderGrammar();

const questions=[
 {cat:'어휘',q:'빈칸에 들어갈 가장 알맞은 말을 고르세요.\n저는 아침에 밥을 ___.',choices:['마셔요','먹어요','읽어요','만나요'],a:1,why:'밥은 보통 먹는다고 표현해요. "밥을 먹어요"는 eat a meal이라는 뜻이에요.'},
 {cat:'문법',q:'빈칸에 알맞은 조사를 고르세요.\n저___ 학생이에요.',choices:['를','에서','는','으로'],a:2,why:'문장의 주제를 나타낼 때 "저는"이라고 해요.'},
 {cat:'어휘',q:'"감사합니다"와 뜻이 가장 가까운 것은?',choices:['안녕히 가세요','죄송합니다','고맙습니다','괜찮습니다'],a:2,why:'감사합니다와 고맙습니다는 모두 감사의 뜻이에요.'},
 {cat:'문법',q:'빈칸에 알맞은 말을 고르세요.\n어제 영화를 ___.',choices:['봐요','봤어요','볼까요','보세요'],a:1,why:'어제는 과거를 나타내므로 "봤어요"가 알맞아요.'},
 {cat:'어휘',q:'"학교"는 무엇을 의미하나요?',choices:['Hospital','School','Library','Restaurant'],a:1,why:'학교는 공부하는 곳인 school을 뜻해요.'},
 {cat:'문법',q:'자연스러운 문장을 고르세요.',choices:['저는 사과를 먹어요.','저는 사과가 먹어요.','저는 사과에 먹어요.','저는 사과로 먹어요.'],a:0,why:'먹는 대상을 나타낼 때 목적격 조사 "를"을 사용해요.'},
 {cat:'어휘',q:'"도서관"에서 할 수 있는 일은?',choices:['책을 읽어요','수영을 해요','요리를 해요','축구를 해요'],a:0,why:'도서관은 책을 읽거나 빌릴 수 있는 곳이에요.'},
 {cat:'문법',q:'빈칸에 알맞은 표현을 고르세요.\n한국 음식을 먹___ 싶어요.',choices:['는','고','을','에'],a:1,why:'동사 어간 뒤에 "-고 싶어요"를 붙여 희망을 표현해요.'},
 {cat:'읽기',q:'글을 읽고 답하세요.\n민수 씨는 일요일에 공원에 갑니다. 친구와 축구를 합니다.\n민수 씨는 누구와 축구를 합니까?',choices:['선생님','가족','친구','혼자'],a:2,why:'글에서 민수 씨는 친구와 축구를 한다고 했어요.'},
 {cat:'읽기',q:'글을 읽고 답하세요.\n수진 씨는 아침 7시에 일어납니다. 8시에 아침을 먹습니다.\n수진 씨는 몇 시에 일어납니까?',choices:['6시','7시','8시','9시'],a:1,why:'첫 문장에서 아침 7시에 일어난다고 했어요.'}
];
let order=questions.map((_,i)=>i),qi=0,answeredCurrent=false,sessionCorrect=0;
function renderQuiz(){
 if(qi>=order.length){showQuizEnd();return}
 const q=questions[order[qi]];answeredCurrent=false;
 $('quizCategory').textContent='학습 · '+q.cat;
 $('quizCount').textContent=(qi+1)+' / '+order.length;
 $('quizProgress').style.width=((qi+1)/order.length*100)+'%';
 $('quizQuestion').textContent=q.q;
 $('quizChoices').replaceChildren();
 q.choices.forEach((choice,i)=>{
  const btn=document.createElement('button');btn.className='choice';
  btn.textContent=['①','②','③','④'][i]+'　'+choice;
  btn.addEventListener('click',()=>selectAnswer(i));
  $('quizChoices').append(btn);
 });
 $('quizFeedback').replaceChildren();
 $('quizNext').disabled=true;
 $('quizNext').textContent=qi===order.length-1?'결과 보기 →':'다음 문제 →';
 $('quizScore').textContent='이번 도전 '+sessionCorrect+'점';
}
function selectAnswer(i){
 if(answeredCurrent)return;
 answeredCurrent=true;
 const q=questions[order[qi]],correct=i===q.a;
 if(correct)sessionCorrect++;
 stats.answered++;if(correct)stats.correct++;
 markLesson('quiz');
 [...$('quizChoices').children].forEach((btn,j)=>{
  btn.disabled=true;
  if(j===q.a)btn.classList.add('correct');
  if(j===i&&!correct)btn.classList.add('wrong');
 });
 const feedback=document.createElement('div');
 feedback.className='feedback '+(correct?'good':'bad');
 const strong=document.createElement('strong');
 strong.textContent=correct?'정답이에요! 🎉':'아쉬워요. 다시 배워 봐요.';
 feedback.append(strong,document.createElement('br'),document.createTextNode(q.why));
 $('quizFeedback').replaceChildren(feedback);
 $('quizScore').textContent='이번 도전 '+sessionCorrect+'점';
 $('quizNext').disabled=false;
}
function nextQuestion(){
 if(!answeredCurrent)return;
 qi++;renderQuiz();
}
function showQuizEnd(){
 $('quizPanel').replaceChildren();
 const wrap=document.createElement('div');wrap.style.textAlign='center';wrap.style.padding='25px 5px';
 const icon=document.createElement('div');icon.style.fontSize='45px';icon.textContent='🏆';
 const title=document.createElement('h2');title.textContent='도전 완료!';
 const score=document.createElement('div');score.className='big-result';score.textContent=sessionCorrect+' / '+questions.length+'점';
 const percent=document.createElement('p');percent.textContent='정답률 '+Math.round(sessionCorrect/questions.length*100)+'%';
 const again=document.createElement('button');again.className='primary';again.textContent='다시 도전하기 ↻';again.addEventListener('click',restartQuiz);
 const home=document.createElement('button');home.className='secondary';home.style.marginLeft='8px';home.textContent='홈으로';home.addEventListener('click',()=>go('home'));
 wrap.append(icon,title,score,percent,again,home);$('quizPanel').append(wrap);
}
function restartQuiz(){
 order=questions.map((_,i)=>i).sort(()=>Math.random()-.5);
 qi=0;sessionCorrect=0;
 $('quizPanel').innerHTML='<div class="quiz-top"><span id="quizCategory"></span><span id="quizCount"></span></div><div class="progress"><div id="quizProgress"></div></div><div class="question" id="quizQuestion"></div><div class="choices" id="quizChoices"></div><div id="quizFeedback" aria-live="polite"></div><div class="row" style="justify-content:space-between"><span id="quizScore" class="hint"></span><button class="primary" id="quizNext" disabled>다음 문제 →</button></div>';
 $('quizNext').addEventListener('click',nextQuestion);
 renderQuiz();
}
updateStats();
</script>
</body>
</html>
