import streamlit as st
import matplotlib.pyplot as plt
import koreanize_matplotlib
from matplotlib.colors import to_rgba
import numpy as np
from datetime import datetime

# 페이지 전환 함수
def navigate_to(page_name):
    st.session_state["current_page"] = page_name
    
# 2차시
def run():
    st.subheader("2차시📌 화산재와 생태계 시뮬레이션")
    # 1. 대기 시뮬레이션
    st.markdown("#### 1. 대기 시뮬레이션: 광량과 기온의 변화")
    st.markdown('''화산 활동이 일어나면 화산 가스와 함께 화산탄, 화산재 등의 쇄설물이 분출됩니다. 
                특히 화산 쇄설물은 대기 중으로 올라가 **햇빛을 차단**합니다. 아래 화산재 농도를 슬라이드하여 조절하며, **광량의 변화**와 이로 인한 **기온의 변화**를 확인해 봅시다.''')

    ash_density = st.slider("화산재 농도 (g/m³)", 0.1, 5.0, 0.1, step=0.1)
    def cal_light(ash):
        return np.exp(-ash/2)
    def cal_temp(light):
        return -2 * (1 - light)
    light_reduction = np.exp(-ash_density / 2)
    temperature_change = -2 * (1 - light_reduction)

    def get_color(base_color, i):
        rgba = to_rgba(base_color)
        return (rgba[0] * i, rgba[1] * i, rgba[2] * i, rgba[3])
    light_color = get_color('blue', light_reduction)
    temperature_color = get_color('yellow', light_reduction)

    # 대기 시뮬레이션 수치 해석
    st.markdown(f":gray-background[💨화산재 농도: {ash_density} g/m³] > :gray-background[🔅광량 변화: {light_reduction:.2f}%] > :gray-background[🌡️기온 변화: {temperature_change:.1f} °C]")
    if "latex_info1" not in st.session_state:
        st.session_state["latex_info1"] = None
    if st.button(label="수식 자세히 보기", key="수식 자세히 보기(1)"):
        st.session_state["latex_info1"] = "show"
    if st.session_state["latex_info1"] == "show":
        st.divider()
        st.markdown("**1. 화산재 농도에 따른 광량(빛의 양) 변화 수식:**")
        st.latex(r"light\_reduction = e^{-\frac{ash\_density}{2}}")
        st.markdown("""
        - 대기 중 화산재가 햇빛을 차단하는 효과는 비어의 법칙을 기반으로 합니다.
        - *비어의 법칙 (Beer's Law):* 대기 중 화학적/광학적 두께가 증가할수록 광량이 지수적으로 감소함
        """)
        st.markdown("**2. 화산재 농도에 따른 기온 변화 수식:**")
        st.latex(r"temperature\_change = -2 \cdot (1 - light\_reduction)")
        st.markdown("""
        - 화산재로 인해 광량이 감소하면 지표면에 도달하는 태양 복사량이 줄어들고 기온 감소를 초래합니다.
        - 일반적으로 대기 및 지표면 시스템의 에너지 균형 변화는 기온 변화로 이어지므로 단순한 선형 비례 모델을 기반으로 합니다.
        - 화산재로 인한 지구 평균 냉각 효과가 약 1~2°C인 사례를 반영해서 온도 변화 계수를 -2로 설정합니다.
        """)
        st.divider()
        if st.button(label="수식 설명 닫기", key="수식 설명 닫기(1)"):
            st.session_state["latex_info1"] = "close"

    # 대기 시뮬레이션 결과 시각화
    fig, ax = plt.subplots(1, 2, figsize=(6, 3))
    fig.subplots_adjust(wspace=0.5)
    ax[0].bar(["광량"], [light_reduction * 100], color=light_color)
    ax[0].set_ylim(0, 100)
    ax[0].set_ylabel("변화율 (%) 또는 (°C)")
    ax[1].bar(["평균 기온"], [temperature_change], color=temperature_color)
    ax[1].set_ylim(-2, 0)
    st.pyplot(fig)
    st.write("")
    st.write("")
    st.write("")

    ##################################################

    # 2. 생태계 시뮬레이션
    st.markdown("#### 2. 생태계 시뮬레이션: 동식물 군집 변화")
    st.markdown("")

    ash_density2 = st.slider("화산재 농도", 0.1, 5.0, 0.1, step=0.1)
    light_reduction2 = np.exp(-ash_density2 / 2)
    temperature_change2 = -2 * (1 - light_reduction2)
    def cal_survival(temp, light, alpha, beta):
        survival_rate = 100 - alpha * abs(temp) - beta * (100 - light * 100)
        return max(0, survival_rate)
    alpha_animal, beta_animal = 5, 0.2
    gamma_plant, delta_plant = 2, 0.5
    animal = cal_survival(temperature_change2, light_reduction2, alpha_animal, beta_animal)
    plant = cal_survival(temperature_change2, light_reduction2, gamma_plant, delta_plant)

    # 생태계 시뮬레이션 수치 해석
    st.markdown(f":gray-background[💨화산재 농도: {ash_density2} g/m³] > :gray-background[🔅광량 변화: {light_reduction2:.2f}%] > :gray-background[🌡️기온 변화: {temperature_change2:.1f} °C]")
    st.markdown(f" > :gray-background[🐾동물 생존율: {animal:.2f}%  /  🌱식물 생존율: {plant:.2f}%]")
    if "latex_info2" not in st.session_state:
        st.session_state["latex_info2"] = None
    if st.button(label="수식 자세히 보기", key="수식 자세히 보기(2)"):
        st.session_state["latex_info2"] = "show"
    if st.session_state["latex_info2"] == "show":
        st.divider()
        st.markdown("**화산재 농도에 따른 동물 및 식물 생존율 수식:**")
        st.latex(r"S_{\text{animal}} = 100 - \alpha \cdot |\Delta T| - \beta \cdot (100 - \text{light change})")
        st.latex(r"S_{\text{plant}} = 100 - \gamma \cdot |\Delta T| - \delta \cdot (100 - \text{light change})")
        st.markdown("""
        - 동식물의 민감도 계수는 종에 따라 다르지만, 일반적으로 광량, 기온 등의 변화가 복합적으로 작용하여 생태계의 균형을 변화시킵니다.
        - 동물(alpha, beta) : 온도 변화에 더 민감하고, 광량 변화에 덜 민감함
        - 식물(gamma, delta) : 광량 변화에 더 민감하고, 온도 변화에 덜 민감함
        """)
        st.divider()
        if st.button(label="수식 설명 닫기", key="수식 설명 닫기(2)"):
            st.session_state["latex_info2"] = "close"

    # 생태계 시뮬레이션 결과 시각화
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["동물 생존율", "식물 생존율"], [animal, plant], color=["brown", "green"], alpha=0.7)
    ax.set_ylabel("생존율 (%)")
    ax.set_ylim(0, 100)
    st.pyplot(fig)
    st.write("")
    st.write("")
    st.write("")

    ##################################################

    st.divider()
    st.subheader("2차시📌 마무리")
    if "flag2_1" not in st.session_state:
        st.session_state["flag2_1"] = False
    if "flag2_2" not in st.session_state:
        st.session_state["flag2_2"] = False
        
    st.markdown("**문제 1)** 화산 활동은 대기 중 햇빛을 차단해서 지구 전체의 평균 온도를 낮추는 등 생명체에 큰 영향을 미칩니다. 화산 분출이 일어났을 때, 이와 같이 생명 시스템에 미치는 피해를 줄이기 위한 방안에는 어떤 것들이 있을지 자유롭게 적어보세요.")
    answer1 = st.text_input("답: ")
    if st.button("제출"):
        if answer1:
            st.success("좋은 의견입니다:)")
            st.session_state["flag2_1"] = True
        else:
            st.warning("다시 도전해보세요.")
    st.write("")

    st.markdown("**문제 2)** 아래 실행 결과와 같이 실행될 수 있도록 코드의 주석 부분:red[(# 표시)]을 완성하세요.")
    result = """화산재 농도: 1 → 광량: 0.61, 기온: 0.74, 동물 생존율: 88.44, 식물 생존율: 78.85
화산재 농도: 2 → 광량: 0.37, 기온: 0.83, 동물 생존율: 83.20, 식물 생존율: 66.73
화산재 농도: 3 → 광량: 0.22, 기온: 0.89, 동물 생존율: 79.99, 식물 생존율: 59.37
화산재 농도: 4 → 광량: 0.14, 기온: 0.93, 동물 생존율: 78.03, 식물 생존율: 54.90]"""
    answer_code = """
import numpy as np

def cal_light(ash):
    return np.exp(-ash/2)
def cal_temp(light):
    return -2 * (1 - light)
def cal_survival(temp, light, alpha, beta):
    survival_rate = 100 - alpha * abs(temp) - beta * (100 - light * 100)
    return max(0, survival_rate)
animal_alpha = 5
animal_beta = 0.2
plant_alpha = 2
plant_beta = 0.5

for a in range(1, 5, 1):
    light = cal_light(a)
    temp = cal_light(light)
    animal = cal_survival(temp, light, animal_alpha, animal_beta)
    plant = cal_survival(temp, light, plant_alpha, plant_beta)
    st.write(f"화산재 농도: {a} → 광량: {light:.2f}, 기온: {temp:.2f}, 동물 생존율: {animal:.2f}, 식물 생존율: {plant:.2f}")
    """

    default_code = """
import numpy as np

def cal_light(ash):
    return np.exp(-ash/2)
def cal_temp(light):
    return -2 * (1 - light)
def cal_survival(temp, light, alpha, beta):
    survival_rate = 100 - alpha * abs(temp) - beta * (100 - light * 100)
    return max(0, survival_rate)
animal_alpha = 5
animal_beta = 0.2
plant_alpha = 2
plant_beta = 0.5

# range 범위에 알맞은 값을 쓰세요
for a in range(       ):
    # light라는 변수를 만들고 적절한 함수를 호출해서 "광량 변화" 값을 저장하세요

    # temp라는 변수를 만들고 적절한 함수를 호출해서 "기온 변화" 값을 저장하세요
    
    # animal이라는 변수를 만들고 적절한 함수를 호출해서 "동물 생존율" 값을 저장하세요
    
    # light라는 변수를 만들고 적절한 함수를 호출해서 "식물 생존율" 값을 저장하세요

    st.write(f"화산재 농도: {a} → 광량: {light:.2f}, 기온: {temp:.2f}, 동물 생존율: {animal:.2f}, 식물 생존율: {plant:.2f}")
    """
    result2 = st.text_area(label = "실행 결과: ", value = result, height = 150)
    answer2 = st.text_area(label = "코드: ", value = default_code, height = 400)
    if st.button("코드 실행"):
        try:
            exec(answer2)
            st.session_state["flag2_2"] = True
        except Exception as e:
            st.error(f"코드 실행 중 오류가 발생했습니다: {e}")
            st.session_state["flag2_1"] = False
    
    ##################################################

    col1, col2 = st.columns(2)
    with col1:
        if st.button("홈 화면으로", icon="🏡"):
            navigate_to("main")
    with col2:
        if st.button("2차시 완료", icon="🔥"):
            if st.session_state["flag2_1"] and st.session_state["flag2_2"]:
                st.session_state["2차시_completed"] = True
                st.session_state["2차시_completed_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.success("2차시를 완료했습니다!")
                navigate_to("main")
            else:
                st.warning("마무리 문제를 모두 풀고 제출하여야 차시를 완료할 수 있습니다.")