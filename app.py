# =========================================================
# 나의 MBTI 검사 - 메뉴(시작 파일)
# 실행: streamlit run app.py
# 왼쪽 사이드바에 "검사하기 / 통계 보기" 메뉴를 만들고, 고른 페이지를 보여 줍니다
#   pages/test_page.py  : 검사하기 (시작 → 질문 → 결과)
#   pages/stats_page.py : 통계 보기 (유형별 인원 막대 그래프)
# =========================================================

import streamlit as st  # 웹앱을 만드는 도구

st.set_page_config(page_title="나의 MBTI 검사", page_icon="🌈", layout="centered")  # 탭 이름, 아이콘, 가운데 정렬

test_page = st.Page("pages/test_page.py", title="검사하기", icon="📝", default=True)  # 처음 열리는 페이지
stats_page = st.Page("pages/stats_page.py", title="통계 보기", icon="📊", url_path="stats")  # 주소 끝이 /stats인 페이지

st.navigation([test_page, stats_page]).run()  # 사이드바 메뉴를 만들고, 고른 페이지를 실행합니다
