import streamlit as st
import pandas as pd
# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="My Planner")
# 2. 사이드바: 사용자 프로필
with st.sidebar:
    st.header("프로필 설정")
    name = st.text_input("이름", "김코딩")
    study_time = st.slider("오늘 목표 공부 시간", 1, 10, 3)
    st.button("설정 저장")
# 3. 메인 화면
st.title(f"{name}님의 스터디 플래너 대시보드")
# 4. 상단 지표 (메트릭 + 컬럼)
col1, col2, col3 = st.columns(3)
col1.metric("오늘 공부한 시간", "2시간", "+30분")
col2.metric("남은 목표", f"{study_time - 2}시간", "화이팅!")
col3.metric("현재 집중도", "최상", "으라차차!")
st.divider() # 구분선
# 5. 상세 내용 (탭)
tab_todo, tab_chart = st.tabs(["할 일 목록(To-Do)", "주간 리포트"])
with tab_todo:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.checkbox("파이썬 복습하기")
        st.checkbox("영어 단어 50개 외우기")
        st.checkbox("운동 1시간 하기")
    with col_b:
        st.image("https://pusan.ac.kr/_contents/kor/_Img/Main/introintro80-logo.png", caption="PNU 로고")
             
with tab_chart:
    st.write("이번 주 공부 시간 추이")
    chart_data = pd.DataFrame({'요일': ['월', '화', '수', '목', '금'], '시간': [3, 4, 2, 5, 3]})
    st.bar_chart(chart_data.set_index('요일'))

