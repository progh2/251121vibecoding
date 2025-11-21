import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 국가별 비율 분석 (Plotly)",
    page_icon="📊",
    layout="wide"
)

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        # 같은 폴더에 있는 csv 파일 읽기
        df = pd.read_csv('countriesMBTI_16types.csv')
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("🚨 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다. 같은 폴더에 파일을 넣어주세요.")
    st.stop()

# 3. 헤더 및 사이드바 구성
st.title("📊 MBTI 유형별 국가 순위")
st.markdown("이 대시보드는 **Plotly**를 사용하여 각 MBTI 유형의 국가별 비율을 시각화합니다.")

# MBTI 컬럼 리스트 (첫 번째 'Country' 컬럼 제외)
mbti_options = df.columns[1:].tolist()

with st.sidebar:
    st.header("옵션")
    selected_mbti = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_options)
    st.info(f"현재 선택된 유형: **{selected_mbti}**")

# 4. 데이터 필터링 및 정렬 로직
# 상위 10개국 (비율이 높은 순)
# Plotly bar(h)는 데이터프레임의 순서대로 아래->위로 그립니다.
# 따라서 가장 높은 값이 그래프 상단에 오게 하려면, 값을 오름차순 정렬해야 합니다.
top_10 = df.nlargest(10, selected_mbti).sort_values(by=selected_mbti, ascending=True)

# 하위 10개국 (비율이 낮은 순)
# 가장 낮은 값이 그래프 상단에 오게 하려면, 값을 내림차순 정렬해야 합니다.
bottom_10 = df.nsmallest(10, selected_mbti).sort_values(by=selected_mbti, ascending=False)


# 5. 시각화 (Plotly Express)

# [그래프 1] Top 10 막대 그래프
fig_top = px.bar(
    top_10,
    x=selected_mbti,
    y='Country',
    orientation='h',
    title=f"🏆 {selected_mbti} 비율이 가장 높은 나라 Top 10",
    text_auto='.3%',  # 막대 끝에 퍼센트 표시
    color=selected_mbti, # 값에 따라 색상 진하기 변경
    color_continuous_scale='Blues'
)
fig_top.update_layout(xaxis_title="비율", yaxis_title="국가", height=500)
fig_top.update_traces(textposition='outside') # 텍스트를 막대 바깥으로


# [그래프 2] Bottom 10 막대 그래프 (인터랙티브)
fig_bottom = px.bar(
    bottom_10,
    x=selected_mbti,
    y='Country',
    orientation='h',
    title=f"📉 {selected_mbti} 비율이 가장 낮은 나라 Bottom 10",
    text_auto='.3%',
    color=selected_mbti,
    color_continuous_scale='Reds' # 하위권은 붉은색 계열
)
fig_bottom.update_layout(xaxis_title="비율", yaxis_title="국가", height=500)
fig_bottom.update_traces(textposition='outside')


# 6. 화면 레이아웃 배치
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_top, use_container_width=True)

with col2:
    st.plotly_chart(fig_bottom, use_container_width=True)
    st.caption("※ 그래프 위에 마우스를 올리면 확대/축소 및 상세 정보를 볼 수 있습니다.")

# 데이터 미리보기
with st.expander("📋 전체 데이터 보기"):
    st.dataframe(df)
