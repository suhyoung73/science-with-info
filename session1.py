import pandas as pd
import streamlit as st
import pydeck as pdk
from datetime import datetime

# 페이지 전환 함수
def navigate_to(page_name):
    st.session_state["current_page"] = page_name

# 1차시
def run():
    st.subheader("1차시📌 지구의 화산대")
    volcano_data = pd.read_csv('volcanoes around the world in 2021.csv')
    plate_data = pd.read_csv('tectonic plate boundaries.csv')

    # Pydeck 레이어 정의
    volcano_layer = pdk.Layer(
        "ScatterplotLayer",
        data=volcano_data,
        get_position=["Longitude", "Latitude"],
        get_color=[255, 0, 0, 200],
        get_radius=20000,
        pickable=True
    )
    plate_layer = pdk.Layer(
        "ScatterplotLayer",
        data=plate_data,
        get_position=["lon", "lat"],
        get_color=[0, 255, 0, 200],
        get_radius=20000,
        pickable=True,
    )

    # 초기 Viewpoint 설정
    view_state1 = pdk.ViewState(
        latitude=volcano_data["Latitude"].mean(),
        longitude=volcano_data["Longitude"].mean(),
        zoom=2,
        pitch=50
    )

    # 초기 Pydeck Map 구성
    st.markdown("#### 1. 화산 지도")
    st.markdown('''다음 지도에서 :red[빨간색 점]은 **지구의 화산 위치**를 나타낸 것입니다. 화산 지구 전체에 고르고 분포되어 있나요, 아니면 집중적으로 분포되어 있는 지역이 있나요? 
                지도 위에서 마우스를 움직여 화산의 위치를 확인해 봅시다. 스크롤하면 확대/축소 가능합니다!''')
    total_map = pdk.Deck(layers=[volcano_layer], initial_view_state=view_state1, tooltip={"text": "{Volcano Name}\nLocation: {Location}"})
    st.pydeck_chart(total_map)

    # 레이어 추가된 Pydeck Map 구성
    st.markdown('''화산이 거의 위치하지 않는 지역도 있는 반면, 여러 개의 화산이 집중적으로 모여 있는 지역도 있습니다. 
                이처럼 화산 활동이 활발하게 일어나며, 띠 모양으로 화산이 분포하고 있는 곳을 **화산대**라고 합니다.''') 
    st.markdown('''다음으로는 아래의 지도를 살펴봅시다. 새롭게 추가된 :green[초록색 점]은 **판의 경계**를 점으로 나타낸 것입니다.
                :red[빨간색 점]과 :green[초록색 점] 사이에 상관관계가 있나요?''')
    volcano_plate_map = pdk.Deck(layers=[volcano_layer, plate_layer], initial_view_state=view_state1)
    st.pydeck_chart(volcano_plate_map)

    st.markdown('''우리나라의 이웃 나라인 일본, 그리고 남아메리카 대륙의 칠레 인근의 화산 분포를 살펴봅시다. :red[빨간색 점]과 :green[초록색 점]의 위치가 거의 동일한 분포를 보이고 있죠?
                :red[화산의 분포]가 :green[판의 경계]와 밀접한 상관관계가 있음을 알 수 있겠네요.
                이처럼 **화산대**는 특히 **특정한 판의 경계 부분**을 따라 나타난다는 점을 지도를 통해 직접 눈으로 확인해 보았습니다.👀''')
    st.info("💡 더 생각해보기: 그렇다면 어떤 판의 경계에서 화산 활동이 활발히 일어날까요?")
    st.write("")
    st.write("")
    st.write("")

    ##################################################

    st.markdown("#### 2. 화산 데이터: 2차원 배열")
    st.markdown('''다음은 지도 위에 표시하였던 **화산 데이터**를 표 형태로 나타낸 것입니다. 
                행과 열을 각각 선택했을 때 어떤 데이터가 나타나는지 확인해보며, **2차원 배열**이라는 자료구조의 행, 열 개념을 복습해 봅시다.''')
    total_column = ['Volcano Name', 'Region', 'Country', 'Location', 'Elevation (m)', 'Type', 'Status']
    st.dataframe(volcano_data[total_column])

    selected_column = st.selectbox("열 선택", ["전체"] + total_column)
    if selected_column != "전체":
        unique_values = volcano_data[selected_column].dropna().unique().tolist()
        selected_value = st.selectbox("ㄴ 열의 값 선택", ["전체"] + unique_values)
        if selected_value != "전체":
            filtered_data = volcano_data[volcano_data[selected_column] == selected_value]
            st.dataframe(filtered_data)
        else:
            filtered_data = volcano_data
    else:
        filtered_data = volcano_data

    if not filtered_data.empty:
        row_options = filtered_data.index.tolist()
        selected_row = st.selectbox("행 선택", ["전체"] + row_options)
        if selected_row != "전체":
            filtered_row = filtered_data.loc[[selected_row]]
            st.dataframe(filtered_row)
            st.markdown(f"{filtered_row['Volcano Name'].values[0]} 화산은 {filtered_row.index[0]}**행** 데이터로, {selected_column}**열**의 값이 {selected_value}인 화산 중 하나입니다.")

    # Pydeck 레이어 재정의
    new_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position=["Longitude", "Latitude"],
        get_color=[255, 0, 0, 200],
        get_radius=40000,
        pickable=True
    )

    # Viewpoint 재설정
    view_state2 = pdk.ViewState(
        latitude=filtered_data["Latitude"].mean() if not filtered_data.empty else 0,
        longitude=filtered_data["Longitude"].mean() if not filtered_data.empty else 0,
        zoom=2,
        pitch=50
    )

    # Pydeck Map 재구성
    new_map = pdk.Deck(layers=[new_layer], initial_view_state=view_state2, tooltip={"text": "{Volcano Name}\nLocation: {Location}"})
    st.pydeck_chart(new_map)
    st.write("")
    st.write("")
    st.write("")

    ##################################################
    
    st.divider()
    st.subheader("1차시📌 마무리")
    if "flag1" not in st.session_state:
        st.session_state["flag1"] = False
    if "flag2" not in st.session_state:
        st.session_state["flag2"] = False

    st.markdown('''**문제 1)** 우리에게 익숙한 \"표\" 형태는 가로와 세로로 이루어져 있습니다. 
                이러한 표 형태를 파이썬 코드로 나타낼 때 2차원 배열이라는 자료구조를 사용하는데, 이는 행과 열이라는 2개의 인덱스를 사용해서 데이터를 나타내는 것을 의미합니다. 
                그렇다면 행과 열은 각각 무엇을 의미하는지 쓰세요.''')
    row_answer = st.text_input("행: ")
    col_answer = st.text_input("열: ")
    if st.button(label="제출", key="1) 제출"):
        if "가로" in row_answer and "세로" in col_answer:
            st.success("정답입니다!")
            st.session_state["flag1"] = True
        else:
            st.warning("다시 도전해보세요.")
    st.write("")
    st.write("")

    st.markdown('''**문제 2)** 화산대가 주로 분포하는 지역은 어디인가요?''')
    vol_answer = st.radio(
        "답: ", ["판의 중앙 부분", "판의 경계 부근"]
    )
    if st.button(label="제출", key="2) 제출"):
        if vol_answer == "판의 경계 부근":
            st.success("정답입니다!")
            st.session_state["flag2"] = True
        else:
            st.warning("다시 도전해보세요.")

    ##################################################
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("홈 화면으로", icon="🏡"):
            navigate_to("main")
    with col2:
        if st.button("1차시 완료", icon="🔥"):
            if st.session_state["flag1"] and st.session_state["flag2"]:
                st.session_state["1차시_completed"] = True
                st.session_state["1차시_completed_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("1차시를 완료했습니다!")
                navigate_to("main")
            else:
                st.warning("마무리 문제를 모두 풀고 제출하여야 차시를 완료할 수 있습니다.")