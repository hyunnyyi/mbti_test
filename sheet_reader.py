# =========================================================
# 읽기 담당: 구글 시트에 쌓인 검사 결과를 표(DataFrame)로 가져옵니다
# (쓰기 담당은 sheet_saver.py, 시트 연결 방법은 둘이 같습니다)
#
# 열쇠 보관함(.streamlit/secrets.toml)에서 읽는 이름:
#   [stats] sheet_url     : 구글 시트 주소
#   [gcp_service_account] : 구글 서비스 계정 키
# =========================================================

import pandas as pd  # 표(데이터)를 다루는 도구
import streamlit as st  # 저장해 두기(cache) 기능을 쓰는 도구

from sheet_saver import get_sheet  # 시트 연결은 기록원(sheet_saver.py)의 함수를 같이 씁니다

TYPE_PATTERN = r"^[EI][SN][TF][JP]$"  # 올바른 MBTI 4글자 모양 (예: INTP) - 연결 테스트 줄 같은 것은 빼기 위해 씁니다


@st.cache_data(ttl=60, show_spinner="통계를 불러오는 중이에요...")  # 읽은 결과를 60초 동안 저장해 두고 다시 씁니다 (시트를 너무 자주 읽지 않게)
def load_results():
    """시트의 검사 결과를 표로 돌려줍니다. 제목 줄(시간, 유형, E, ...)이 표의 칸 이름이 됩니다."""
    records = get_sheet().get_all_records()  # 시트의 모든 줄을 [{시간: ..., 유형: ...}, ...] 모양으로 읽습니다
    df = pd.DataFrame(records)               # 읽은 줄들을 표로 바꿉니다

    if df.empty or "유형" not in df.columns:   # 결과가 하나도 없으면
        return pd.DataFrame(columns=["시간", "유형"])  # 빈 표를 돌려줍니다

    df["유형"] = df["유형"].astype(str).str.strip()     # 유형 칸을 글자로 바꾸고 앞뒤 빈칸을 지웁니다
    return df[df["유형"].str.match(TYPE_PATTERN)]       # 올바른 4글자 유형이 적힌 줄만 남깁니다
