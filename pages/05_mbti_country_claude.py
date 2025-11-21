import streamlit as st
import pandas as pd
import altair as alt

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

# 사이드바에 MBTI 선택
st.sidebar.header("⚙️ 설정")
selected_mbti = st.sidebar.selectbox(
    "MBTI 유형을 선택하세요:",
    mbti_types,
    index=mbti_types.index('INFP')  # 기본값: INFP
)

# 선택된 MBTI에 대한 설명
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

# 하위 10개 국가 데이터
bottom_10 = df.nsmallest(10, selected_mbti)[['Country', selected_mbti]].reset_index(drop=True)
bottom_10['Rank'] = range(1, 11)

# 상위 10개 국가 그래프
st.subheader(f"📊 {selected_mbti} 비율이 가장 높은 10개 국가")

chart_top = alt.Chart(top_10).mark_bar().encode(
    x=alt.X(f'{selected_mbti}:Q', 
            title=f'{selected_mbti} 비율',
            axis=alt.Axis(format='%'),
            scale=alt.Scale(domain=[0, top_10[selected_mbti].max() * 1.1])),
    y=alt.Y('Country:N', 
            sort='-x',
            title='국가'),
    color=alt.Color(f'{selected_mbti}:Q',
                    scale=alt.Scale(scheme='blues'),
                    legend=None),
    tooltip=[
        alt.Tooltip('Rank:Q', title='순위'),
        alt.Tooltip('Country:N', title='국가'),
        alt.Tooltip(f'{selected_mbti}:Q', title=f'{selected_mbti} 비율', format='.2%')
    ]
).properties(
    height=400
).configure_mark(
    opacity=0.8
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).interactive()

st.altair_chart(chart_top, use_container_width=True)

st.markdown("---")

# 하위 10개 국가 그래프
st.subheader(f"📉 {selected_mbti} 비율이 가장 낮은 10개 국가")

# 인터랙티브한 선택 기능 추가
selection = alt.selection_point(fields=['Country'], on='mouseover', nearest=True)

chart_bottom = alt.Chart(bottom_10).mark_bar().encode(
    x=alt.X(f'{selected_mbti}:Q', 
            title=f'{selected_mbti} 비율',
            axis=alt.Axis(format='%'),
            scale=alt.Scale(domain=[0, bottom_10[selected_mbti].max() * 1.1])),
    y=alt.Y('Country:N', 
            sort='x',
            title='국가'),
    color=alt.condition(
        selection,
        alt.Color(f'{selected_mbti}:Q',
                  scale=alt.Scale(scheme='oranges'),
                  legend=None),
        alt.value('lightgray')
    ),
    opacity=alt.condition(selection, alt.value(1.0), alt.value(0.5)),
    tooltip=[
        alt.Tooltip('Rank:Q', title='순위'),
        alt.Tooltip('Country:N', title='국가'),
        alt.Tooltip(f'{selected_mbti}:Q', title=f'{selected_mbti} 비율', format='.2%')
    ]
).add_params(
    selection
).properties(
    height=400
).configure_mark(
    opacity=0.8
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).interactive()

st.altair_chart(chart_bottom, use_container_width=True)

# 데이터 테이블 (옵션)
with st.expander("📋 상세 데이터 보기"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**상위 10개 국가**")
        st.dataframe(
            top_10.style.format({selected_mbti: '{:.2%}'}),
            hide_index=True,
            use_container_width=True
        )
    
    with col2:
        st.markdown("**하위 10개 국가**")
        st.dataframe(
            bottom_10.style.format({selected_mbti: '{:.2%}'}),
            hide_index=True,
            use_container_width=True
        )

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <small>💡 마우스를 그래프 위에 올려보세요. 하위 10개 그래프는 마우스를 올리면 하이라이트됩니다.</small>
    </div>
    """,
    unsafe_allow_html=True
)
