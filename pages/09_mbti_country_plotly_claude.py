import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="MBTI 국가별 분포",
    page_icon="🌍",
    layout="wide"
)

# 타이틀
st.title("🌍 국가별 MBTI 유형 분포 분석")
st.markdown("---")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

df = load_data()

# MBTI 유형 목록 (Country 컬럼 제외)
mbti_types = df.columns[1:].tolist()

# MBTI 유형별 설명
mbti_descriptions = {
    'INFJ': '내향적, 직관적, 감정적, 판단적 - 용기있는 수호자',
    'ISFJ': '내향적, 감각적, 감정적, 판단적 - 수호자',
    'INTP': '내향적, 직관적, 사고적, 인식적 - 논리적인 사색가',
    'ISFP': '내향적, 감각적, 감정적, 인식적 - 호기심 많은 예술가',
    'ENTP': '외향적, 직관적, 사고적, 인식적 - 논쟁을 즐기는 변론가',
    'INFP': '내향적, 직관적, 감정적, 인식적 - 열정적인 중재자',
    'ENTJ': '외향적, 직관적, 사고적, 판단적 - 대담한 통솔자',
    'ISTP': '내향적, 감각적, 사고적, 인식적 - 만능 재주꾼',
    'INTJ': '내향적, 직관적, 사고적, 판단적 - 용의주도한 전략가',
    'ESFP': '외향적, 감각적, 감정적, 인식적 - 자유로운 영혼의 연예인',
    'ESTJ': '외향적, 감각적, 사고적, 판단적 - 엄격한 관리자',
    'ENFP': '외향적, 직관적, 감정적, 인식적 - 재기발랄한 활동가',
    'ESTP': '외향적, 감각적, 사고적, 인식적 - 모험을 즐기는 사업가',
    'ISTJ': '내향적, 감각적, 사고적, 판단적 - 청렴결백한 논리주의자',
    'ENFJ': '외향적, 직관적, 감정적, 판단적 - 정의로운 사회운동가',
    'ESFJ': '외향적, 감각적, 감정적, 판단적 - 사교적인 외교관'
}

# 사이드바에 MBTI 선택
st.sidebar.header("⚙️ 설정")
selected_mbti = st.sidebar.selectbox(
    "MBTI 유형을 선택하세요:",
    mbti_types,
    index=mbti_types.index('INFP')  # 기본값: INFP
)

# 선택된 MBTI에 대한 설명
st.sidebar.info(f"**{selected_mbti}**\n\n{mbti_descriptions.get(selected_mbti, '')}")

# 통계 정보
col1, col2, col3 = st.columns(3)
with col1:
    avg_value = df[selected_mbti].mean()
    st.metric("전 세계 평균 비율", f"{avg_value:.2%}")
with col2:
    max_country = df.loc[df[selected_mbti].idxmax(), 'Country']
    max_value = df[selected_mbti].max()
    st.metric("최고 비율 국가", max_country, f"{max_value:.2%}")
with col3:
    min_country = df.loc[df[selected_mbti].idxmin(), 'Country']
    min_value = df[selected_mbti].min()
    st.metric("최저 비율 국가", min_country, f"{min_value:.2%}")

st.markdown("---")

# 상위 10개 국가 데이터
top_10 = df.nlargest(10, selected_mbti)[['Country', selected_mbti]].reset_index(drop=True)
top_10['Rank'] = range(1, 11)
top_10 = top_10.sort_values(selected_mbti, ascending=True)  # Plotly 가로 막대를 위해 오름차순

# 상위 10개 국가 그래프
st.subheader(f"📊 {selected_mbti} 비율이 가장 높은 10개 국가")

fig_top = px.bar(
    top_10,
    x=selected_mbti,
    y='Country',
    orientation='h',
    title=f'{selected_mbti} 비율 상위 10개 국가',
    labels={selected_mbti: f'{selected_mbti} 비율', 'Country': '국가'},
    color=selected_mbti,
    color_continuous_scale='Blues',
    hover_data={
        'Rank': True,
        'Country': True,
        selected_mbti: ':.2%'
    }
)

fig_top.update_layout(
    height=500,
    showlegend=False,
    xaxis_title=f'{selected_mbti} 비율',
    yaxis_title='국가',
    xaxis_tickformat='.0%',
    hovermode='closest',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

fig_top.update_traces(
    hovertemplate='<b>%{y}</b><br>비율: %{x:.2%}<extra></extra>'
)

st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# 하위 10개 국가 데이터
bottom_10 = df.nsmallest(10, selected_mbti)[['Country', selected_mbti]].reset_index(drop=True)
bottom_10['Rank'] = range(1, 11)
bottom_10 = bottom_10.sort_values(selected_mbti, ascending=True)  # Plotly 가로 막대를 위해 오름차순

# 하위 10개 국가 그래프 (인터랙티브)
st.subheader(f"📉 {selected_mbti} 비율이 가장 낮은 10개 국가")

fig_bottom = px.bar(
    bottom_10,
    x=selected_mbti,
    y='Country',
    orientation='h',
    title=f'{selected_mbti} 비율 하위 10개 국가 (인터랙티브)',
    labels={selected_mbti: f'{selected_mbti} 비율', 'Country': '국가'},
    color=selected_mbti,
    color_continuous_scale='Oranges',
    hover_data={
        'Rank': True,
        'Country': True,
        selected_mbti: ':.2%'
    }
)

fig_bottom.update_layout(
    height=500,
    showlegend=False,
    xaxis_title=f'{selected_mbti} 비율',
    yaxis_title='국가',
    xaxis_tickformat='.0%',
    hovermode='closest',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

fig_bottom.update_traces(
    hovertemplate='<b>%{y}</b><br>비율: %{x:.2%}<extra></extra>'
)

st.plotly_chart(fig_bottom, use_container_width=True)

# 데이터 테이블 (옵션)
with st.expander("📋 상세 데이터 보기"):
    col1, col2 = st.columns(2)
    
    # 다시 내림차순으로 정렬하여 표시
    top_10_display = df.nlargest(10, selected_mbti)[['Country', selected_mbti]].reset_index(drop=True)
    top_10_display.index = range(1, 11)
    
    bottom_10_display = df.nsmallest(10, selected_mbti)[['Country', selected_mbti]].reset_index(drop=True)
    bottom_10_display.index = range(1, 11)
    
    with col1:
        st.markdown("**상위 10개 국가**")
        st.dataframe(
            top_10_display.style.format({selected_mbti: '{:.2%}'}),
            use_container_width=True
        )
    
    with col2:
        st.markdown("**하위 10개 국가**")
        st.dataframe(
            bottom_10_display.style.format({selected_mbti: '{:.2%}'}),
            use_container_width=True
        )

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <small>💡 그래프 위에 마우스를 올리면 상세 정보를 볼 수 있습니다. 확대/축소/이동도 가능합니다!</small>
    </div>
    """,
    unsafe_allow_html=True
)
