import streamlit as st
import sqlite3

st.title("📝 나만의 야구 직관 다이어리")

def get_db_connection():
    return sqlite3.connect("baseball.db")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("메인 페이지에서 먼저 로그인을 해주세요.")
else:
    user = st.session_state["user"]
    team = st.session_state["fav_team"]
    
    st.subheader("🧼 새로운 직관 일기 작성하기")
    
    # 1. 사용자 수동 입력 단계
    date = st.date_input("직관 날짜 선택").strftime("%Y-%m-%d")
    opposing_team = st.text_input("상대 팀명 입력 (예: KIA 타이거즈)")
    score = st.text_input("최종 점수 입력 (예: 5:4)")
    
    # 2. 자동 로드 트리거 버튼
    auto_lineup = ""
    auto_pitcher = ""
    
    if st.button("날짜/점수 기반 선발 및 라인업 자동 로드"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT lineup, pitcher FROM game_history WHERE date=? AND team=? AND opposing_team=? AND score=?",
            (date, team, opposing_team, score)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            st.session_state["auto_lineup"] = result[0]
            st.session_state["auto_pitcher"] = result[1]
            st.success("네이버 스포츠 과거 기록실 데이터 연동 완료!")
        else:
            st.error("해당 날짜와 스코어에 일치하는 오피셜 경기 데이터가 없습니다. 수동으로 입력해 주세요.")
            st.session_state["auto_lineup"] = ""
            st.session_state["auto_pitcher"] = ""

    # 세션 상태값 반영
    lineup_val = st.session_state.get("auto_lineup", "")
    pitcher_val = st.session_state.get("auto_pitcher", "")

    # 3. 추가 일기 폼
    final_pitcher = st.text_input("그날의 선발 투수", value=pitcher_val)
    final_lineup = st.text_area("그날의 라인업", value=lineup_val)
    
    weather = st.selectbox("구장 날씨", ["맑음 ☀️", "흐림 ☁️", "비온 뒤 갬 🌦️", "고척돔(실내) 🏟️"])
    companion = st.text_input("같이 간 사람")
    mood = st.select_slider("그날 나의 기분 상태", options=["최악 🤬", "아쉬움 🥲", "보통 😐", "신남 🥳", "도파민 폭발 🚀"])
    content = st.text_area("오늘의 직관 일기 한 줄 평 및 상세 기록")
    
    if st.button("직관 일기 저장하기"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO diary (username, date, opposing_team, score, weather, companion, mood, content, lineup, pitcher)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user, date, opposing_team, score, weather, companion, mood, content, final_lineup, final_pitcher))
        conn.commit()
        conn.close()
        st.success("직관 일기가 안전하게 다이어리에 저장되었습니다!")
        
    # 저장된 일기 목록 보여주기
    st.markdown("---")
    st.subheader("📚 나의 지난 직관 기록첩")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, opposing_team, score, mood, content FROM diary WHERE username=?", (user,))
    history = cursor.fetchall()
    conn.close()
    
    for row in history:
        with st.expander(f"📅 {row[0]} | vs {row[1]} ({row[2]}) - {row[3]}"):
            st.write(f"**일기 내용:** {row[4]}")

