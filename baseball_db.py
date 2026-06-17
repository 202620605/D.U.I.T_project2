import sqlite3

def init_db():
    conn = sqlite3.connect("baseball.db")
    cursor = conn.cursor()
    
    # 1. 회원 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            favorite_team TEXT
        )
    """)
    
    # 2. 직관 일기 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            opposing_team TEXT,
            score TEXT,
            weather TEXT,
            companion TEXT,
            mood TEXT,
            content TEXT,
            lineup TEXT,
            pitcher TEXT
        )
    """)
    
    # 3. 과거 경기 데이터 샘플 테이블 (직관 일기 자동 로드용 가상 데이터)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_history (
            date TEXT,
            team TEXT,
            opposing_team TEXT,
            score TEXT,
            lineup TEXT,
            pitcher TEXT,
            PRIMARY KEY (date, team)
        )
    """)
    
    # 샘플 데이터 삽입 (테스트용)
    cursor.execute("""
        INSERT OR IGNORE INTO game_history VALUES 
        ('2026-06-17', 'LG 트윈스', 'KIA 타이거즈', '5:4', '1.홍창기 2.신민재 3.김현수 4.오스틴 5.문보경', '임찬규'),
        ('2026-06-17', 'KIA 타이거즈', 'LG 트윈스', '4:5', '1.박찬호 2.최원준 3.김도영 4.최형우 5.나성범', '양현종')
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("데이터베이스 초기화 완료!")
