
import streamlit as st

st.set_page_config(
    page_title="우리 문화 추천",
    page_icon="🇰🇷",
    layout="wide"
)

st.title("우리 문화 추천")
st.write("한국 생활이 낯선 분들을 위한 문화, 음식, 관광지 안내")

st.sidebar.title("메뉴")
menu = st.sidebar.radio(
    "원하는 항목을 선택하세요.",
    ["우리 문화와 예절", "한국 음식 추천", "한국 관광지 추천"]
)

if menu == "우리 문화와 예절":
    st.header("한국 문화와 예절")
    st.write("한국에서 생활할 때 알아 두면 좋은 예절을 소개합니다.")

    with st.expander("인사 예절"):
        st.write("한국에서는 인사할 때 고개를 가볍게 숙이기도 합니다.")
        st.write("처음 만나는 사람이나 어른에게는 존댓말을 사용하는 것이 좋습니다.")

    with st.expander("식사 예절"):
        st.write("어른이 먼저 식사를 시작할 때까지 기다리는 것이 일반적인 예절입니다.")
        st.write("식사 중에는 다른 사람을 배려하고 조용히 대화합니다.")

    with st.expander("대중교통 예절"):
        st.write("버스나 지하철에서는 줄을 서서 차례대로 탑니다.")
        st.write("노약자, 임산부 등에게 자리를 양보할 수 있습니다.")

    with st.expander("쓰레기 분리배출"):
        st.write("일반 쓰레기, 음식물 쓰레기, 재활용품을 구분해서 버립니다.")
        st.write("지역마다 배출 방법이 다를 수 있으므로 지역 안내를 확인합니다.")

elif menu == "한국 음식 추천":
    st.header("한국 음식 추천")
    st.write("먹고 싶은 종류를 선택하면 관련 음식을 추천합니다.")

    food_type = st.selectbox(
        "음식 종류",
        ["전체", "밥과 식사", "면 요리", "간식", "매운 음식이 아닌 음식"]
    )

    foods = [
        {
            "name": "비빔밥",
            "type": "밥과 식사",
            "description": "밥에 여러 채소와 양념을 넣어 비벼 먹는 음식입니다."
        },
        {
            "name": "불고기",
            "type": "밥과 식사",
            "description": "양념한 고기를 구워 먹는 음식입니다."
        },
        {
            "name": "김밥",
            "type": "간식",
            "description": "김에 밥과 여러 재료를 넣어 말아 만든 음식입니다."
        },
        {
            "name": "잡채",
            "type": "밥과 식사",
            "description": "당면과 채소 등을 볶아 만든 음식입니다."
        },
        {
            "name": "칼국수",
            "type": "면 요리",
            "description": "밀가루 반죽을 썰어 국물에 끓인 면 요리입니다."
        },
        {
            "name": "떡볶이",
            "type": "간식",
            "description": "떡에 양념을 넣고 조리한 한국의 대표적인 간식입니다."
        },
        {
            "name": "삼계탕",
            "type": "매운 음식이 아닌 음식",
            "description": "닭과 여러 재료를 넣고 끓인 국물 음식입니다."
        }
    ]

    if food_type == "전체":
        selected_foods = foods
    elif food_type == "매운 음식이 아닌 음식":
        selected_foods = [
            food for food in foods
            if food["type"] == "매운 음식이 아닌 음식"
            or food["name"] in ["불고기", "잡채", "칼국수", "비빔밥"]
        ]
    else:
        selected_foods = [
            food for food in foods
            if food["type"] == food_type
        ]

    for food in selected_foods:
        st.subheader(food["name"])
        st.write(food["description"])
        st.divider()

    st.caption("음식의 재료와 알레르기 유발 성분은 주문 전에 확인하세요.")

elif menu == "한국 관광지 추천":
    st.header("한국 관광지 추천")
    st.write("지역을 선택하면 방문할 만한 장소를 소개합니다.")

    region = st.selectbox(
        "지역 선택",
        ["서울", "부산", "제주도", "경주"]
    )

    places = {
        "서울": [
            ("경복궁", "한국의 전통 건축과 궁궐 문화를 살펴볼 수 있습니다."),
            ("남산서울타워", "서울의 도시 풍경을 감상할 수 있습니다."),
            ("인사동", "전통 공예품과 한국 문화를 경험할 수 있습니다.")
        ],
        "부산": [
            ("해운대해수욕장", "바다 풍경을 즐길 수 있는 해변입니다."),
            ("감천문화마을", "다양한 색상의 건물과 예술 작품을 볼 수 있습니다."),
            ("자갈치시장", "부산의 해산물과 시장 문화를 경험할 수 있습니다.")
        ],
        "제주도": [
            ("성산일출봉", "화산 활동으로 형성된 자연 명소입니다."),
            ("한라산", "제주도의 대표적인 산입니다."),
            ("협재해수욕장", "맑은 바다와 해변 풍경을 감상할 수 있습니다.")
        ],
        "경주": [
            ("불국사", "한국의 역사와 불교 문화를 알아볼 수 있습니다."),
            ("첨성대", "신라 시대의 천문 관측 시설로 알려져 있습니다."),
            ("대릉원", "신라 시대의 고분을 살펴볼 수 있는 역사 유적지입니다.")
        ]
    }

    for name, description in places[region]:
        st.subheader(name)
        st.write(description)
        st.divider()

st.sidebar.divider()
st.sidebar.caption("한국 생활에 필요한 정보를 쉽게 알아보세요.")
