# =========================================================
# 기록원: MBTI 검사 결과를 구글 시트에 한 줄 적는 일만 합니다
# (화면을 보여 주고 순서를 정하는 감독은 app.py입니다)
#
# 시트 1번째 줄 제목 순서: 시간, 유형, E, I, S, N, T, F, J, P, 답변
# 열쇠 보관함(.streamlit/secrets.toml)에서 읽는 이름:
#   [stats] sheet_url     : 구글 시트 주소
#   [gcp_service_account] : 구글 서비스 계정 키
# =========================================================

from datetime import datetime, timedelta, timezone  # 날짜와 시간을 다루는 도구

import gspread  # 구글 시트를 다루는 도구
import streamlit as st  # 열쇠 보관함(st.secrets)을 읽는 도구

KST = timezone(timedelta(hours=9))  # 한국 시간 (배포 서버는 다른 나라 시간이라 직접 정해 줍니다)
LETTERS = ["E", "I", "S", "N", "T", "F", "J", "P"]  # 시트 제목 줄의 점수 순서


@st.cache_resource  # 시트 연결은 한 번만 하고, 다음부터는 저장해 둔 연결을 씁니다
def get_sheet():
    key = dict(st.secrets["gcp_service_account"])                        # 열쇠 보관함에서 키를 꺼냅니다
    client = gspread.service_account_from_dict(key)                      # 키로 구글에 로그인합니다
    spreadsheet = client.open_by_url(st.secrets["stats"]["sheet_url"])  # [stats] 묶음의 주소로 시트를 엽니다
    return spreadsheet.sheet1                                            # 첫 번째 시트(탭)를 돌려줍니다


def save_result(mbti, scores, answer_letters):
    """검사 결과 한 줄을 시트 맨 아래에 추가합니다. 실패하면 오류를 그대로 감독(app.py)에게 넘깁니다."""
    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")  # 지금 한국 시간 (예: 2026-11-12 21:30:00)
    row = [now, mbti]                                       # 시간, 유형
    for letter in LETTERS:                                  # E부터 P까지 차례대로
        row.append(scores[letter])                          # 점수를 붙입니다
    row.append(",".join(answer_letters))                    # 답변: 질문마다 고른 알파벳 (예: E,I,I,N,...)
    get_sheet().append_row(row)                             # 시트 맨 아래에 한 줄을 추가합니다
