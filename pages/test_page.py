# =========================================================
# 나의 MBTI 검사 - 검사 페이지
# 실행: streamlit run app.py (app.py 메뉴에서 이 페이지가 열립니다)
# 흐름: 시작 화면 → 질문 화면(12개) → 결과 화면
# =========================================================

import json  # JSON 파일을 읽는 도구
from pathlib import Path  # 파일 경로를 다루는 도구

import streamlit as st  # 웹앱을 만드는 도구

from sheet_reader import load_results  # 읽기 담당: 저장 후 통계가 바로 바뀌도록 저장해 둔 결과를 지울 때 씁니다
from sheet_saver import save_result  # 기록원: 검사 결과를 구글 시트에 적는 함수


# ========== 1. 데이터 불러오기 ==========

FOLDER = Path(__file__).parent.parent  # pages 폴더의 한 칸 위 = questions.json이 있는 mbti_test 폴더


@st.cache_data  # 파일을 한 번만 읽고, 다음부터는 저장해 둔 값을 씁니다
def load_json(file_name):
    with open(FOLDER / file_name, encoding="utf-8") as f:  # 한글이 깨지지 않게 utf-8로 엽니다
        return json.load(f)  # 파일 내용을 파이썬 딕셔너리로 바꿔 돌려줍니다


question_data = load_json("questions.json")  # 질문 파일 전체
QUESTIONS = question_data["questions"]       # 질문 12개 목록
APP_NAME = question_data["app_name"]         # 앱 이름
TYPES = load_json("types.json")              # 16유형의 이름과 설명

PAIRS = ["EI", "SN", "TF", "JP"]  # 비교할 지표 4개 (이 순서대로 글자를 붙입니다)


# ========== 2. 페이지 기본 설정은 app.py(메뉴)에서 합니다 ==========


# ========== 3. 꾸미기 (파스텔 색과 모바일 크기) ==========
# st.markdown에 <style>을 넣으면 CSS로 화면을 꾸밀 수 있습니다

st.markdown(
    """
    <style>
    /* 귀여운 한글 글꼴(Jua)을 불러옵니다 */
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    /* 색 이름 정하기 */
    :root {
      --main: #f1f5b6;        /* 메인: 연노랑 배경 */
      --sub: #e5b8b7;         /* 보조: 연분홍 버튼 */
      --point: #92ccdc;       /* 포인트: 하늘색 */
      --point-text: #337589;  /* 포인트 글자: 진한 하늘색 */
      --text: #404040;        /* 글자: 진회색 */
    }

    /* 페이지 배경과 글꼴 */
    .stApp {
      background: var(--main);
      font-family: "Jua", "Malgun Gothic", sans-serif;
      color: var(--text);
    }

    /* 맨 위 Streamlit 메뉴 줄을 투명하게 */
    header[data-testid="stHeader"] {
      background: transparent;
    }

    /* 가운데 내용 영역: 흰색 둥근 카드처럼 보이게 */
    .block-container {
      max-width: 540px;
      margin: 72px auto 40px;  /* 위쪽은 메뉴 줄(60px)에 가리지 않게 띄웁니다 */
      padding: 40px 28px;
      background: #ffffff;
      border-radius: 28px;
      box-shadow: 0 10px 28px rgba(64, 64, 64, 0.12);
    }

    /* 모든 글자에 같은 글꼴과 색 */
    /* (아이콘 글자 stIconMaterial은 빼야 사이드바 화살표 아이콘이 글자로 바뀌지 않습니다) */
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span:not([data-testid="stIconMaterial"]), .stApp button {
      font-family: "Jua", "Malgun Gothic", sans-serif !important;
      color: var(--text);
    }

    /* 가운데 정렬 글자 */
    .center { text-align: center; }

    /* 제목 */
    .title { font-size: 40px !important; margin: 0 0 12px; }

    /* 한줄소개 */
    .intro { font-size: 19px !important; line-height: 1.5; margin: 0 0 16px; }

    /* 12문항 · 약 2분 안내 */
    .info {
      display: inline-block;
      padding: 6px 16px;
      border-radius: 999px;
      background: var(--main);
      font-size: 15px !important;
    }

    /* 재미로 보는 검사예요 */
    .notice { font-size: 14px !important; opacity: 0.6; margin-top: 8px; }

    /* 진행 숫자 (3 / 12) */
    .progress-text { text-align: right; font-size: 16px !important; margin: 0; }

    /* 진행 막대: 회색 바탕 안에서 하늘색 막대가 늘어납니다 */
    .progress { height: 10px; border-radius: 999px; background: #eeeeee; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 999px; background: var(--point); }

    /* 질문 번호 (Q3) */
    .q-number { font-size: 18px !important; color: var(--point-text) !important; margin: 18px 0 4px; }

    /* 질문 내용 */
    .q-text { font-size: 26px !important; line-height: 1.4; margin: 0 0 22px; word-break: keep-all; }

    /* 큰 버튼 (검사 시작, 다시 하기): 연분홍 알약 모양 */
    .st-key-start_btn button, .st-key-restart_btn button {
      min-height: 56px;
      border: none;
      border-radius: 999px;
      background: var(--sub);
    }
    .st-key-start_btn button p, .st-key-restart_btn button p { font-size: 21px !important; }

    /* 전체 통계 보기 버튼: 하늘색 테두리 알약 모양 */
    .st-key-stats_btn button {
      min-height: 56px;
      border: 2px solid var(--point);
      border-radius: 999px;
      background: #ffffff;
    }
    .st-key-stats_btn button p { font-size: 19px !important; }

    /* 선택지 버튼: 흰 바탕에 분홍 테두리 */
    .st-key-choice_0 button, .st-key-choice_1 button {
      min-height: 56px;
      padding: 14px 18px;
      border: 2px solid var(--sub);
      border-radius: 18px;
      background: #ffffff;
    }
    .st-key-choice_0 button p, .st-key-choice_1 button p {
      font-size: 18px !important;
      line-height: 1.4;
      word-break: keep-all;
    }

    /* 이전 버튼: 테두리 없는 글자 버튼 */
    .st-key-back_btn button {
      border: none;
      background: transparent;
      padding: 0 4px;
    }

    /* Streamlit 기본 효과(누른 뒤 남는 색)를 없애고 흰 바탕을 유지합니다 */
    .st-key-choice_0 button:focus, .st-key-choice_1 button:focus,
    .st-key-choice_0 button:active, .st-key-choice_1 button:active,
    .st-key-choice_0 button:hover, .st-key-choice_1 button:hover {
      background: #ffffff;
      border-color: var(--sub);
      color: var(--text);
    }

    /* 마우스가 있는 기기에서만 버튼에 올리면 색이 바뀝니다 (핸드폰에서 색이 남는 것 방지) */
    @media (hover: hover) {
      .st-key-choice_0 button:hover, .st-key-choice_1 button:hover { background: #fbeceb; border-color: var(--sub); }
      .st-key-start_btn button:hover, .st-key-restart_btn button:hover { filter: brightness(0.95); }
    }

    /* 결과: 당신의 유형은 */
    .result-label { font-size: 18px !important; margin: 0; }

    /* 결과: 4글자 유형 */
    .result-type { font-size: 72px !important; letter-spacing: 4px; color: var(--point-text) !important; margin: 0; line-height: 1.2; }

    /* 결과: 유형 이름과 설명 */
    .result-name { font-size: 26px !important; margin: 6px 0 4px; }
    .result-desc { font-size: 17px !important; opacity: 0.8; margin: 0 0 20px; }

    /* 결과: 점수 막대 상자 */
    .scores { padding: 16px 14px; border-radius: 18px; background: #fafafa; margin-bottom: 20px; }
    .score-row { display: grid; grid-template-columns: 18px 16px 1fr 16px 18px; gap: 8px; align-items: center; margin: 8px 0; font-size: 17px !important; }
    .bar { height: 12px; border-radius: 999px; background: var(--point); overflow: hidden; }
    .bar-fill { height: 100%; background: var(--sub); }

    /* 핸드폰(599px 이하): 여백과 글자를 줄입니다 */
    @media (max-width: 599px) {
      .block-container { width: calc(100% - 32px); margin: 64px auto 24px; padding: 32px 20px; }  /* 양옆 16px 여백 */
      .title { font-size: 32px !important; }
      .q-text { font-size: 22px !important; }
      .result-type { font-size: 56px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,  # HTML과 CSS를 그대로 쓰도록 허용합니다
)


# ========== 4. 상태 저장 (st.session_state) ==========
# Streamlit은 버튼을 누를 때마다 코드를 처음부터 다시 실행합니다
# 그래서 지금 화면, 질문 순서, 답안지를 session_state에 저장해 둡니다

if "screen" not in st.session_state:   # 처음 열었을 때만
    st.session_state.screen = "start"   # 시작 화면부터 보여 줍니다
    st.session_state.current = 0        # 질문 순서 (0이 첫 번째 질문)
    st.session_state.answers = []       # 답안지 (질문마다 고른 번호 0 또는 1)
    st.session_state.saved = False      # 이번 검사 결과를 시트에 저장했는지 (두 번 저장 막기)
    st.session_state.save_error = None  # 저장에 실패했을 때의 오류 내용


# ========== 5. 버튼을 누르면 할 일 ==========

def start_test():  # 검사 시작
    st.session_state.answers = [None] * len(QUESTIONS)  # 답안지를 빈칸 12개로 준비합니다
    st.session_state.current = 0                         # 첫 질문부터
    st.session_state.saved = False                       # 새 검사이니 아직 저장 전입니다
    st.session_state.save_error = None                   # 지난 저장 오류를 지웁니다
    st.session_state.screen = "question"                 # 질문 화면으로 이동


def choose(index):  # 선택지 고르기 (index: 첫 번째 0, 두 번째 1)
    st.session_state.answers[st.session_state.current] = index  # 답안지 지금 칸에 적습니다 (다시 고르면 바뀜)
    if st.session_state.current < len(QUESTIONS) - 1:  # 마지막 질문이 아니면
        st.session_state.current += 1                  # 다음 질문으로
    else:                                              # 마지막 질문이었으면
        st.session_state.screen = "result"             # 결과 화면으로


def go_back():  # 이전 질문으로
    if st.session_state.current > 0:   # 첫 질문이 아니면
        st.session_state.current -= 1  # 한 칸 앞으로


def restart():  # 다시 하기
    st.session_state.answers = []       # 답안지를 비웁니다
    st.session_state.current = 0        # 질문 순서를 처음으로
    st.session_state.screen = "start"   # 시작 화면으로


# ========== 5-1. 결과를 시트에 한 번만 저장 ==========

def save_once(mbti, scores):
    if st.session_state.saved:   # 이미 저장했으면
        return                   # 아무것도 하지 않습니다 (두 번 저장 막기)
    st.session_state.saved = True  # 저장을 시도했다고 먼저 적어 둡니다 (실패해도 다시 시도하지 않음)

    letters = []                                            # 질문마다 고른 알파벳을 모을 곳
    for question, answer in zip(QUESTIONS, st.session_state.answers):  # 질문과 고른 답을 짝지어 꺼냅니다
        chosen = question["choices"][answer]                # 고른 선택지
        letters.append(list(chosen["score"])[0])            # 그 선택지의 알파벳 (예: E)

    try:  # 기록원에게 저장을 맡겨 보고
        save_result(mbti, scores, letters)
        load_results.clear()  # 저장에 성공하면, 통계 페이지가 내 결과까지 새로 읽도록 저장해 둔 결과를 지웁니다
    except Exception as error:  # 실패하면 오류 내용만 적어 둡니다 (결과 화면은 그대로 보여 줌)
        st.session_state.save_error = type(error).__name__


# ========== 6. 점수 계산 ==========

def calculate(answers):
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}  # 점수판을 0점으로 준비

    for question, answer in zip(QUESTIONS, answers):  # 질문과 고른 답을 하나씩 짝지어 꺼냅니다
        chosen = question["choices"][answer]          # 고른 선택지
        for letter, point in chosen["score"].items(): # 점수 알파벳과 점수 (예: E, 1)
            scores[letter] += point                   # 그 알파벳에 점수를 더합니다

    mbti = ""                                         # 결과 유형을 담을 빈 글자
    for pair in PAIRS:                                # 지표를 하나씩 (예: "EI")
        first, second = pair[0], pair[1]              # 첫 글자 E, 두 번째 글자 I
        if scores[first] > scores[second]:            # 첫 글자 점수가 더 높으면
            mbti += first                             # 첫 글자를 붙이고
        else:                                         # 두 번째가 높거나 같으면
            mbti += second                            # 두 번째 글자를 붙입니다

    return mbti, scores  # 4글자 유형과 점수판을 돌려줍니다


# ========== 7. 화면 1: 시작 화면 ==========

def show_start():
    st.markdown(
        f"""
        <div class="center">
          <p class="title">{APP_NAME}</p>
          <p class="intro">{len(QUESTIONS)}개 질문으로 알아보는<br>나의 성격 유형</p>
          <p><span class="info">{len(QUESTIONS)}문항 · 약 2분</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )  # 제목, 한줄소개, 안내 문구
    st.button("검사 시작", key="start_btn", on_click=start_test, width="stretch")  # 누르면 start_test 실행
    st.markdown('<p class="center notice">재미로 보는 검사예요</p>', unsafe_allow_html=True)  # 작은 안내


# ========== 8. 화면 2: 질문 화면 ==========

def show_question():
    current = st.session_state.current  # 지금 질문 순서
    total = len(QUESTIONS)              # 전체 질문 수
    question = QUESTIONS[current]       # 지금 질문

    # 맨 위 줄: 왼쪽에 이전 버튼, 오른쪽에 진행 숫자를 가로로 나란히 놓습니다
    # (st.columns는 핸드폰에서 위아래로 쌓여서, 가로 고정 상자를 씁니다)
    top_row = st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center")
    with top_row:
        if current > 0:          # 첫 질문이 아닐 때만 이전 버튼을 보여 줍니다
            st.button("< 이전", key="back_btn", on_click=go_back)
        else:                    # 첫 질문에서는 빈 자리를 두어 진행 숫자가 오른쪽에 있게 합니다
            st.markdown(" ")
        st.markdown(f'<p class="progress-text">{current + 1} / {total}</p>', unsafe_allow_html=True)  # 진행 숫자

    percent = (current + 1) / total * 100  # 진행 막대 길이 (%)
    st.markdown(
        f'<div class="progress"><div class="progress-fill" style="width:{percent}%"></div></div>',
        unsafe_allow_html=True,
    )  # 하늘색 진행 막대

    st.markdown(
        f"""
        <div class="center">
          <p class="q-number">Q{question["id"]}</p>
          <p class="q-text">{question["text"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )  # 질문 번호와 질문 내용

    for i, choice in enumerate(question["choices"]):  # 선택지 2개를 하나씩 (i는 0, 1)
        st.button(
            choice["text"],         # 버튼 글자: 선택 문장
            key=f"choice_{i}",      # 버튼 이름표 (choice_0, choice_1)
            on_click=choose,        # 누르면 choose 실행
            args=(i,),              # choose에 고른 번호를 넘겨줍니다
            width="stretch",        # 버튼을 가로로 꽉 채웁니다
        )


# ========== 9. 화면 3: 결과 화면 ==========

def show_result():
    mbti, scores = calculate(st.session_state.answers)  # 점수 계산
    info = TYPES.get(mbti)                              # types.json에서 유형 찾기 (없으면 None)

    if info:                              # 찾았으면
        name = info["name"]               # 유형 이름
        desc = info["description"]        # 한 줄 설명
    else:                                 # 못 찾았으면
        name = "설명을 준비 중이에요"
        desc = ""

    rows = ""                                         # 점수 막대 4줄의 HTML을 모을 곳
    for pair in PAIRS:                                # 지표마다
        a, b = pair[0], pair[1]                       # 왼쪽 글자, 오른쪽 글자
        total = scores[a] + scores[b]                 # 두 점수의 합
        percent = scores[a] / total * 100 if total else 50  # 왼쪽 글자 비율 (합이 0이면 반반)
        rows += (
            f'<div class="score-row">'
            f'<span>{a}</span><span>{scores[a]}</span>'
            f'<div class="bar"><div class="bar-fill" style="width:{percent}%"></div></div>'
            f'<span>{scores[b]}</span><span>{b}</span>'
            f'</div>'
        )  # 한 줄: [글자] [점수] [막대] [점수] [글자]

    st.markdown(
        f"""
        <div class="center">
          <p class="result-label">당신의 유형은</p>
          <p class="result-type">{mbti}</p>
          <p class="result-name">{name}</p>
          <p class="result-desc">{desc}</p>
        </div>
        <div class="scores">{rows}</div>
        """,
        unsafe_allow_html=True,
    )  # 유형, 이름, 설명, 점수 막대

    st.session_state.my_type = mbti  # 내 유형을 적어 둡니다 (통계 페이지에서 "나와 같은 유형"을 찾을 때 씁니다)

    save_once(mbti, scores)  # 결과를 먼저 보여 준 뒤, 시트에 한 번만 저장합니다
    if st.session_state.save_error:  # 저장에 실패했으면 경고만 띄웁니다
        st.warning(f"결과를 기록하지 못했어요. 결과는 그대로 볼 수 있어요. ({st.session_state.save_error})")

    if st.button("전체 통계 보기", key="stats_btn", width="stretch"):  # 누르면
        st.switch_page("pages/stats_page.py")                           # 통계 페이지로 이동합니다
    st.button("다시 하기", key="restart_btn", on_click=restart, width="stretch")  # 누르면 restart 실행
    st.markdown('<p class="center notice">재미로 보는 검사예요</p>', unsafe_allow_html=True)  # 작은 안내


# ========== 10. 지금 화면에 맞는 함수 실행 ==========

if st.session_state.screen == "start":       # 시작 화면이면
    show_start()
elif st.session_state.screen == "question":  # 질문 화면이면
    show_question()
else:                                        # 결과 화면이면
    show_result()
