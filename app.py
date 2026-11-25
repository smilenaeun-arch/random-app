import random
import streamlit as st

# 1. 데이터 구조 (리스트 & 딕셔너리): 과목 및 과목별 랜덤 학습 미션
subjects = ["국어", "영어", "수학", "사회", "과학"]

missions = {
    "국어": ["비문학(독서) 2지문 시간 재고 풀기", "문학 고전시가 핵심 어휘 정리", "화법과 작문 기출 1세트 풀이"],
    "영어": ["빈칸 추론·순서 배열 5문제 집중 풀이", "EBS 연계 핵심 영단어 50개 암기", "듣기 평가 오답 딕테이션"],
    "수학": ["모의고사 4점 준킬러 3문제 오답 노트", "개념원리 취약 단원 공식 백지 복습", "기출 문제 10문제 타임어택"],
    "사회": ["기출 선지 O/X 퀴즈로 개념 확인", "도표·자료 해석 유형 집중 연습", "단원별 핵심 개념 마인드맵 그리기"],
    "과학": ["실험·탐구 과정 분석 문제 풀이", "자주 틀리는 킬러 단원 계산 연습", "기출 오답 선지 개념서에서 찾아 정리"],
}

# 2. 함수 (def): 성적과 시간을 받아 맞춤형 스케줄 생성
def make_schedule(grades, start_t, end_t):
    total_hours = end_t - start_t
    
    # 등급 숫자가 클수록(예: 5등급 > 1등급) 취약 과목이므로 내림차순 정렬
    sorted_subjects = sorted(grades.items(), key=lambda x: x[1], reverse=True)
    weakest_subject = sorted_subjects[0][0]
    
    # 취약 과목에 가중치(2배)를 두어 배정 후보 리스트 생성
    weighted_pool = []
    for subj, grade in sorted_subjects:
        if grade >= 4:
            weighted_pool.extend([subj, subj])  # 4등급 이하 취약 과목은 2번 추가
        else:
            weighted_pool.append(subj)
            
    schedule_table = []
    # 4. 반복문 (for): 시작 시간부터 종료 시간까지 1시간 단위로 스케줄 배정
    for i in range(total_hours):
        current_start = start_t + i
        current_end = current_start + 1
        
        # 순서대로 과목 배정 (시간이 길면 순환)
        assigned_subj = weighted_pool[i % len(weighted_pool)]
        # random 라이브러리로 해당 과목의 오늘의 추천 미션 뽑기
        random_mission = random.choice(missions[assigned_subj])
        
        schedule_table.append({
            "시간대": f"{current_start:02d}:00 ~ {current_end:02d}:00",
            "배정 과목": assigned_subj,
            "취약도(입력 등급)": f"{grades[assigned_subj]}등급",
            "오늘의 랜덤 추천 미션": random_mission
        })
        
    return weakest_subject, total_hours, schedule_table

# --- 화면 UI 구성 ---
st.title("📚 맞춤형 공부 스케줄 관리")
st.caption("수능·모의고사 대비 취약 과목 집중 케어 플래너")

st.subheader("1. 모의고사 성적 입력 (등급)")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    kor = st.selectbox("국어", list(range(1, 10)), index=2)
with col2:
    eng = st.selectbox("영어", list(range(1, 10)), index=2)
with col3:
    math = st.selectbox("수학", list(range(1, 10)), index=3)
with col4:
    soc = st.selectbox("사회", list(range(1, 10)), index=1)
with col5:
    sci = st.selectbox("과학", list(range(1, 10)), index=2)

st.subheader("2. 오늘의 공부 시간 설정")
start_time = st.slider("공부 시작 시간 (시)", min_value=0, max_value=24, value=18)
end_time = st.slider("공부 끝내는 시간 (시)", min_value=0, max_value=24, value=23)

# 버튼 클릭 시 실행
if st.button("분석하기"):
    # 3. 조건문 (if-else): 시간 입력 오류 체크
    if end_time <= start_time:
        st.error("⚠️ 공부 끝내는 시간은 시작 시간보다 늦어야 합니다! 슬라이더를 다시 설정해주세요.")
    else:
        user_grades = {
            "국어": kor,
            "영어": eng,
            "수학": math,
            "사회": soc,
            "과학": sci
        }
        
        weakest, total_h, result_table = make_schedule(user_grades, start_time, end_time)
        
        st.divider()
        st.subheader("📊 분석 결과 및 맞춤형 시간표")
        
        # 텍스트 메시지 및 강조 수치(Metric) 출력
        st.success(f"💡 모의고사 성적 분석 결과, 가장 집중 보완이 필요한 과목은 **[{weakest}]**입니다!")
        
        m1, m2 = st.columns(2)
        m1.metric(label="총 순공부 목표 시간", value=f"{total_h}시간")
        m2.metric(label="최우선 집중 과목", value=f"{weakest} ({user_grades[weakest]}등급)")
        
        # 테이블(표) 형태로 결과 출력
        st.table(result_table)
