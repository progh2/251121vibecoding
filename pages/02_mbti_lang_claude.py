import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 프로그래밍 언어 추천",
    page_icon="💻",
    layout="centered"
)

# MBTI별 프로그래밍 언어 추천 데이터
mbti_languages = {
    "ISTJ": {
        "language": "Java ☕",
        "emoji": "📋",
        "reason": "체계적이고 신뢰성 있는 당신에게 딱! 엔터프라이즈급 안정성과 명확한 구조를 자랑합니다.",
        "traits": "철저함 • 책임감 • 규칙 준수",
        "color": "#5382a1"
    },
    "ISFJ": {
        "language": "Python 🐍",
        "emoji": "💝",
        "reason": "섬세하고 배려심 많은 당신을 위한 언어! 읽기 쉽고 배우기 쉬워 모두를 배려합니다.",
        "traits": "친절함 • 세심함 • 헌신",
        "color": "#3776ab"
    },
    "INFJ": {
        "language": "JavaScript 🌐",
        "emoji": "🔮",
        "reason": "통찰력 있는 당신에게 완벽! 웹의 미래를 창조하며 깊은 의미를 담을 수 있습니다.",
        "traits": "직관력 • 창의성 • 이상주의",
        "color": "#f7df1e"
    },
    "INTJ": {
        "language": "C++ 🚀",
        "emoji": "🧠",
        "reason": "전략적이고 독립적인 당신의 선택! 최고의 성능과 완벽한 통제력을 제공합니다.",
        "traits": "논리적 • 혁신적 • 독립적",
        "color": "#00599c"
    },
    "ISTP": {
        "language": "Rust 🦀",
        "emoji": "🔧",
        "reason": "실용적이고 분석적인 당신에게 딱! 메모리 안전성과 높은 성능을 동시에 잡았습니다.",
        "traits": "실용성 • 기술적 • 유연함",
        "color": "#ce422b"
    },
    "ISFP": {
        "language": "Swift 🍎",
        "emoji": "🎨",
        "reason": "예술적이고 자유로운 당신의 캔버스! 아름답고 직관적인 iOS 앱을 만들어보세요.",
        "traits": "창의력 • 유연성 • 감성",
        "color": "#fa7343"
    },
    "INFP": {
        "language": "Ruby 💎",
        "emoji": "🌸",
        "reason": "이상주의적이고 창의적인 당신을 위한 언어! 개발자의 행복을 최우선으로 합니다.",
        "traits": "상상력 • 진정성 • 열정",
        "color": "#cc342d"
    },
    "INTP": {
        "language": "Haskell 🎓",
        "emoji": "🔬",
        "reason": "논리적이고 혁신적인 당신의 놀이터! 순수 함수형 프로그래밍의 정수를 경험하세요.",
        "traits": "분석력 • 호기심 • 논리성",
        "color": "#5e5086"
    },
    "ESTP": {
        "language": "Go 🏃",
        "emoji": "⚡",
        "reason": "행동파인 당신에게 최고! 빠르고 간결하며 즉각적인 결과를 보여줍니다.",
        "traits": "실행력 • 적응력 • 모험심",
        "color": "#00add8"
    },
    "ESFP": {
        "language": "PHP 🎭",
        "emoji": "🎉",
        "reason": "사교적이고 즐거움을 추구하는 당신! 웹 개발의 즐거움을 느껴보세요.",
        "traits": "사교성 • 즐거움 • 현실감각",
        "color": "#777bb4"
    },
    "ENFP": {
        "language": "JavaScript 🌈",
        "emoji": "✨",
        "reason": "열정적이고 창의적인 당신의 무한한 가능성! 프론트엔드부터 백엔드까지 자유롭게!",
        "traits": "열정 • 창의력 • 자유로움",
        "color": "#f7df1e"
    },
    "ENTP": {
        "language": "Scala 🎯",
        "emoji": "🧩",
        "reason": "도전적이고 혁신적인 당신! 객체지향과 함수형의 완벽한 조합을 마스터하세요.",
        "traits": "창의성 • 논쟁력 • 도전정신",
        "color": "#dc322f"
    },
    "ESTJ": {
        "language": "C# 🏢",
        "emoji": "📊",
        "reason": "실용적이고 조직적인 당신의 파트너! 강력한 .NET 생태계와 함께합니다.",
        "traits": "효율성 • 조직력 • 결단력",
        "color": "#239120"
    },
    "ESFJ": {
        "language": "TypeScript 🤝",
        "emoji": "💼",
        "reason": "협력적이고 책임감 있는 당신! 팀 프로젝트에서 빛을 발하는 안전한 JavaScript입니다.",
        "traits": "협동심 • 배려심 • 조화",
        "color": "#3178c6"
    },
    "ENFJ": {
        "language": "Python 🌟",
        "emoji": "🎤",
        "reason": "리더십과 공감능력을 가진 당신! 모두가 이해하기 쉬운 코드로 팀을 이끌어보세요.",
        "traits": "리더십 • 공감력 • 카리스마",
        "color": "#3776ab"
    },
    "ENTJ": {
        "language": "Kotlin ⚔️",
        "emoji": "👑",
        "reason": "리더십과 효율성을 겸비한 당신! 현대적이고 강력한 안드로이드 개발의 왕자입니다.",
        "traits": "전략적 • 목표지향적 • 효율성",
        "color": "#7f52ff"
    }
}

# 헤더
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .result-card {
        padding: 2rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .trait-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.3);
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
    }
    .stSelectbox {
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>💻 MBTI 프로그래밍 언어 추천 🚀</h1>
        <p>당신의 성격 유형에 딱 맞는 프로그래밍 언어를 찾아드려요!</p>
    </div>
""", unsafe_allow_html=True)

# 메인 컨텐츠
st.markdown("### 🎯 당신의 MBTI를 선택해주세요")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    mbti_types = list(mbti_languages.keys())
    selected_mbti = st.selectbox(
        "MBTI 유형",
        options=["선택해주세요"] + mbti_types,
        index=0,
        help="자신의 MBTI 유형을 선택하세요 😊"
    )

# 결과 표시
if selected_mbti != "선택해주세요":
    data = mbti_languages[selected_mbti]
    
    st.markdown("---")
    
    # 결과 카드
    st.markdown(f"""
        <div class="result-card">
            <h2 style="text-align: center; font-size: 3rem;">{data['emoji']}</h2>
            <h1 style="text-align: center; margin: 1rem 0;">{selected_mbti} 유형</h1>
            <h2 style="text-align: center; font-size: 2.5rem; margin: 1.5rem 0;">{data['language']}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 추천 이유
    st.markdown("### 💡 추천 이유")
    st.info(data['reason'])
    
    # 성격 특성
    st.markdown("### ✨ 당신의 강점")
    traits = data['traits'].split(' • ')
    cols = st.columns(len(traits))
    for i, trait in enumerate(traits):
        with cols[i]:
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                border-radius: 10px; margin: 0.5rem 0;">
                    <strong>{trait}</strong>
                </div>
            """, unsafe_allow_html=True)
    
    # 시작 버튼
    st.markdown("---")
    st.markdown("### 🚀 다음 단계")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #e3f2fd; border-radius: 10px;">
                <h4>📚 학습 시작</h4>
                <p>온라인 강의로<br>기초부터!</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #f3e5f5; border-radius: 10px;">
                <h4>💻 실습 프로젝트</h4>
                <p>간단한 프로젝트로<br>실력 향상!</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; background: #e8f5e9; border-radius: 10px;">
                <h4>🤝 커뮤니티</h4>
                <p>개발자 모임에<br>참여하기!</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.success("🎉 당신의 개발 여정을 응원합니다!")

else:
    # 초기 화면 안내
    st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
        border-radius: 15px; margin: 2rem 0;">
            <h2>🎨 어떻게 사용하나요?</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0;">
                1️⃣ 위에서 당신의 MBTI 유형을 선택하세요<br>
                2️⃣ 맞춤형 프로그래밍 언어 추천을 받으세요<br>
                3️⃣ 새로운 개발 여정을 시작하세요!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # MBTI 그리드 미리보기
    st.markdown("### 🌈 모든 MBTI 유형 미리보기")
    
    cols = st.columns(4)
    for idx, mbti in enumerate(mbti_types):
        with cols[idx % 4]:
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; border-radius: 10px; margin: 0.5rem 0;">
                    <h4>{mbti}</h4>
                    <p style="font-size: 2rem; margin: 0.5rem 0;">{mbti_languages[mbti]['emoji']}</p>
                    <small>{mbti_languages[mbti]['language']}</small>
                </div>
            """, unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>💝 Made with Streamlit | 당신의 꿈을 응원합니다 🚀</p>
        <small>※ 이 추천은 재미와 영감을 위한 것입니다. 모든 언어는 배울 가치가 있어요!</small>
    </div>
""", unsafe_allow_html=True)
