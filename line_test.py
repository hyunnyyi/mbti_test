# =========================================================
# 날짜별 검사 수 꺾은선 그래프 그리기
# 실행: python line_test.py
# 하는 일:
#   mbti_results_sample.csv를 읽어서
#   하루에 몇 명이 검사했는지 꺾은선 그래프로 그리고
#   mbti_line.png로 저장합니다
# =========================================================

import platform  # 지금 컴퓨터가 윈도우인지 맥인지 알아보는 도구
from pathlib import Path  # 파일 경로를 다루는 도구

import matplotlib.pyplot as plt  # 그래프를 그리는 도구
import pandas as pd  # 표(데이터)를 다루는 도구

FOLDER = Path(__file__).parent  # 이 파이썬 파일이 있는 폴더


# ========== 1. 한글 글꼴 설정 ==========
# matplotlib 기본 글꼴에는 한글이 없어서 □□□처럼 깨지므로, 한글 글꼴을 지정합니다

if platform.system() == "Windows":                  # 윈도우라면
    plt.rcParams["font.family"] = "Malgun Gothic"   # 맑은 고딕
elif platform.system() == "Darwin":                 # 맥이라면
    plt.rcParams["font.family"] = "AppleGothic"     # 애플 고딕
else:                                               # 그 밖의 컴퓨터라면
    plt.rcParams["font.family"] = "NanumGothic"     # 나눔고딕 (설치되어 있어야 합니다)

plt.rcParams["axes.unicode_minus"] = False  # 마이너스(-) 기호가 깨지는 것을 막습니다


# ========== 2. 데이터 읽기 ==========

df = pd.read_csv(FOLDER / "mbti_results_sample.csv", encoding="utf-8-sig")  # CSV 파일을 표로 읽습니다
df["시간"] = pd.to_datetime(df["시간"])  # "2026-11-03 10:13:10" 같은 글자를 날짜·시간 값으로 바꿉니다


# ========== 3. 날짜별 검사 수 세기 ==========

daily = df.set_index("시간").resample("D").size()  # 하루(D) 단위로 묶어서 몇 줄(몇 명)인지 셉니다
                                                   # 검사가 없던 날도 0명으로 채워 줍니다

print("[날짜별 검사 수]")
for day, count in daily.items():                       # 날짜와 인원을 하나씩 꺼냅니다
    print(f"{day.strftime('%Y-%m-%d')}: {count}명")    # 예) 2026-11-03: 13명
print(f"총 검사 수: {daily.sum()}명")


# ========== 4. 꺾은선 그래프 그리기 ==========

labels = [day.strftime("%m/%d") for day in daily.index]  # 가로축 이름표: 11/03처럼 월/일만 씁니다

fig, ax = plt.subplots(figsize=(9, 5))  # 그림판(fig)과 그래프 영역(ax)을 만듭니다 (가로 9, 세로 5인치)

ax.plot(labels, daily.values,           # 가로는 날짜, 세로는 검사 수
        color="#337589",                # 선 색: 앱의 진한 하늘색
        linewidth=2,                    # 선 굵기
        marker="o", markersize=8)       # 날짜마다 동그라미 점을 찍습니다

for x, y in zip(labels, daily.values):              # 점마다
    ax.annotate(f"{y}명", (x, y),                   # 인원 수를 적습니다
                textcoords="offset points", xytext=(0, 10),  # 점보다 10포인트 위에
                ha="center", fontsize=11, color="#404040")   # 가운데 정렬, 진회색 글자

ax.set_title("날짜별 검사 수", fontsize=18, pad=16)  # 그래프 제목

# 그림 오른쪽 아래 구석에 총 참여 인원을 작은 글씨로 적습니다
fig.text(0.985, 0.02,                       # 그림 전체의 오른쪽(98.5%), 아래쪽(2%) 위치
         f"총 참여 인원 {daily.sum()}명",    # 적을 글자 (예: 총 참여 인원 60명)
         ha="right", va="bottom",           # 오른쪽 아래를 기준으로 맞춥니다
         fontsize=10, color="#6b6b6b")      # 작은 글씨, 회색
ax.set_xlabel("날짜", fontsize=12)                    # 가로축 이름
ax.set_ylabel("검사 수(명)", fontsize=12)             # 세로축 이름

ax.set_ylim(0, daily.max() * 1.25)                      # 세로축을 0부터 시작하고, 위쪽에 글자가 들어갈 여유를 둡니다
ax.yaxis.get_major_locator().set_params(integer=True)   # 세로축 눈금을 정수로만 표시합니다
ax.grid(axis="y", color="#e5e5e5", linewidth=0.8)       # 가로 방향 보조선을 연하게 그립니다
ax.set_axisbelow(True)                                  # 보조선이 선 뒤로 가게 합니다
for side in ["top", "right"]:                           # 위쪽, 오른쪽 테두리는
    ax.spines[side].set_visible(False)                  # 지워서 깔끔하게 만듭니다

fig.tight_layout()  # 글자가 잘리지 않게 여백을 자동으로 맞춥니다


# ========== 5. 그림 파일로 저장하고 화면에 보여 주기 ==========

fig.savefig(FOLDER / "mbti_line.png", dpi=200)  # mbti_line.png로 저장합니다 (포트폴리오용 선명한 화질)
print("꺾은선 그래프를 mbti_line.png로 저장했어요.")

plt.show()  # 그래프 창을 띄웁니다 (창을 닫으면 프로그램이 끝납니다)
