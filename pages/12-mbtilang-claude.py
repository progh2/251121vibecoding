import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="🎯 MBTI 프로그래밍 언어 추천",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# MBTI와 프로그래밍 언어 매칭
MBTI_LANGUAGE_MAP = {
    "INTJ": {
        "language": "Python",
        "icon": "🐍",
        "reason": "전략적이고 분석적인 INTJ는 Python의 명확한 문법과 강력한 데이터 분석 능력에 완벽하게 맞아떨어집니다!",
        "traits": ["전략가", "분석적 사고", "체계적 접근"]
    },
    "ENTP": {
        "language": "JavaScript",
        "icon": "⚡",
        "reason": "창의적이고 혁신적인 ENTP는 JavaScript의 유연성과 빠른 프로토타이핑 능력을 최대한 활용할 수 있습니다!",
        "traits": ["논쟁을 즐김", "창의적", "유연한 사고"]
    },
    "ISTJ": {
        "language": "Java",
        "icon": "☕",
        "reason": "체계적이고 신뢰성 있는 ISTJ는 Java의 안정적인 구조와 엄격한 타입 시스템을 선호합니다!",
        "traits": ["책임감", "체계적", "현실적"]
    },
    "ENFP": {
        "language": "Ruby",
        "icon": "💎",
        "reason": "열정적이고 표현력 풍부한 ENFP는 Ruby의 우아하고 직관적인 문법을 사랑할 것입니다!",
        "traits": ["열정적", "창의적", "표현력 풍부"]
    },
    "ISTP": {
        "language": "C/C++",
        "icon": "🔧",
        "reason": "실용적이고 기술적인 ISTP는 C/C++의 하드웨어 제어와 성능 최적화에 흥미를 느낄 것입니다!",
        "traits": ["실용적", "분석적", "문제 해결사"]
    },
    "ESTJ": {
        "language": "C#",
        "icon": "🎯",
        "reason": "조직적이고 효율적인 ESTJ는 C#의 구조화된 프레임워크와 명확한 설계 패턴을 선호합니다!",
        "traits": ["조직적", "효율적", "리더십"]
    },
    "INFJ": {
        "language": "Python",
        "icon": "🌟",
        "reason": "통찰력 있고 이상주의적인 INFJ는 Python의 읽기 쉬운 코드와 풍부한 라이브러리로 세상을 변화시킬 수 있습니다!",
        "traits": ["통찰력", "이상주의", "창의적"]
    },
    "ENFJ": {
        "language": "TypeScript",
        "icon": "🤝",
        "reason": "카리스마 있고 협업을 중시하는 ENFJ는 TypeScript의 명확한 타입 정의로 팀워크를 강화할 수 있습니다!",
        "traits": ["리더십", "협력적", "열정적"]
    },
    "INFP": {
        "language": "Swift",
        "icon": "🦋",
        "reason": "이상주의적이고 예술적인 INFP는 Swift의 우아한 문법과 아름다운 UI 구현에 매력을 느낄 것입니다!",
        "traits": ["이상주의", "창의적", "열정적"]
    },
    "ESTP": {
        "language": "Go",
        "icon": "🚀",
        "reason": "활동적이고 실행력 있는 ESTP는 Go의 빠른 컴파일과 효율적인 동시성 처리를 즐길 것입니다!",
        "traits": ["행동파", "적응력", "현실적"]
    },
    "INTP": {
        "language": "Rust",
        "icon": "🦀",
        "reason": "논리적이고 혁신적인 INTP는 Rust의 메모리 안전성과 정교한 타입 시스템에 흥미를 느낄 것입니다!",
        "traits": ["논리적", "혁신적", "분석적"]
    },
    "ESFP": {
        "language": "PHP",
        "icon": "🎭",
        "reason": "사교적이고 즉흥적인 ESFP는 PHP의 빠른 웹 개발과 즉각적인 결과물에 만족할 것입니다!",
        "traits": ["사교적", "즉흥적", "활동적"]
    },
    "ISFP": {
        "language": "Dart",
        "icon": "🎨",
        "reason": "예술적이고 유연한 ISFP는 Dart의 아름다운 UI 프레임워크 Flutter로 창의성을 표현할 수 있습니다!",
        "traits": ["예술적", "유연한", "창의적"]
    },
    "ESFJ": {
        "language": "Kotlin",
        "icon": "💝",
        "reason": "협력적이고 실용적인 ESFJ는 Kotlin의 사용자 친화적 문법과 안드로이드 개발에 적합합니다!",
        "traits": ["협력적", "책임감", "실용적"]
    },
    "ISFJ": {
        "language": "R",
        "icon": "📊",
        "reason": "세심하고 신뢰성 있는 ISFJ는 R의 통계 분석과 데이터 시각화로 의미있는 인사이트를 도출할 수 있습니다!",
        "traits": ["세심함", "책임감", "헌신적"]
    },
    "ENTJ": {
        "language": "Scala",
        "icon": "👑",
        "reason": "야심차고 전략적인 ENTJ는 Scala의 함수형 프로그래밍과 객체지향의 조화로운 결합을 선호합니다!",
        "traits": ["리더", "전략적", "효율적"]
    }
}

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('Popularity_of_Programming_Languages_from_2004_to_2024.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# 메인 앱
def main():
    st.markdown('<h1 class="main-header">🎯 MBTI 프로그래밍 언어 추천기</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">당신의 성격 유형에 딱 맞는 프로그래밍 언어를 찾아드립니다! 💻✨</p>', unsafe_allow_html=True)
    
    # 데이터 로드
    try:
        df = load_data()
    except:
        st.error("❌ CSV 파일을 찾을 수 없습니다. 'Popularity_of_Programming_Languages_from_2004_to_2024.csv' 파일이 현재 디렉토리에 있는지 확인해주세요!")
        return
    
    # 사이드바
    with st.sidebar:
        st.markdown("### 🧭 설정")
        st.markdown("---")
        
        mbti_types = list(MBTI_LANGUAGE_MAP.keys())
        selected_mbti = st.selectbox(
            "🎭 당신의 MBTI를 선택하세요",
            mbti_types,
            help="16가지 MBTI 유형 중 하나를 선택하세요"
        )
        
        st.markdown("---")
        st.markdown("### 📚 MBTI란?")
        st.info(
            "Myers-Briggs Type Indicator는 "
            "개인의 성격을 16가지 유형으로 분류하는 "
            "심리 검사 도구입니다."
        )
        
        st.markdown("---")
        st.markdown("### 💡 Tip")
        st.success("자신의 MBTI를 모르신다면, [16personalities.com](https://www.16personalities.com/ko)에서 무료 테스트를 해보세요!")
    
    # 추천 결과
    recommendation = MBTI_LANGUAGE_MAP[selected_mbti]
    lang = recommendation["language"]
    icon = recommendation["icon"]
    reason = recommendation["reason"]
    traits = recommendation["traits"]
    
    # 추천 박스
    st.markdown(
        f"""
        <div class="recommendation-box">
            <h1 style="font-size: 4rem; margin: 0;">{icon}</h1>
            <h2 style="margin: 1rem 0;">당신을 위한 언어는 <strong>{lang}</strong>입니다!</h2>
            <p style="font-size: 1.2rem; opacity: 0.95;">{reason}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 특성 표시
    st.markdown("### 🌟 당신의 MBTI 특성")
    cols = st.columns(len(traits))
    for idx, trait in enumerate(traits):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="stat-card">
                    <h3>✨</h3>
                    <p style="font-size: 1.1rem; font-weight: bold; margin: 0;">{trait}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # 선택된 언어의 통계 정보
    if lang in df.columns:
        st.markdown(f"## 📈 {lang} 언어 트렌드 분석")
        
        # 최신 데이터
        latest_data = df.iloc[-1]
        oldest_data = df.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_popularity = latest_data[lang]
            st.metric(
                "🔥 현재 인기도",
                f"{current_popularity:.2f}%",
                delta=None,
                help="2024년 12월 기준"
            )
        
        with col2:
            initial_popularity = oldest_data[lang]
            change = current_popularity - initial_popularity
            st.metric(
                "📊 2004년 대비 변화",
                f"{change:+.2f}%",
                delta=f"{change:+.2f}%",
                help="2004년 7월 대비"
            )
        
        with col3:
            max_popularity = df[lang].max()
            max_date = df.loc[df[lang].idxmax(), 'Date'].strftime('%Y년 %m월')
            st.metric(
                "⭐ 최고 인기도",
                f"{max_popularity:.2f}%",
                delta=f"{max_date}",
                help="역대 최고 인기도"
            )
        
        with col4:
            avg_popularity = df[lang].mean()
            st.metric(
                "📌 평균 인기도",
                f"{avg_popularity:.2f}%",
                delta=None,
                help="전체 기간 평균"
            )
        
        # 트렌드 그래프
        st.markdown("### 📉 20년간의 트렌드")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[lang],
            mode='lines',
            name=lang,
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        
        fig.update_layout(
            title=f'{icon} {lang} 인기도 변화 (2004-2024)',
            xaxis_title='연도',
            yaxis_title='인기도 (%)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            font=dict(size=14),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 최근 5년 비교
        st.markdown("### 🎯 최근 5년간의 변화")
        recent_df = df[df['Date'] >= '2019-01-01']
        
        fig2 = px.line(
            recent_df,
            x='Date',
            y=lang,
            title=f'{lang} 최근 5년 상세 트렌드',
            markers=True
        )
        
        fig2.update_traces(
            line_color='#764ba2',
            line_width=3,
            marker=dict(size=6)
        )
        
        fig2.update_layout(
            xaxis_title='날짜',
            yaxis_title='인기도 (%)',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # 전체 언어 비교 테이블
    st.markdown("## 🌐 모든 프로그래밍 언어 비교")
    st.markdown("### 📊 2024년 12월 기준 인기도 순위")
    
    # 최신 데이터로 테이블 생성
    latest = df.iloc[-1]
    
    # 언어별 데이터 정리
    languages = [col for col in df.columns if col != 'Date']
    summary_data = []
    
    language_icons = {
        'Python': '🐍', 'JavaScript': '⚡', 'Java': '☕', 'C/C++': '🔧',
        'C#': '🎯', 'PHP': '🐘', 'TypeScript': '📘', 'Ruby': '💎',
        'Swift': '🦋', 'Go': '🚀', 'Rust': '🦀', 'Kotlin': '🎨',
        'R': '📊', 'Scala': '🔺', 'Dart': '🎯', 'Objective-C': '🍎'
    }
    
    for lang_name in languages:
        icon = language_icons.get(lang_name, '💻')
        current = latest[lang_name]
        avg = df[lang_name].mean()
        max_val = df[lang_name].max()
        min_val = df[lang_name].min()
        change = current - df.iloc[0][lang_name]
        
        summary_data.append({
            '순위': 0,  # 나중에 채울 예정
            '언어': f"{icon} {lang_name}",
            '현재 인기도': f"{current:.2f}%",
            '평균 인기도': f"{avg:.2f}%",
            '최고 인기도': f"{max_val:.2f}%",
            '20년간 변화': f"{change:+.2f}%",
            '트렌드': '📈' if change > 0 else '📉'
        })
    
    # 현재 인기도로 정렬
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('현재 인기도', ascending=False)
    summary_df['순위'] = range(1, len(summary_df) + 1)
    
    # 순위에 따라 메달 추가
    def add_medal(rank):
        if rank == 1:
            return f"🥇 {rank}"
        elif rank == 2:
            return f"🥈 {rank}"
        elif rank == 3:
            return f"🥉 {rank}"
        else:
            return f"{rank}"
    
    summary_df['순위'] = summary_df['순위'].apply(add_medal)
    
    # 추천된 언어 하이라이트
    def highlight_recommended(row):
        if lang in row['언어']:
            return ['background-color: #667eea; color: white; font-weight: bold'] * len(row)
        return [''] * len(row)
    
    styled_df = summary_df.style.apply(highlight_recommended, axis=1)
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=600
    )
    
    # 추가 인사이트
    st.markdown("### 💡 주요 인사이트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_languages = summary_df.head(5)['언어'].str.replace(r'^[^\s]+ ', '', regex=True).tolist()
        st.info(f"""
        **🏆 TOP 5 언어**
        
        1. {summary_df.iloc[0]['언어']}
        2. {summary_df.iloc[1]['언어']}
        3. {summary_df.iloc[2]['언어']}
        4. {summary_df.iloc[3]['언어']}
        5. {summary_df.iloc[4]['언어']}
        """)
    
    with col2:
        # 가장 많이 성장한 언어
        growth_sorted = pd.DataFrame(summary_data).sort_values('20년간 변화', ascending=False)
        st.success(f"""
        **📈 가장 성장한 언어들**
        
        • {growth_sorted.iloc[0]['언어']} ({growth_sorted.iloc[0]['20년간 변화']})
        • {growth_sorted.iloc[1]['언어']} ({growth_sorted.iloc[1]['20년간 변화']})
        • {growth_sorted.iloc[2]['언어']} ({growth_sorted.iloc[2]['20년간 변화']})
        """)
    
    # 전체 트렌드 비교 그래프
    st.markdown("### 🎨 모든 언어 트렌드 비교")
    
    # 인기도 상위 10개 언어만 표시
    top_10_languages = summary_df.head(10)['언어'].str.replace(r'^[^\s]+ ', '', regex=True).tolist()
    
    fig3 = go.Figure()
    
    colors = px.colors.qualitative.Set3
    
    for idx, lang_name in enumerate(top_10_languages):
        if lang_name in df.columns:
            fig3.add_trace(go.Scatter(
                x=df['Date'],
                y=df[lang_name],
                mode='lines',
                name=lang_name,
                line=dict(width=2.5 if lang_name == lang else 1.5),
                opacity=1.0 if lang_name == lang else 0.6
            ))
    
    fig3.update_layout(
        title='상위 10개 프로그래밍 언어 트렌드 비교',
        xaxis_title='연도',
        yaxis_title='인기도 (%)',
        hovermode='x unified',
        template='plotly_white',
        height=600,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>💻 <strong>프로그래밍 언어 추천 웹앱</strong> 💻</p>
            <p>데이터 출처: TIOBE Index (2004-2024)</p>
            <p>Made with ❤️ using Streamlit & Plotly</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
