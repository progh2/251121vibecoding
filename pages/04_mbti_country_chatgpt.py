import pandas as pd
import streamlit as st
import altair as alt

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
st.title("나라별 MBTI 분포 시각화")

st.write("MBTI 유형을 선택하면, 해당 유형 비율이 **가장 높은 10개 나라**와 "
         "**가장 낮은 10개 나라**를 막대 그래프로 보여줍니다.")

selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_cols)

# ======================
# 선택된 MBTI 기준 상위 / 하위 10개 나라 계산
# ======================
top10 = df.nlargest(10, selected_mbti)[["Country", selected_mbti]].copy()
top10 = top10.rename(columns={selected_mbti: "ratio"})

bottom10 = df.nsmallest(10, selected_mbti)[["Country", selected_mbti]].copy()
bottom10 = bottom10.rename(columns={selected_mbti: "ratio"})

# 값이 0~1 비율이면 퍼센트로 바꿔서 보여주고 싶다면 아래처럼 사용해도 됨
# top10["ratio_percent"] = top10["ratio"] * 100
# bottom10["ratio_percent"] = bottom10["ratio"] * 100

# ======================
# 상위 10개 나라 막대 그래프 (Altair)
# ======================
st.subheader(f"{selected_mbti} 비율이 **가장 높은 10개 나라**")

top_chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X("Country:N", sort="-y", title="Country"),
        y=alt.Y("ratio:Q", title=f"{selected_mbti} 비율"),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("ratio:Q", title="Ratio", format=".3f"),
        ],
    )
    .properties(width=700, height=400)
)

st.altair_chart(top_chart, use_container_width=True)

# ======================
# 하위 10개 나라 막대 그래프 (인터랙티브)
# ======================
st.subheader(f"{selected_mbti} 비율이 **가장 낮은 10개 나라** (인터랙티브)")

# Altair 인터랙션: 클릭해서 강조하는 selection
selection = alt.selection_single(fields=["Country"], on="click", empty="none")

bottom_chart = (
    alt.Chart(bottom10)
    .mark_bar()
    .encode(
        x=alt.X("Country:N", sort="y", title="Country"),
        y=alt.Y("ratio:Q", title=f"{selected_mbti} 비율"),
        color=alt.condition(
            selection,
            alt.value("steelblue"),   # 선택된 막대
            alt.value("lightgray"),   # 선택 안 된 막대
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("ratio:Q", title="Ratio", format=".3f"),
        ],
    )
    .add_selection(selection)
    .properties(width=700, height=400)
    .interactive()  # 줌/팬 등 기본 인터랙션 추가
)

st.altair_chart(bottom_chart, use_container_width=True)
