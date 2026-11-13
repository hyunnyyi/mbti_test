# =========================================================
# MBTI 지표별 비율 원그래프 그리기
# 실행: python pie_test.py
# 하는 일:
#   mbti_results_sample.csv를 읽어서
#   E vs I, S vs N, T vs F, J vs P 비율을 원그래프 4개로 그리고
#   mbti_pie.png로 저장합니다
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


# ========== 3. 원그래프 4개 그리기 ==========

PAIRS = ["EI", "SN", "TF", "JP"]   # 비교할 지표 4개 (유형 4글자의 순서와 같습니다)
NAMES = {                          # 글자마다 한글 뜻 (원그래프 이름표에 함께 씁니다)
    "E": "외향", "I": "내향", "S": "감각", "N": "직관",
    "T": "사고", "F": "감정", "J": "판단", "P": "인식",
}
COLORS = ["#e5b8b7", "#92ccdc"]    # 원그래프 색: 앞 글자는 연분홍, 뒤 글자는 하늘색 (앱과 같은 색)

fig, axes = plt.subplots(2, 2, figsize=(9, 9))  # 2줄 × 2칸 = 그래프 4개를 그릴 자리를 만듭니다
fig.suptitle("MBTI 지표별 비율", fontsize=20)   # 그림 전체의 큰 제목

for position, pair in enumerate(PAIRS):   # 지표를 하나씩 꺼냅니다 (position: 0, 1, 2, 3)
    ax = axes.flat[position]              # 이번 지표를 그릴 칸 (왼쪽 위 → 오른쪽 위 → 왼쪽 아래 → 오른쪽 아래)
    first, second = pair[0], pair[1]      # 지표의 두 글자 (예: E와 I)

    letters = df["유형"].str[position]    # 모든 사람의 유형에서 그 자리 글자만 꺼냅니다 (예: ISTJ → I)
    counts = [(letters == first).sum(), (letters == second).sum()]  # [첫 글자 인원, 두 번째 글자 인원]

    labels = [f"{first} ({NAMES[first]})\n{counts[0]}명",    # 이름표: 글자, 한글 뜻, 인원 (예: E (외향) 29명)
              f"{second} ({NAMES[second]})\n{counts[1]}명"]

    ax.pie(
        counts,                     # 원을 나눌 숫자
        labels=labels,              # 조각 바깥쪽 이름표
        colors=COLORS,              # 조각 색
        autopct="%.1f%%",           # 조각 안에 비율을 소수점 한 자리까지 표시 (예: 48.3%)
        startangle=90,              # 12시 방향부터 그리기 시작
        counterclock=False,         # 시계 방향으로 그리기
        wedgeprops={"edgecolor": "white", "linewidth": 2},  # 조각 사이에 흰 선을 넣어 구분합니다
        textprops={"fontsize": 12, "color": "#404040"},     # 글자 크기와 색 (진회색)
    )
    ax.set_title(f"{first} vs {second}", fontsize=15, pad=6)  # 각 원그래프의 제목 (예: E vs I)

    print(f"{first} vs {second}: {first} {counts[0]}명 / {second} {counts[1]}명")  # 화면에도 숫자를 출력합니다

fig.tight_layout()  # 글자가 잘리지 않게 여백을 자동으로 맞춥니다


# ========== 4. 그림 파일로 저장하고 화면에 보여 주기 ==========

fig.savefig(FOLDER / "mbti_pie.png", dpi=200)  # mbti_pie.png로 저장합니다 (포트폴리오용 선명한 화질)
print("원그래프를 mbti_pie.png로 저장했어요.")

plt.show()  # 그래프 창을 띄웁니다 (창을 닫으면 프로그램이 끝납니다)
