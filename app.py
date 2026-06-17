import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="KBO 통합 관제탑", page_icon="⚾", layout="wide")

# DB 연결 함수
def get_db_connection():
    return sqlite3.connect("baseball.db")

# 구단 기본 정보 정의
KBO_CLUBS = {
    "LG 트윈스": {"stadium": "잠실 야구장", "homepage": "https://www.lgtwins.com/", "insta": "https://www.instagram.com/lgtwinsbaseballclub/", "emblem": "🦁"},
    "KIA 타이거즈": {"stadium": "광주-기아 챔피언스 필드", "homepage": "https://www.kiatigers.co.kr/", "insta": "https://www.instagram.com/kiatigers/", "emblem": "🐯"},
    "삼성 라이온즈": {"stadium": "대구 삼성 라이온즈 파크", "homepage": "https://www.samsunglions.com/", "insta": "https://www.instagram.com/sam_lions_play/", "emblem": "🦁"},
    "두산 베어스": {"stadium": "잠실 야구장", "homepage": "https://www.doosanbears.com/", "insta": "https://www.instagram.com/doosanbears_1982/", "emblem": "🐻"},
    "롯데 자이언츠": {"stadium": "부산 사직 야구장", "homepage": "https://www.giantsclub.com/", "insta": "https://www.instagram.com/busanlottegiants/", "emblem": "🦅"},
    "SSG 랜더스": {"stadium": "인천 SSG 랜더스 필드", "homepage": "http://www.ssglanders.com/", "insta": "https://www.instagram.com/ssglanders.official/", "emblem": "🚀"},
    "KT 위즈": {"stadium": "수원 케이티 위즈 파크", "homepage": "https://www.ktwiz.co.kr/", "insta": "https://www.instagram.com/ktwiz.pr/", "emblem": "🧙"},
    "한화 이글스": {"stadium": "대전 한화생명 이글스파크", "homepage": "https://www.hanwhaeagles.co.kr/", "insta": "https://www.instagram.com/hanwhaeagles_official/", "emblem": "🦅"},
    "NC 다이노스": {"stadium": "창원 NC 파크", "homepage": "https://www.ncdinos.com/", "insta": "https://www.instagram.com/ncdinosofficial/", "emblem": "🦖"},
    "키움 히어로즈": {"stadium": "고척 스카이돔", "homepage": "https://www.heroesbaseballclub.co.kr/", "insta": "https://www.instagram.com/heroesbaseballclub/", "emblem": "🦸"}
}

# 세션 로그인 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.session_state["fav_team"] = "LG 트윈스"

# 데이터베이스가 없으면 자동 생성
if not os.path.exists("baseball.db"):
    import baseball_db
    baseball_db.init_db()

# 로그인 / 회원가입 로직
if not st.session_state["logged_in"]:
    st.title("⚾ KBO 실시간 통합 관제탑 로그인")
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    
    with tab1:
        login_user = st.text_input("아이디", key="login_id")
        login_pw = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT favorite_team FROM users WHERE username=? AND password=?", (login_user, login_pw))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                st.session_state["logged_in"] = True
                st.session_state["user"] = login_user
                st.session_state["fav_team"] = result[0]
                st.success(f"{login_user}님 환영합니다! 선호 구단: {result[0]}")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 틀렸습니다.")
                
    with tab2:
        reg_user = st.text_input("새 아이디", key="reg_id")
        reg_pw = st.text_input("새 비밀번호", type="password", key="reg_pw")
        reg_team = st.selectbox("응원 구단 선택", list(KBO_CLUBS.keys()), key="reg_team")
        if st.button("회원가입"):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (reg_user, reg_pw, reg_team))
                conn.commit()
                conn.close()
                st.success("회원가입 완료! 로그인 탭에서 로그인해 주세요.")
            except sqlite3.IntegrityError:
                st.error("이미 존재하는 아이디입니다.")

# 로그인 완료 후 메인 대시보드
else:
    st.sidebar.success(f"종합 관제탑 작동 중 ({st.session_state['user']}님)")
    st.title(f"{st.session_state['fav_team']} 매치 포트")
    
    # 선호 구단 정보 로드
    team_data = KBO_CLUBS[st.session_state["fav_team"]]
    
    col1, col2 = st.columns([1, 3])
    with col1:
        # 이모지로 대체 출력 (assets/에 실제 png 배치 시 st.image(f"assets/{팀명}.png")로 변경 가능)
        st.text(team_data["emblem"])
        st.metric(label="나의 응원 구단", value=st.session_state["fav_team"])
    with col2:
        st.subheader("📌 구단 오피셜 허브 (크롤링 연계)")
        st.info(f"🏟️ **홈구장:** {team_data['stadium']}")
        
        # 실제 연계 크롤러가 들어갈 영역 가이드
        st.markdown(f"🔗 [네이버 스포츠 {st.session_state['fav_team']} 섹션 바로가기](https://sports.news.naver.com/kbaseball/index)")
        st.markdown(f"📸 [공식 인스타그램 연계피드 확인]({team_data['insta']})")
        st.markdown(f"🏠 [공식 홈페이지 선수단 정보]({team_data['homepage']})")
        
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.rerun()

