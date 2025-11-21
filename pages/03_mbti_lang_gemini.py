import streamlit as st

# 1. 페이지 설정 (브라우저 탭 타이틀 및 아이콘)
st.set_page_config(
    page_title="MBTI 코딩 진로 상담소",
    page_icon="💻",
    layout="wide"  # 테이블을 넓게 보여주기 위해 wide 모드 설정
)

# 2. 데이터 정의 (별도 DB나 파일 없이 딕셔너리로 관리)
# 16가지 MBTI 유형과 매칭되는 언어, 설명, 이모지
mbti_db = {
    "INTJ": {"lang": "Rust", "icon": "🦀", "tag": "전략가", "desc": "안전하고 효율적인 시스템 설계"},
    "INTP": {"lang": "Python", "icon": "🐍", "tag": "논리술사", "desc": "AI와 데이터의 본질 탐구"},
    "ENTJ": {"lang": "C++", "icon": "⚡", "tag": "지배자", "desc": "압도적인 성능과 시스템 장악"},
    "ENTP": {"lang": "Go (Golang)", "icon": "🐹", "tag": "혁명가", "desc": "빠르고 실용적인 구글의 언어"},
    "INFJ": {"lang": "Swift", "icon": "🍎", "tag": "예언자", "desc": "우아한 구조의 iOS 앱 개발"},
    "INFP": {"lang": "Kotlin", "icon": "🤖", "tag": "몽상가", "desc": "자유로운 안드로이드 세상 창조"},
    "ENFJ": {"lang": "Ruby", "icon": "💎", "tag": "언변가", "desc": "개발자의 행복을 위한 코딩"},
    "ENFP": {"lang": "JavaScript", "icon": "✨", "tag": "스파크", "desc": "웹 프론트엔드의 화려한 마법"},
    "ISTJ": {"lang": "Java", "icon": "☕", "tag": "관리자", "desc": "견고하고 안정적인 대규모 백엔드"},
    "ISFJ": {"lang": "SQL", "icon": "🗃️", "tag": "수호자", "desc": "데이터의 질서와 보존을 담당"},
    "ESTJ": {"lang": "C#", "icon": "🎯", "tag": "감독관", "desc": "체계적인 윈도우/.NET 생태계"},
    "ESFJ": {"lang": "PHP", "icon": "🐘", "tag": "도우미", "desc": "웹의 역사와 함께하는 친근함"},
    "ISTP": {"lang": "C", "icon": "🔌", "tag": "장인", "desc": "하드웨어를 제어하는 극한의 효율"},
    "ISFP": {"lang": "Dart (Flutter)", "icon": "🦋", "tag": "예술가", "desc": "하나의 코드로 그리는 예쁜 UI"},
    "ESTP": {"lang": "Solidity", "icon": "⛓️", "tag": "사업가", "desc": "블록체인이라는 기회의 땅"},
    "ESFP": {"lang": "HTML/CSS", "icon": "🎨", "tag": "연예인", "desc": "눈에 보이는 즉각적인 결과물"}
}

# 3. 사이드바: 사용자 입력
with st.sidebar:
    st.title("🔎 내 성향 찾기")
    st.write("당신의 MBTI를 선택해주세요.")
    
    # MBTI 리스트 정렬 (찾기 쉽게)
    mbti_list = sorted(list(mbti_db.keys()))
    user_mbti = st.selectbox("MBTI 유형 선택", mbti_list)
    
    st.markdown("---")
    st.caption("Developer Career Guide 🤖")

# 4. 메인 화면: 추천 결과
st.title("🚀 주니어 개발자 진로 상담소")
st.markdown(f"### **{user_mbti}** 유형인 당신에게 추천하는 언어는...")

# 선택된 데이터 가져오기
selected_data = mbti_db[user_mbti]

# 시각적 강조를 위한 컨테이너
container = st.container(border=True)
with container:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # 이모지를 아주 크게 표시
        st.markdown(f"<div style='font-size: 80px; text-align: center; line-height: 1.2;'>{selected_data['icon']}</div>", unsafe_allow_html=True)
    
    with col2:
        st.subheader(f"{selected_data['lang']}")
        st.markdown(f"**🕵️ 별명:** {selected_data['tag']}")
        st.info(selected_data['desc'])

st.write("") # 여백
st.success("💡 **Tip:** 이 언어는 당신의 타고난 성향과 아주 잘 맞을 거예요! 지금 바로 'Hello World'를 찍어보세요!")
st.markdown("---")

# 5. 요약 테이블 (선택하지 않은 다른 언어들)
st.subheader("📊 다른 언어들은 어때요?")
st.write("선택하신 유형 외에 다른 MBTI 추천 언어들을 한눈에 확인해보세요.")

# Pandas 없이 순수 Python 리스트로 데이터 변환 (테이블용)
table_data = []
for mbti, info in mbti_db.items():
    # 현재 선택된 MBTI는 제외하고 보여줄지, 포함할지 결정 (여기서는 비교를 위해 모두 표시하되 선택된 행 강조는 어려우므로 전체 표시)
    # 요청하신 '다른 프로그래밍 언어들'의 뉘앙스를 살려 선택된 것은 맨 위로 올리거나, 혹은 그대로 둡니다.
    # 여기서는 전체 리스트를 깔끔하게 보여줍니다.
    table_data.append({
        "MBTI": mbti,
        "추천 언어": f"{info['icon']} {info['lang']}",
        "특징 요약": info['desc']
    })

# 스트림릿 기본 데이터프레임 기능 사용 (Pandas import 불필요)
# use_container_width=True로 화면 꽉 차게 표시
st.dataframe(
    table_data, 
    column_config={
        "MBTI": st.column_config.TextColumn("성격 유형", width="small"),
        "추천 언어": st.column_config.TextColumn("추천 언어", width="medium"),
        "특징 요약": st.column_config.TextColumn("한줄 요약", width="large"),
    },
    hide_index=True,
    use_container_width=True
)

# 6. 푸터
st.markdown(
    """
    <div style='text-align: center; color: #888; margin-top: 50px; font-size: 12px;'>
        Made with ❤️ by Streamlit | No external libraries utilized.
    </div>
    """, 
    unsafe_allow_html=True
)
