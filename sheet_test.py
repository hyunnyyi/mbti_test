# =========================================================
# 구글 시트 저장 테스트 (아주 작은 Streamlit 앱)
# 실행: streamlit run sheet_test.py
# 필요한 비밀값 (.streamlit/secrets.toml 또는 Streamlit 배포 화면의 Secrets):
#   [stats] sheet_url     : 구글 시트 주소
#   [gcp_service_account] : 구글 서비스 계정 키
# =========================================================

from datetime import datetime, timedelta, timezone  # 날짜와 시간을 다루는 도구

import gspread  # 구글 시트를 다루는 도구
import streamlit as st  # 웹앱을 만드는 도구
from streamlit.errors import StreamlitSecretNotFoundError  # 비밀 설정 파일이 없을 때 나는 오류

KST = timezone(timedelta(hours=9))  # 한국 시간 (배포 서버는 다른 나라 시간이라 직접 정해 줍니다)

st.title("구글 시트 저장 테스트")  # 페이지 제목


@st.cache_resource  # 시트 연결은 한 번만 하고, 다음부터는 저장해 둔 연결을 씁니다
def get_sheet():
    key = dict(st.secrets["gcp_service_account"])          # 비밀값에서 서비스 계정 키를 꺼냅니다
    client = gspread.service_account_from_dict(key)        # 키로 구글에 로그인합니다
    spreadsheet = client.open_by_url(st.secrets["stats"]["sheet_url"])  # [stats] 묶음의 주소로 시트 파일을 엽니다
    return spreadsheet.sheet1                              # 첫 번째 시트(탭)를 돌려줍니다


text = st.text_input("저장할 내용")  # 사용자에게 저장할 글을 입력받습니다

if st.button("시트에 저장"):  # 버튼을 누르면
    if text.strip() == "":                          # 아무것도 입력하지 않았으면
        st.warning("저장할 내용을 입력해 주세요.")    # 안내만 보여 줍니다
    else:
        try:  # 아래 일을 해 보고, 실패하면 except로 갑니다
            sheet = get_sheet()                                   # 시트에 연결합니다
            now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S") # 지금 한국 시간 (예: 2026-11-12 21:30:00)
            sheet.append_row([now, text])                         # 시트 맨 아래에 [시간, 내용] 한 줄을 추가합니다
            st.success(f"저장했어요: {now} | {text}")              # 성공 메시지
        except (KeyError, StreamlitSecretNotFoundError):  # 비밀 설정 파일이 없거나, 그 안에 이름을 찾지 못했을 때
            st.error("비밀값을 찾지 못했어요. secrets.toml에 [stats]의 sheet_url과 [gcp_service_account]가 있는지 확인해 주세요.")
        except gspread.exceptions.SpreadsheetNotFound:  # 시트를 열 권한이 없거나 주소가 틀렸을 때
            st.error("시트를 열지 못했어요. 시트의 공유 버튼에서 서비스 계정 이메일(client_email)을 편집자로 추가했는지 확인해 주세요.")
        except Exception as error:  # 그 밖의 오류
            st.error(f"저장하지 못했어요: {type(error).__name__}: {error}")  # 오류 종류와 내용을 보여 줍니다
