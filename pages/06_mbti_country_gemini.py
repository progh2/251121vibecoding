import streamlit as st
import pandas as pd
import altair as alt

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 국가별 비율 분석",
    page_icon="🌍",
    layout="wide"
)

# 2. 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    # csv 파일이 같은 폴더에 있다고 가정
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 같은 폴더에 있는지 확인해주세요.")
    st.stop()

# 3. 사이드바 및 헤더 구성
st.title("🌍 MBTI 유형별 국가 분포")
st.markdown("각 MBTI 유형의 비율이 **가장 높은 나라**와 **가장 낮은 나라**를 확인해보세요.")

# MBTI 컬럼 리스트 추출 (첫 번째 컬럼인 'Country' 제외)
mbti_list = df.columns[1:].tolist()

# 사용자 선택 (사이드바)
with st.sidebar:
    st.header("옵션 선택")
    selected_mbti = st.selectbox("확인하고 싶은 MBTI를 선택하세요:", mbti_list)
    st.write(f"선택된 MBTI: **{selected_mbti}**")

# 4. 데이터 필터링 및 정렬
# 상위 10개국 (내림차순 정렬)
top_10 = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)
# 하위 10개국 (오름차순 정렬)
bottom_10 = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=True).head(10)

# 5. Altair 그래프 생성

# [그래프 1] 상위 10개국 (Top 10)
chart_top = alt.Chart(top_10).mark_bar().encode(
    x=alt.X(f'{selected_mbti}:Q', title='비율', axis=alt.Axis(format='%')),
    y=alt.Y('Country:N', sort='-x', title='국가'), # 값에 따라 내림차순 정렬
    color=alt.value('#4c78a8'),  # 파란색 계열
    tooltip=['Country', alt.Tooltip(f'{selected_mbti}:Q', format='.2%')]
).properties(
    title=f"📈 {selected_mbti} 비율이 가장 높은 나라 Top 10",
    height=400
)

# [그래프 2] 하위 10개국 (Bottom 10) - 인터랙티브 설정
chart_bottom = alt.Chart(bottom_10).mark_bar().encode(
    x=alt.X(f'{selected_mbti}:Q', title='비율', axis=alt.Axis(format='%')),
    y=alt.Y('Country:N', sort='x', title='국가'), # 값에 따라 오름차순 정렬
    color=alt.value('#e45756'),  # 붉은색 계열
    tooltip=['Country', alt.Tooltip(f'{selected_mbti}:Q', format='.2%')]
).properties(
    title=f"📉 {selected_mbti} 비율이 가장 낮은 나라 Bottom 10 (확대/축소 가능)",
    height=400
).interactive() # 요청하신 대로 인터랙티브 기능 활성화 (줌/팬)

# 6. 화면 출력
col1, col2 = st.columns(2)

with col1:
    st.altair_chart(chart_top, use_container_width=True)

with col2:
    st.altair_chart(chart_bottom, use_container_width=True)

# 데이터 미리보기 (옵션)
with st.expander("전체 데이터 원본 보기"):
    st.dataframe(df)
