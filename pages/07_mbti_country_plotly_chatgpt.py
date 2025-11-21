import pandas as pd
import streamlit as st
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="나라별 MBTI 분포",
    layout="wide"
)

# ======================
# 데이터 로드
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# MBTI 컬럼 목록 (Country 제외)
mbti_cols = [c for c in df.columns if c != "Country"]

# ======================
# UI
# ======================
st.title("나라별 MBTI 분포 시각화 (Plotly 버전)")

st.write(
    """
    MBTI 유형을 선택하면,
    - 그 유형 비율이 **가장 높은 10개 나라**
    - **가장 낮은 10개 나라**
    
    를 각각 막대 그래프로 보여줍니다.  
    Plotly라서 기본적으로 줌/호버/범례 토글 등 인터랙션이 가능합니다.
    """
)

selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_cols)

# ======================
# 선택된 MBTI 기준 상위 / 하위 10개 나라 계산
# ======================
top10 = df.nlargest(10, selected_mbti)[["Country", selected_mbti]].copy()
top10 = top10.sort_values(selected_mbti, ascending=False)

bottom10 = df.nsmallest(10, selected_mbti)[["Country", selected_mbti]].copy()
bottom10 = bottom10.sort_values(selected_mbti, ascending=True)

# ======================
# 상위 10개 나라 막대 그래프 (Plotly)
# ======================
st.subheader(f"📈 {selected_mbti} 비율이 가장 높은 10개 나라")

fig_top = px.bar(
    top10,
    x="Country",
    y=selected_mbti,
    title=f"{selected_mbti} 비율이 높은 10개 나라",
    labels={
        "Country": "Country",
        selected_mbti: f"{selected_mbti} 비율"
    },
    hover_data={
        "Country": True,
        selected_mbti: ":.3f"
    }
)

fig_top.update_layout(
    xaxis_title="Country",
    yaxis_title=f"{selected_mbti} 비율",
    hovermode="x unified"
)

st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# ======================
# 하위 10개 나라 막대 그래프 (인터랙티브)
# ======================
st.subheader(f"📉 {selected_mbti} 비율이 가장 낮은 10개 나라 (인터랙티브)")

fig_bottom = px.bar(
    bottom10,
    x="Country",
    y=selected_mbti,
    title=f"{selected_mbti} 비율이 낮은 10개 나라",
    labels={
        "Country": "Country",
        selected_mbti: f"{selected_mbti} 비율"
    },
    hover_data={
        "Country": True,
        selected_mbti: ":.3f"
    }
)

# 카테고리 정렬 & 약간의 인터랙션 튜닝
fig_bottom.update_layout(
    xaxis_title="Country",
    yaxis_title=f"{selected_mbti} 비율",
    xaxis=dict(categoryorder="total ascending"),
    hovermode="x unified"
)

# 막대에 값 표시 옵션 (원하면 주석 처리 풀어도 됨)
fig_bottom.update_traces(
    hovertemplate="<b>%{x}</b><br>" +
                  selected_mbti + " 비율: %{y:.3f}<extra></extra>"
)

st.plotly_chart(fig_bottom, use_container_width=True)

st.info(
    "그래프 위에서 마우스 휠로 줌, 드래그로 이동, 상단 툴바로 영역 확대/리셋 등이 가능합니다."
)
