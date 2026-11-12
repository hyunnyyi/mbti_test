// =========================================================
// 나의 MBTI 검사 - 동작 파일
// 데이터 불러오기 → 화면 전환 → 답 적기 → 점수 계산 → 결과 보여 주기
// =========================================================


// ========== 1. 데이터를 담을 변수 ==========

let questions = [];  // questions.json에서 불러온 질문 12개
let types = {};      // types.json에서 불러온 16유형의 이름과 설명
let answers = [];    // 답안지: 질문마다 고른 선택지 번호(0 또는 1)를 적어 둡니다
let current = 0;     // 지금 보고 있는 질문의 순서 (0이 첫 번째 질문)


// ========== 2. 화면에서 바꿀 곳 찾기 ==========
// index.html에 붙여 둔 id 이름표로 자리를 찾아 변수에 담아 둡니다

const startScreen = document.getElementById("start-screen");        // 시작 화면
const questionScreen = document.getElementById("question-screen");  // 질문 화면
const resultScreen = document.getElementById("result-screen");      // 결과 화면

const appTitle = document.getElementById("app-title");              // 제목
const questionCount = document.getElementById("question-count");    // 문항 수
const startBtn = document.getElementById("start-btn");              // 검사 시작 버튼

const backBtn = document.getElementById("back-btn");                // 이전 버튼
const progressText = document.getElementById("progress-text");      // 진행 숫자 (3 / 12)
const progressFill = document.getElementById("progress-fill");      // 진행 막대
const questionNumber = document.getElementById("question-number");  // 질문 번호 (Q3)
const questionText = document.getElementById("question-text");      // 질문 내용
const choiceBtn1 = document.getElementById("choice-1");             // 선택지 1 버튼
const choiceBtn2 = document.getElementById("choice-2");             // 선택지 2 버튼

const resultType = document.getElementById("result-type");          // 4글자 유형
const resultName = document.getElementById("result-name");          // 유형 이름
const resultDesc = document.getElementById("result-desc");          // 한 줄 설명
const restartBtn = document.getElementById("restart-btn");          // 다시 하기 버튼


// ========== 3. 데이터 불러오기 ==========
// async와 await: 파일을 다 읽을 때까지 기다렸다가 다음 줄로 넘어갑니다

async function loadData() {
  startBtn.disabled = true;  // 데이터를 읽는 동안에는 시작 버튼을 누를 수 없게 합니다

  try {  // try: 아래 일을 해 보고, 실패하면 catch로 갑니다
    const questionResponse = await fetch("questions.json");  // 질문 파일을 요청합니다
    const typeResponse = await fetch("types.json");          // 유형 파일을 요청합니다

    if (!questionResponse.ok || !typeResponse.ok) {  // 파일을 찾지 못했으면
      throw new Error("데이터 파일을 찾지 못했어요");  // 일부러 실패로 보냅니다
    }

    const questionData = await questionResponse.json();  // 질문 파일 내용을 꺼냅니다
    types = await typeResponse.json();                   // 유형 파일 내용을 꺼냅니다
    questions = questionData.questions;                  // 질문 목록만 저장합니다

    appTitle.textContent = questionData.app_name;  // 제목을 app_name으로 바꿉니다
    document.title = questionData.app_name;        // 브라우저 탭 이름도 바꿉니다
    questionCount.textContent = questions.length;  // 문항 수를 표시합니다

    startBtn.disabled = false;  // 준비가 끝났으니 시작 버튼을 누를 수 있게 합니다
  } catch (error) {  // 파일을 읽지 못했을 때
    console.error(error);  // 개발자 도구에 오류 내용을 남깁니다
    startBtn.textContent = "질문을 불러오지 못했어요";  // 버튼 글자로 문제를 알려 줍니다
    alert("질문 파일을 읽지 못했어요.\nindex.html을 더블클릭하지 말고, 파이썬 웹 서버로 열어 주세요.");  // 해결 방법을 안내합니다
  }
}


// ========== 4. 화면 바꾸기 ==========

function showScreen(screen) {  // 보여 줄 화면 하나를 받습니다
  startScreen.hidden = true;     // 시작 화면을 숨깁니다
  questionScreen.hidden = true;  // 질문 화면을 숨깁니다
  resultScreen.hidden = true;    // 결과 화면을 숨깁니다
  screen.hidden = false;         // 받은 화면만 보이게 합니다
  window.scrollTo(0, 0);         // 화면 맨 위로 올라갑니다
}


// ========== 5. 검사 시작 ==========

function startTest() {
  answers = [];  // 답안지를 비웁니다
  current = 0;   // 첫 번째 질문부터 시작합니다
  showQuestion();               // 첫 질문을 채워 넣습니다
  showScreen(questionScreen);   // 질문 화면을 보여 줍니다
}


// ========== 6. 질문 보여 주기 ==========

function showQuestion() {
  const question = questions[current];  // 지금 순서의 질문을 꺼냅니다
  const total = questions.length;       // 전체 질문 수 (12)

  progressText.textContent = (current + 1) + " / " + total;          // 진행 숫자: 예) 3 / 12
  progressFill.style.width = ((current + 1) / total * 100) + "%";    // 진행 막대 길이를 바꿉니다
  questionNumber.textContent = "Q" + question.id;                    // 질문 번호: 예) Q3
  questionText.textContent = question.text;                          // 질문 내용
  choiceBtn1.textContent = question.choices[0].text;                 // 선택지 1 문장
  choiceBtn2.textContent = question.choices[1].text;                 // 선택지 2 문장

  if (current === 0) {                     // 첫 번째 질문이면
    backBtn.style.visibility = "hidden";   // 이전 버튼을 숨깁니다 (자리는 그대로 둡니다)
  } else {                                 // 두 번째 질문부터는
    backBtn.style.visibility = "visible";  // 이전 버튼을 보여 줍니다
  }

  // 새 질문이 살짝 떠오르는 움직임을 다시 보여 줍니다
  questionScreen.style.animation = "none";  // 움직임을 잠깐 껐다가
  void questionScreen.offsetWidth;          // 브라우저가 화면을 다시 계산하게 한 뒤
  questionScreen.style.animation = "";      // 다시 켜면 처음부터 다시 움직입니다
}


// ========== 7. 선택지 고르기 ==========

function choose(index) {  // index: 첫 번째 선택지는 0, 두 번째 선택지는 1
  answers[current] = index;  // 답안지의 지금 칸에 고른 번호를 적습니다 (전에 적은 답이 있으면 바뀝니다)

  if (current < questions.length - 1) {  // 아직 마지막 질문이 아니면
    current = current + 1;  // 다음 질문으로 넘어가고
    showQuestion();         // 그 질문을 보여 줍니다
  } else {                  // 마지막 질문이었으면
    showResult();           // 결과를 보여 줍니다
  }
}


// ========== 8. 이전 질문으로 돌아가기 ==========

function goBack() {
  if (current > 0) {         // 첫 번째 질문이 아니면
    current = current - 1;   // 한 칸 앞으로 돌아가고
    showQuestion();          // 그 질문을 다시 보여 줍니다
  }
}


// ========== 9. 점수 계산과 결과 보여 주기 ==========

function showResult() {
  // 1단계: 점수판을 모두 0점으로 준비합니다
  const scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };

  // 2단계: 답안지를 1번부터 12번까지 하나씩 채점합니다
  for (let i = 0; i < questions.length; i++) {           // 질문을 하나씩 꺼냅니다
    const chosen = questions[i].choices[answers[i]];      // 그 질문에서 고른 선택지
    for (const letter in chosen.score) {                  // 선택지의 점수 알파벳을 꺼냅니다 (예: E)
      scores[letter] = scores[letter] + chosen.score[letter];  // 그 알파벳에 점수를 더합니다
    }
  }

  // 3단계와 4단계: 지표마다 점수가 높은 글자를 골라 순서대로 붙입니다
  const pairs = ["EI", "SN", "TF", "JP"];  // 비교할 지표 4개 (이 순서대로 붙입니다)
  let mbti = "";                           // 결과 유형을 담을 빈 글자

  for (const pair of pairs) {   // 지표를 하나씩 꺼냅니다 (예: "EI")
    const first = pair[0];      // 첫 글자 (예: E)
    const second = pair[1];     // 두 번째 글자 (예: I)

    if (scores[first] > scores[second]) {  // 첫 글자 점수가 더 높으면
      mbti = mbti + first;                 // 첫 글자를 붙입니다
    } else {                               // 두 번째 글자가 높거나 같으면
      mbti = mbti + second;                // 두 번째 글자를 붙입니다 (같을 때 규칙)
    }

    // 점수 숫자를 화면에 적습니다
    document.getElementById("score-" + first).textContent = scores[first];    // 왼쪽 점수
    document.getElementById("score-" + second).textContent = scores[second];  // 오른쪽 점수

    // 점수 막대: 왼쪽 글자가 차지하는 비율만큼 분홍색을 칠합니다
    const sum = scores[first] + scores[second];                        // 두 글자 점수의 합
    let percent = 50;                                                  // 합이 0이면 반반으로 둡니다
    if (sum > 0) {                                                     // 점수가 있으면
      percent = scores[first] / sum * 100;                             // 왼쪽 글자 비율을 구합니다
    }
    document.getElementById("fill-" + pair).style.width = percent + "%";  // 막대 길이를 바꿉니다
  }

  // 5단계: types.json에서 유형을 찾아 이름과 설명을 보여 줍니다
  resultType.textContent = mbti;  // 4글자 유형을 적습니다
  const info = types[mbti];       // 유형 정보를 찾습니다

  if (info) {                                  // 찾았으면
    resultName.textContent = info.name;        // 유형 이름을 적고
    resultDesc.textContent = info.description; // 한 줄 설명을 적습니다
  } else {                                     // 못 찾았으면 (types.json을 고치다 실수했을 때)
    resultName.textContent = "설명을 준비 중이에요";  // 안내 문구를 적고
    resultDesc.textContent = "";                     // 설명은 비워 둡니다
  }

  showScreen(resultScreen);  // 결과 화면을 보여 줍니다
}


// ========== 10. 다시 하기 ==========

function restart() {
  answers = [];  // 답안지를 비웁니다
  current = 0;   // 질문 순서를 처음으로 되돌립니다
  showScreen(startScreen);  // 시작 화면을 보여 줍니다
}


// ========== 11. 버튼을 누르면 할 일 연결하기 ==========
// addEventListener("click", 함수): 버튼을 누르면 그 함수를 실행합니다

startBtn.addEventListener("click", startTest);                    // 검사 시작
choiceBtn1.addEventListener("click", function () { choose(0); }); // 선택지 1을 고름
choiceBtn2.addEventListener("click", function () { choose(1); }); // 선택지 2를 고름
backBtn.addEventListener("click", goBack);                        // 이전 질문으로
restartBtn.addEventListener("click", restart);                    // 다시 하기


// ========== 12. 페이지가 열리면 데이터부터 불러옵니다 ==========
loadData();
