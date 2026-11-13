# =========================================================
# 나의 MBTI 검사 - 통계 페이지
# 구글 시트에 쌓인 검사 결과로 유형별 인원 막대 그래프를 보여 주고,
# 방금 검사한 사람에게는 "나와 같은 유형이 몇 %인지"도 알려 줍니다
# =========================================================

import altair as alt  # 웹에서 보는 그래프를 그리는 도구 (브라우저 글꼴을 써서 한글이 깨지지 않습니다)
import pandas as pd  # 표(데이터)를 다루는 도구
import streamlit as st  # 웹앱을 만드는 도구

from sheet_reader import load_results  # 읽기 담당: 시트의 검사 결과를 표로 가져오는 함수


# ========== 1. 꾸미기 (검사 페이지와 같은 파스텔 색) ==========

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    :root { --main: #f1f5b6; --sub: #e5b8b7; --point: #92ccdc; --point-text: #337589; --text: #404040; }

    /* 페이지 배경과 글꼴 */
    .stApp { background: var(--main); color: var(--text); }
    /* (아이콘 글자 stIconMaterial은 빼야 사이드바 화살표 아이콘이 글자로 바뀌지 않습니다) */
    .stApp p, .stApp h1, .stApp span:not([data-testid="stIconMaterial"]), .stApp button, .stApp label, .stApp div[data-testid="stMetricValue"] {
      font-family: "Jua", "Malgun Gothic", sans-serif !important; color: var(--text);
    }
    header[data-testid="stHeader"] { background: transparent; }

    /* 가운데 흰색 카드 */
    .block-container {
      max-width: 540px; margin: 72px auto 40px; padding: 40px 28px;
      background: #ffffff; border-radius: 28px; box-shadow: 0 10px 28px rgba(64, 64, 64, 0.12);
    }

    .title { font-size: 34px !important; text-align: center; margin: 0 0 4px; }
    .subtitle { font-size: 15px !important; text-align: center; opacity: 0.7; margin: 0 0 20px; }

    /* 나와 같은 유형 상자 */
    .mine { padding: 16px 18px; border-radius: 18px; background: #eef7fa; margin: 8px 0 16px; text-align: center; }
    .mine p { margin: 0; font-size: 18px !important; line-height: 1.5; }
    .mine b { color: var(--point-text) !important; }

    /* 버튼: 다시 검사하기는 분홍 알약, 새로고침은 글자 버튼 */
    .st-key-retest_btn button { min-height: 52px; border: none; border-radius: 999px; background: var(--sub); }
    .st-key-retest_btn button p { font-size: 19px !important; }
    .st-key-refresh_btn button { border: none; background: transparent; }

    /* 핸드폰(599px 이하) */
    @media (max-width: 599px) {
      .block-container { width: calc(100% - 32px); margin: 64px auto 24px; padding: 32px 20px; }
      .title { font-size: 28px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,  # HTML과 CSS를 그대로 쓰도록 허용합니다
)

st.markdown('<p class="title">MBTI 검사 통계</p>', unsafe_allow_html=True)  # 페이지 제목
st.markdown('<p class="subtitle">지금까지 검사한 사람들의 유형이에요</p>', unsafe_allow_html=True)  # 부제목


# ========== 2. 시트에서 결과 읽기 ==========

try:  # 시트 읽기를 해 보고
    df = load_results()
except Exception as error:  # 실패하면 경고를 보여 주고 여기서 멈춥니다
    st.warning(f"통계를 불러오지 못했어요. 잠시 후 다시 시도해 주세요. ({type(error).__name__})")
    st.stop()

if df.empty:  # 결과가 하나도 없으면 안내만 보여 주고 멈춥니다
    st.info("아직 검사 결과가 없어요. 첫 번째로 검사해 보세요!")
    st.stop()


# ========== 3. 숫자 계산 ==========

counts = df["유형"].value_counts()  # 유형별 인원 (많은 순서대로 정렬됩니다)
total = int(counts.sum())           # 총 참여 인원
top_type = counts.index[0]          # 가장 많은 유형
my_type = st.session_state.get("my_type")  # 검사 페이지에서 적어 둔 내 유형 (검사 전이면 None)

left, right = st.columns(2)                                         # 숫자 카드 2개를 나란히
left.metric("총 참여 인원", f"{total}명")                             # 왼쪽: 총 참여 인원
right.metric("가장 많은 유형", f"{top_type} ({counts.iloc[0]}명)")    # 오른쪽: 가장 많은 유형


# ========== 4. 나와 같은 유형은 몇 %? ==========

if my_type:                                       # 방금 검사를 했다면
    same = int(counts.get(my_type, 0))            # 나와 같은 유형의 인원
    percent = same / total * 100                  # 전체 중 몇 %인지
    st.markdown(
        f'<div class="mine"><p>전체 {total}명 중 나와 같은 <b>{my_type}</b>는<br>'
        f'<b>{same}명 ({percent:.1f}%)</b>이에요</p></div>',
        unsafe_allow_html=True,
    )
else:                                             # 아직 검사 전이라면
    st.caption("검사를 마치면 나와 같은 유형이 몇 %인지 볼 수 있어요.")


# ========== 5. 유형별 인원 막대 그래프 ==========
# 핸드폰에서도 유형 이름이 겹치지 않게 가로 막대로 그립니다 (위에서부터 많은 순서)

chart_data = pd.DataFrame({
    "유형": counts.index,                                                     # 유형 이름
    "인원": counts.values,                                                    # 인원 수
    "구분": ["내 유형" if t == my_type else "다른 유형" for t in counts.index],  # 내 유형만 진하게 칠하기 위한 칸
})

chart = (
    alt.Chart(chart_data)
    .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)        # 막대 끝을 살짝 둥글게
    .encode(
        y=alt.Y("유형:N", sort=list(counts.index), title=None,
                axis=alt.Axis(labelFontSize=13, labelPadding=6)),        # 세로: 유형 (많은 순서), 글자 크게
        x=alt.X("인원:Q", title="인원수",
                axis=alt.Axis(tickMinStep=1, format="d", labelFontSize=12, titleFontSize=13)),  # 가로: 인원수 (정수 눈금)
        color=alt.Color("구분:N",
                        scale=alt.Scale(domain=["내 유형", "다른 유형"], range=["#337589", "#92ccdc"]),
                        legend=None),                                   # 내 유형은 진한 하늘색, 나머지는 하늘색
        tooltip=[alt.Tooltip("유형:N"), alt.Tooltip("인원:Q", title="인원(명)")],  # 막대에 올리면 숫자가 보입니다
    )
    .properties(
        height=alt.Step(30),        # 막대 한 줄의 높이 (유형이 많아지면 그래프도 자동으로 길어집니다)
        title="유형별 인원",          # 그래프 제목
        background="#ffffff",       # 그래프 바탕을 카드와 같은 흰색으로
    )
    .configure_view(strokeWidth=0)  # 그래프 바깥 테두리 선을 없앱니다
)

st.altair_chart(chart, width="stretch")  # 그래프를 카드 너비에 맞춰 보여 줍니다
if my_type in counts.index:  # 내 유형이 그래프에 있을 때만 안내합니다
    st.caption("진한 막대가 내 유형이에요.")


# ========== 6. 버튼 ==========

if st.button("다시 검사하기", key="retest_btn", width="stretch"):  # 누르면
    st.switch_page("pages/test_page.py")                            # 검사 페이지로 이동합니다

if st.button("↻ 최신 결과로 새로고침", key="refresh_btn"):  # 누르면
    load_results.clear()                                    # 저장해 둔 결과를 지우고
    st.rerun()                                              # 페이지를 다시 그려서 시트를 새로 읽습니다
st.caption("새 결과는 1분 안에 자동으로 반영돼요.")
