import streamlit as st

# 세션 상태 초기화
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "main"
if "1차시_completed" not in st.session_state:
    st.session_state["1차시_completed"] = False
if "1차시_completed_time" not in st.session_state:
    st.session_state["1차시_completed_time"] = None
if "2차시_completed" not in st.session_state:
    st.session_state["2차시_completed"] = False
if "2차시_completed_time" not in st.session_state:
    st.session_state["2차시_completed_time"] = None

# 페이지 전환 함수
def navigate_to(page_name):
    st.session_state["current_page"] = page_name

# UI 및 논리
st.title("🌏통합과학 X 정보💻 융합 수업")
st.header("지구 시스템 시뮬레이션")

if st.session_state["current_page"] == "main":
    st.subheader("학습할 차시를 선택하세요.")
    
    # 썸네일 컬럼 구성
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("thumbnail1.png")
        if st.button("1차시📌 화산대"):
            navigate_to("1차시")
        if st.session_state["1차시_completed"]:
            st.write(f"1차시 완료 시간: {st.session_state['1차시_completed_time']}")
    
    with col2:
        st.image("thumbnail2.png")
        if st.button("2차시📌 화산재와 생태계 시뮬레이션"):
            if st.session_state["1차시_completed"]:
                navigate_to("2차시")
            else:
                st.warning("1차시를 먼저 완료해야 합니다!")
        if st.session_state["2차시_completed"]:
            st.write(f"2차시 완료 시간: {st.session_state['2차시_completed_time']}")

    with col3:
        st.image("thumbnail3.png")
        if st.button("3차시📌 화산 가스와 산성비"):
            st.warning("3차시 준비 중...")
    
    with col4:
        st.image("thumbnail4.png")
        if st.button("4차시📌 화산 활동의 에너지와 충격량"):
            st.warning("4차시는 준비 중...")

elif st.session_state["current_page"] == "1차시":
    import session1
    session1.run()

elif st.session_state["current_page"] == "2차시":
    import session2
    session2.run()
