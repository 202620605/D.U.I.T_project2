import streamlit as st
import random
import requests
from bs4 import BeautifulSoup

st.title("📡 1군 & 2군 실시간 라이브 매치 센터")

# 선호 구단 세션 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("메인 페이지에서 먼저 로그인을 해주세요.")
else:
    team = st.session_state["fav_team"]
    
    tab1, tab2, tab3 = st.tabs(["⚡ 1군 라이브", "🌱 2군 라이브", "📢 인사/공시/부상 리포트"])
    
    with tab1:
        st.header(f"오늘의 1군 경기 일정 ({team})")
        
        # 가상의 기상청 API 연동 조건문 (우취 확률 계산)
        rain_prob = random.randint(10, 90) # 실개발 시 날씨 API 연동
        st.metric(label="경기장 예상 강수 확률", value=f"{rain_prob}%")
        if rain_prob >= 70:
            st.error("⚠️ 우천 취소(우취) 가능성이 매우 높습니다! 실시간 공시를 확인하세요.")
        else:
            st.success("☀️ 경기가 정상 진행될 것으로 예상됩니다.")
            
        st.write("**오늘의 선발 투수:** 임찬규 (상대팀: 양현종)")
        st.code("🚨 [실시간 라인업 완료] 1.홍창기 2.신민재 3.김현수 4.오스틴 5.문보경 ...", language="markdown")
        
        # 실시간 문자 중계 파싱 시뮬레이션 인터페이스
        st.subheader("🏟️ 실시간 문자 중계 전광판 (2~3초 자동 파싱 영역)")
        
        # 가상의 네이버 스포츠 실시간 문자중계 텍스트 파싱 로직 샘플
        mock_naver_chats = [
            "[3회말] 오스틴 2점 홈런!! 비거리 120m 좌측 담장 통과! (득점: 2-0)",
            "[5회초] 투수 임찬규, 김도영에게 안타 허용 후 실점 (득점: 2-1)",
            "[7회초] 🚨 부상 상황 발생: 타자 주루 도중 발목 통증 호소, 선수 교체 완료.",
            "[주석/오피셜 소식] 인스타 라이브 확인 결과, 해당 선수는 단순 타박상으로 확인됨."
        ]
        
        for chat in mock_naver_chats:
            if "홈런" in chat or "안타" in chat:
                st.success(chat)
            elif "실점" in chat or "부상" in chat:
                st.danger(chat) if hasattr(st, "danger") else st.error(chat)
            else:
                st.info(chat)

    with tab2:
        st.header(f"🌱 2군 퓨처스리그 및 육성군 실시간 현황")
        st.write("1군과 동일한 네이버 퓨처스 리그 문자 중계 및 구단 홈페이지 육성군 명단 연동 데이터입니다.")
        st.text_area("2군 실시간 전황 로그", value="[2회초] 육성군 OOO 3루타로 1타점 득점 성공\n[현재 2군 스코어] 1 - 0 리드 중", height=100)

    with tab3:
        st.subheader("📅 오늘의 1·2군 선수 등록 및 말소 공시")
        st.write("*(KBO / 네이버 스포츠 종합 공시 실시간 크롤링 연동)*")
        
        col_reg, col_del = st.columns(2)
        with col_reg:
            st.success("⬆️ 오늘 1군 등록 선수\n- OOO (투수)\n- OOO (외야수)")
        with col_del:
            st.error("⬇️ 오늘 1군 말소 (2군 이동)\n- OOO (내야수)")
            
        st.subheader("🚑 부상 및 트레이드/영입/방출 마켓 리포트")
        st.warning("🚨 [부상] OOO 선수 - 햄스트링 부상 (예상 복귀 시점: 3주 뒤 후반기 시작 전)")
        st.info("🔄 [트레이드/영입] 구단 공식 인스타그램 공시 완료: 외야수 OOO 영입 확정 (방출: OOO)")

