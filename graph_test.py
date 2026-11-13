# =========================================================
# MBTI 검사 결과 그래프 그리기
# 실행: python graph_test.py
# 하는 일:
#   1. mbti_results_sample.csv를 읽습니다
#   2. 총 검사 수와 지표별(E/I, S/N, T/F, J/P) 인원을 화면에 출력합니다
#   3. 유형별 인원 수를 많은 순서대로 막대 그래프로 그리고 mbti_graph.png로 저장합니다
# =========================================================

import platform  # 지금 컴퓨터가 윈도우인지 맥인지 알아보는 도구
from pathlib import Path  # 파일 경로를 다루는 도구

import matplotlib.pyplot as plt  # 그래프를 그리는 도구
import pandas as pd  # 표(데이터)를 다루는 도구

FOLDER = Path(__file__).parent  # 이 파이썬 파일이 있는 폴더 (다른 곳에서 실행해도 파일을 찾게 해 줍니다)


# ========== 1. 한글 글꼴 설정 ==========
# matplotlib은 기본 글꼴에 한글이 없어서, 한글이 □□□처럼 깨집니다
# 그래서 컴퓨터 종류에 맞는 한글 글꼴을 지정해 줍니다

if platform.system() == "Windows":          # 윈도우라면
    plt.rcParams["font.family"] = "Malgun Gothic"   # 맑은 고딕
elif platform.system() == "Darwin":         # 맥이라면
    plt.rcParams["font.family"] = "AppleGothic"     # 애플 고딕
else:                                       # 그 밖의 컴퓨터(리눅스 등)라면
    plt.rcParams["font.family"] = "NanumGothic"     # 나눔고딕 (설치되어 있어야 합니다)

plt.rcParams["axes.unicode_minus"] = False  
# 한글 글꼴에서 마이너스(-) 기호가 깨지는 것을 막습니다


# ========== 2. 데이터 읽기 ==========

df = pd.read_csv(FOLDER / "mbti_results_sample.csv", encoding="utf-8-sig")  # CSV 파일을 표로 읽습니다 (utf-8-sig: 엑셀용 파일도 한글이 안 깨지게)

total = len(df)  # 표의 줄 수 = 총 검사 수


# ========== 3. 숫자 출력하기 ==========

print("=" * 30)                       # 구분선
print(f"총 검사 수: {total}명")        # 총 검사 수
print("=" * 30)

print("[지표별 인원]")
for pair in ["EI", "SN", "TF", "JP"]:              # 지표 4개를 하나씩 꺼냅니다
    position = ["EI", "SN", "TF", "JP"].index(pair)  # 이 지표가 유형 4글자 중 몇 번째 글자인지 (0, 1, 2, 3)
    first, second = pair[0], pair[1]               # 지표의 두 글자 (예: E와 I)

    letters = df["유형"].str[position]             # 모든 사람의 유형에서 그 자리 글자만 꺼냅니다 (예: ISTJ → I)
    first_count = (letters == first).sum()         # 첫 글자인 사람 수
    second_count = (letters == second).sum()       # 두 번째 글자인 사람 수

    print(f"{first}: {first_count}명 / {second}: {second_count}명")  # 예) E: 25명 / I: 35명


# ========== 4. 유형별 인원 세기 ==========

counts = df["유형"].value_counts()  # 유형별로 몇 명인지 셉니다 (많은 순서대로 자동 정렬됩니다)

print()
print("[유형별 인원 (많은 순서)]")
for mbti, count in counts.items():  # 유형과 인원을 하나씩 꺼냅니다
    print(f"{mbti}: {count}명")


# ========== 5. 막대 그래프 그리기 ==========

fig, ax = plt.subplots(figsize=(10, 5.5))  # 그림판(fig)과 그래프 영역(ax)을 만듭니다 (가로 10, 세로 5.5인치)

ax.bar(counts.index, counts.values, color="#337589", width=0.6)  # 막대 그래프: 가로는 유형, 세로는 인원 수

ax.set_title("MBTI 유형 검사 결과", fontsize=18, pad=16)  # 그래프 제목
ax.set_xlabel("유형", fontsize=12)                          # 가로축 이름
ax.set_ylabel("인원수", fontsize=12)                        # 세로축 이름

ax.yaxis.get_major_locator().set_params(integer=True)  # 세로축 눈금을 정수(1명, 2명...)로만 표시합니다
ax.grid(axis="y", color="#e5e5e5", linewidth=0.8)      # 가로 방향 보조선을 연하게 그립니다
ax.set_axisbelow(True)                                 # 보조선이 막대 뒤로 가게 합니다
for side in ["top", "right"]:                          # 위쪽, 오른쪽 테두리는
    ax.spines[side].set_visible(False)                 # 지워서 깔끔하게 만듭니다

fig.tight_layout()  # 글자가 잘리지 않게 여백을 자동으로 맞춥니다


# ========== 6. 그림 파일로 저장하고 화면에 보여 주기 ==========

fig.savefig(FOLDER / "mbti_graph.png", dpi=200)  # mbti_graph.png로 저장합니다 (dpi=200: 포트폴리오용 선명한 화질)
print()
print("그래프를 mbti_graph.png로 저장했어요.")

plt.show()  # 그래프 창을 띄웁니다 (창을 닫으면 프로그램이 끝납니다)
