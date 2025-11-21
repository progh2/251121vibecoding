import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 기본 세팅
# =========================
st.set_page_config(
    page_title="MBTI 기반 프로그래밍 언어 추천",
    page_icon="💻",
    layout="centered"
)

# =========================
# 데이터 불러오기 (pandas)
# =========================
CSV_PATH = "Popularity_of_Programming_Languages_from_2004_to_2024.csv"

@st.cache_data
def load_language_popularity(path: str):
    df = pd.read_csv(path)
    # 'July 2004' 같은 형식 → datetime
    df["Date"] = pd.to_datetime(df["Date"], format="%B %Y")
    df = df.sort_values("Date")
    return df

try:
    popularity_df = load_language_popularity(CSV_PATH)
    data_loaded = True
except Exception as e:
    popularity_df = None
    data_loaded = False
    st.error(f"언어 인기 데이터(CSV)를 불러오는 중 오류가 발생했어요 😢\n\n에러: {e}")

# =========================
# MBTI → 언어 매핑 (이전 버전 + 약간 리팩토링)
# =========================
mbti_to_language = {
    "INTJ": {
        "display": "Rust 🦀",
        "col": "Rust",
        "tagline": "완벽주의 전략가에게 어울리는 안정성과 성능!",
        "reason": [
            "메모리 안전성, 고성능 등 '깔끔한 설계'를 좋아하는 타입과 잘 맞아요.",
            "복잡한 시스템을 설계하고 최적화하는 데 큰 재미를 느낄 수 있어요.",
        ],
    },
    "INTP": {
        "display": "Haskell 🧠",
        "col": "Haskell",
        "tagline": "개념 덕후 논리왕에게 어울리는 함수형 언어!",
        "reason": [
            "수학적 사고, 추상화, 우아한 코드에 매력을 느끼는 타입에게 찰떡.",
            "현실보다는 개념과 구조를 탐구하는 걸 좋아한다면 잘 맞는 언어예요.",
        ],
    },
    "ENTJ": {
        "display": "Java ☕",
        "col": "Java",
        "tagline": "리더십 있는 기획·관리형에게 어울리는 산업 표준 언어!",
        "reason": [
            "대규모 서비스, 기업용 시스템 등 '현실에서 강한' 언어.",
            "팀 프로젝트, 아키텍처 설계, 역할 분담이 중요한 환경과 잘 맞아요.",
        ],
    },
    "ENTP": {
        "display": "JavaScript ⚡",
        "col": "JavaScript",
        "tagline": "아이디어 폭발, 실험 정신 가득한 타입에게 어울리는 웹의 언어!",
        "reason": [
            "프론트엔드부터 백엔드까지, 브라우저만 있으면 뭐든 실험 가능.",
            "새로운 프레임워크와 기술을 만지는 걸 좋아한다면 최고의 놀이터!",
        ],
    },
    "INFJ": {
        "display": "Python 🐍",
        "col": "Python",
        "tagline": "사람과 세상을 돕고 싶은 이상주의자에게 어울리는 친절한 언어!",
        "reason": [
            "문법이 직관적이라, 문제 해결 아이디어에 집중하기 좋아요.",
            "데이터 분석, AI, 교육용 등 '사람에게 도움 되는 분야'에 강점.",
        ],
    },
    "INFP": {
        "display": "Python 🐍",
        "col": "Python",
        "tagline": "감성 넘치는 크리에이터에게 어울리는 따뜻한 첫 언어!",
        "reason": [
            "간단한 문법으로 나만의 앱, 봇, 도구를 금방 만들 수 있어요.",
            "자유로운 실험과 취미 프로젝트에 딱 맞는 분위기의 언어예요.",
        ],
    },
    "ENFJ": {
        "display": "Kotlin 💜",
        "col": "Kotlin",
        "tagline": "함께 성장하고 싶은 리더형에게 어울리는 모던 안드로이드 언어!",
        "reason": [
            "안드로이드 앱 개발의 핵심 언어로, 사람들에게 직접 가치를 줄 수 있어요.",
            "깔끔한 문법으로 팀 협업과 코드 리뷰에도 강점이 있어요.",
        ],
    },
    "ENFP": {
        "display": "JavaScript 🌈",
        "col": "JavaScript",
        "tagline": "아이디어 부자, 즉흥적인 실험러에게 딱 맞는 웹 언어!",
        "reason": [
            "웹 페이지, 게임, 인터랙티브 아트 등 무엇이든 빠르게 만들어볼 수 있어요.",
            "결과가 바로 브라우저에 보이니 동기부여도 💯.",
        ],
    },
    "ISTJ": {
        "display": "C 🧱",
        "col": "C/C++",  # 데이터는 'C/C++' 컬럼으로 들어있음
        "tagline": "원칙과 구조를 중시하는 관리자형에게 어울리는 기본기 끝판왕!",
        "reason": [
            "운영체제, 임베디드 등 컴퓨터의 바닥부터 이해할 수 있어요.",
            "탄탄한 기본기를 쌓고 싶은 타입에게 최고의 훈련 언어.",
        ],
    },
    "ISFJ": {
        "display": "Python 🤝",
        "col": "Python",
        "tagline": "성실하고 배려 깊은 조력자형에게 어울리는 안정적인 언어!",
        "reason": [
            "교육, 자동화 스크립트, 실무 보조 도구 등에 잘 쓰이는 실용적인 언어예요.",
            "팀에서 '묵묵히 잘 돌아가게 만드는 사람'이 되고 싶다면 추천!",
        ],
    },
    "ESTJ": {
        "display": "C# 🏗️",
        "col": "C#",
        "tagline": "체계적인 조직가형에게 어울리는 윈도우·게임·백엔드 만능 언어!",
        "reason": [
            "엔터프라이즈 개발, 데스크톱, 게임(유니티) 등 현업에서 강력.",
            "도구와 프레임워크가 잘 정리되어 있어 관리형 성향과 잘 맞아요.",
        ],
    },
    "ESFJ": {
        "display": "TypeScript 🤗",
        "col": "TypeScript",
        "tagline": "협업과 커뮤니케이션을 중시하는 타입에게 어울리는 안전한 JS!",
        "reason": [
            "팀 프로젝트에서 실수 줄이고, 읽기 쉬운 코드를 쓰는 데 큰 도움.",
            "프론트엔드 협업 환경에서 빛나는 언어예요.",
        ],
    },
    "ISTP": {
        "display": "C++ 🛠️",
        "col": "C/C++",  # 동일 컬럼 사용
        "tagline": "손으로 만지고 튜닝하는 걸 좋아하는 장인형에게 어울리는 언어!",
        "reason": [
            "게임 엔진, 고성능 앱, 하드웨어 가까운 영역에 강해요.",
            "최적화와 성능 튜닝에서 '직접 만지는 손맛'을 느낄 수 있어요.",
        ],
    },
    "ISFP": {
        "display": "Swift 🎨",
        "col": "Swift",
        "tagline": "감성적인 아티스트형에게 어울리는 iOS·macOS 앱 언어!",
        "reason": [
            "디자인 감성을 살린 iOS 앱을 만드는 데 최적.",
            "Apple 생태계에서 깔끔하고 예쁜 결과물을 만들 수 있어요.",
        ],
    },
    "ESTP": {
        "display": "Go 🚀",
        "col": "Go",
        "tagline": "직설적이고 실행력 강한 타입에게 어울리는 단순·고속 언어!",
        "reason": [
            "문법이 단순해서 바로 서버 만들고 성능 테스트 해볼 수 있어요.",
            "클라우드·백엔드·인프라 쪽에서 특히 강력한 언어예요.",
        ],
    },
    "ESFP": {
        "display": "JavaScript 🎉",
        "col": "JavaScript",
        "tagline": "무대 체질 엔터테이너형에게 어울리는 화려한 인터랙션 언어!",
        "reason": [
            "애니메이션, 이펙트, 인터랙티브 웹 등 즐거운 결과물 위주로 배우기 좋아요.",
            "사람들 반응을 바로 볼 수 있어 즐겁게 개발할 수 있어요.",
        ],
    },
}

language_summary = [
    {
        "언어": "Python 🐍",
        "느낌": "친절, 만능, 입문용 최고",
        "난이도(체감)": "★☆☆",
        "잘 맞는 성향": "차분, 사람 중심, 아이디어 구현",
    },
    {
        "언어": "JavaScript ⚡",
        "느낌": "즉흥, 실험, 웹의 왕",
        "난이도(체감)": "★★☆",
        "잘 맞는 성향": "아이디어 폭발, 눈에 보이는 결과 선호",
    },
    {
        "언어": "TypeScript 📘",
        "느낌": "안전한 JavaScript",
        "난이도(체감)": "★★☆",
        "잘 맞는 성향": "협업, 구조, 안정성 중시",
    },
    {
        "언어": "Java ☕",
        "느낌": "전통 강자, 기업용 표준",
        "난이도(체감)": "★★★",
        "잘 맞는 성향": "리더십, 큰 그림, 안정적인 커리어",
    },
    {
        "언어": "C 🧱",
        "느낌": "저수준, 탄탄한 기본기",
        "난이도(체감)": "★★★",
        "잘 맞는 성향": "원리파, 시스템 깊게 이해하고 싶은 타입",
    },
    {
        "언어": "C++ 🛠️",
        "느낌": "고성능, 게임·엔진",
        "난이도(체감)": "★★★☆",
        "잘 맞는 성향": "튜닝, 성능, 하드코어 개발자 지망",
    },
    {
        "언어": "C# 🎮",
        "느낌": "윈도우, 게임, 백엔드 만능",
        "난이도(체감)": "★★☆",
        "잘 맞는 성향": "체계적, 도구 친화, 유니티 관심",
    },
    {
        "언어": "Swift 🍎",
        "느낌": "iOS, Apple 감성",
        "난이도(체감)": "★★☆",
        "잘 맞는 성향": "디자인·UX, 예쁜 결과물 선호",
    },
    {
        "언어": "Go 🚀",
        "느낌": "단순, 빠름, 서버·클라우드",
        "난이도(체감)": "★★☆",
        "잘 맞는 성향": "실행력, 인프라, 깔끔한 문법 선호",
    },
    {
        "언어": "Rust 🦀",
        "느낌": "메모리 안전, 고성능",
        "난이도(체감)": "★★★★",
        "잘 맞는 성향": "완벽주의, 안정성 집착, 시스템 개발",
    },
    {
        "언어": "Kotlin 💜",
        "느낌": "모던, 안드로이드, 깔끔",
        "난이도(체감)": "★★☆",
        "잘 맞는 성향": "안드로이드 앱, 협업, 최신 문법 선호",
    },
    {
        "언어": "Haskell 🧠",
        "느낌": "함수형, 개념 덕후 전용",
        "난이도(체감)": "★★★★",
        "잘 맞는 성향": "수학, 추상화, 논리 퍼즐 애호가",
    },
]

# =========================
# UI 헤더
# =========================
st.markdown(
    """
    <h1 style="text-align:center;">
        🔮 MBTI로 보는 첫 프로그래밍 언어 추천소 💻
    </h1>
    <p style="text-align:center; color:gray;">
        주니어 프로그래머를 위한 &lt;MBTI x Language&gt; 매칭 가이드 🚀 + 실제 인기 데이터 📈
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =========================
# MBTI 선택 영역
# =========================
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1️⃣ 내 MBTI 선택하기")
    mbti_list = sorted(mbti_to_language.keys())
    selected_mbti = st.selectbox(
        "학생의 MBTI를 골라줘요:",
        mbti_list,
        index=mbti_list.index("INFJ") if "INFJ" in mbti_list else 0,
        help="16가지 MBTI 중 하나를 선택하면, 그 타입에 어울리는 언어를 추천해줘요!",
    )

with col2:
    st.subheader("2️⃣ 어떤 앱인가요? 🤔")
    st.markdown(
        """
        - MBTI별로 **첫 프로그래밍 언어**를 추천해주는 웹앱이에요.
        - 게다가, 실제 **2004~2024년 언어 인기 데이터**까지 같이 보여줘요.  
        - 아래에는 **다른 언어들도 한눈에 보는 요약 테이블**이 나와요.
        """
    )

st.divider()

# =========================
# 추천 결과 카드
# =========================
info = mbti_to_language[selected_mbti]

st.markdown(f"### 🎯 {selected_mbti} 타입에게 어울리는 언어는 바로…")
st.markdown(
    f"""
    <div style="
        border-radius: 16px;
        padding: 16px 20px;
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        margin-bottom: 10px;
    ">
        <h2 style="margin:0; font-size: 1.6rem;">🏆 {info['display']}</h2>
        <p style="margin-top:4px; color:#e5e7eb;">{info['tagline']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### 💡 왜 이 언어가 잘 맞을까요?")
for r in info["reason"]:
    st.markdown(f"- {r}")

st.caption("※ MBTI는 재미로 보는 가이드일 뿐, 어떤 언어든 충분히 잘할 수 있어요 😉")

st.divider()

# =========================
# Plotly로 추천 언어 인기 그래프 그리기
# =========================
st.markdown("## 📈 추천 언어의 실제 인기 추이 (2004~2024)")

if data_loaded:
    lang_col = info["col"]
    if lang_col not in popularity_df.columns:
        st.warning(
            f"🙇‍♂️ 죄송! 현재 CSV 데이터에 **{lang_col}** 컬럼이 없어서 그래프를 그릴 수 없어요."
        )
    else:
        df_lang = popularity_df[["Date", lang_col]].dropna()

        # 요약 정보 계산
        latest_row = df_lang.iloc[-1]
        latest_date = latest_row["Date"]
        latest_value = latest_row[lang_col]

        peak_idx = df_lang[lang_col].idxmax()
        peak_row = df_lang.loc[peak_idx]
        peak_date = peak_row["Date"]
        peak_value = peak_row[lang_col]

        start_value = df_lang.iloc[0][lang_col]
        change = latest_value - start_value

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="📍 최신 인기 지수(%)",
                value=f"{latest_value:.2f}",
                help=f"{latest_date.strftime('%Y-%m')} 기준 값",
            )
        with c2:
            st.metric(
                label="🏔️ 최고 인기 지수(%)",
                value=f"{peak_value:.2f}",
                help=f"{peak_date.strftime('%Y-%m')} 에 최고치 기록",
            )
        with c3:
            st.metric(
                label="📊 2004 → 최신 변화량",
                value=f"{change:+.2f}p",
                help="첫 데이터 시점과 비교한 변화량",
            )

        # Plotly 라인 그래프
        fig = px.line(
            df_lang,
            x="Date",
            y=lang_col,
            title=f"{info['display']} 인기 추이",
            labels={"Date": "연도", lang_col: "인기 지수(%)"},
        )
        fig.update_layout(
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "※ 데이터는 제공된 CSV 기준이며, 값은 상대적인 **인기 지수(%)**로 보면 돼요."
        )
else:
    st.info("CSV를 불러올 수 없어서 그래프를 표시하지 못했어요. 파일 경로와 이름을 다시 확인해 주세요 😭")

st.divider()

# =========================
# 언어 요약 테이블
# =========================
st.markdown("## 📚 다른 프로그래밍 언어 한눈에 보기")
st.markdown("주니어 프로그래머용 **언어 분위기·난이도 요약 테이블**이에요:")

st.dataframe(
    language_summary,
    use_container_width=True,
    hide_index=True,
)

st.markdown(
    """
    > ⚠️ 난이도는 '체감 난이도' 기준으로 아주 대략적인 느낌입니다.  
    > 학생의 흥미와 목표가 가장 중요하니, **하고 싶은 언어부터 파고드는 것**도 완전 추천해요! 🌱
    """
)

# 이스터에그
with st.expander("🎈 오늘도 코딩하기 딱 좋은 날! (눌러보기)"):
    st.write("당신의 첫 언어가 어떤 것이든, **꾸준함이 곧 치트키**입니다. 천천히, 하지만 멈추지 말기! 🧑‍💻✨")

st.balloons()
