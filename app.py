import streamlit as st
import random

# --- 🎮 Web Page Configuration ---
st.set_page_config(page_title="Hangul Wordle", page_icon="📝", layout="centered")

# ==========================================
# 🎨 UI Style Sheet (흰색 줄선 노트 감성 & 폼 다이어트)
# ==========================================
st.markdown("""
    <style>
        @import url('https://cdn.jsdelivr.net/gh/neodgm/neodgm-webfont@1.530/neodgm/style.css');
        
        /* 📝 아날로그 줄선 노트 배경 */
        [data-testid="stAppViewContainer"] { 
            background-color: #ffffff !important; 
            background-image: 
                linear-gradient(90deg, transparent 79px, #ff9e9e 79px, #ff9e9e 81px, transparent 81px),
                linear-gradient(#eeeeee 1px, transparent 1px) !important;
            background-size: 100% 40px !important;
            background-attachment: local !important;
        }
        
        /* 텍스트를 검은색 계열로 변경 */
        h1, h2, h3, p, span, label { font-family: 'NeoDunggeunmo', sans-serif !important; color: #333333 !important; }
        h1 { text-align: center !important; font-size: 3rem !important; margin-bottom: 20px !important; color: #1e3a8a !important; text-shadow: 2px 2px 0px rgba(0,0,0,0.1); }
        
        /* 🟩 워들 입력 격자판 스타일 (노트 버전) */
        .wordle-row { display: flex; justify-content: center; margin-bottom: 6px; }
        .wordle-tile {
            width: 55px; height: 55px; line-height: 52px;
            border: 2px solid #a3a8ad; border-radius: 6px;
            text-align: center; font-size: 1.6rem; font-weight: bold;
            margin: 0 3px; user-select: none;
            background-color: rgba(255, 255, 255, 0.7);
            color: #111111;
        }
        .tile-correct { background-color: #538d4e !important; border-color: #538d4e !important; color: white !important; }
        .tile-present { background-color: #b59f3b !important; border-color: #b59f3b !important; color: white !important; }
        .tile-absent { background-color: #787c7e !important; border-color: #787c7e !important; color: white !important; }
        .tile-empty { border-color: #d3d6da; }
        
        /* ⌨️ 가상 키보드 스타일 (노트 버전) */
        .kb-container { margin: 25px 0; text-align: center; }
        .kb-row { display: flex; justify-content: center; margin-bottom: 6px; gap: 4px; }
        .kb-key {
            min-width: 32px; height: 42px; line-height: 42px;
            background-color: #d3d6da; border-radius: 4px; border: 1px solid #b0b4b8;
            text-align: center; font-size: 1.1rem; font-weight: bold;
            color: #111111; user-select: none; padding: 0 6px; box-shadow: 0 2px 0 rgba(0,0,0,0.1);
        }
        .kb-correct { background-color: #538d4e !important; color: white !important; border-color: #538d4e !important; }
        .kb-present { background-color: #b59f3b !important; color: white !important; border-color: #b59f3b !important; }
        .kb-absent { background-color: #787c7e !important; color: white !important; border-color: #787c7e !important; }
        
        /* 인풋창 & 버튼 노트 스타일로 수정 */
        .stButton>button, .stFormSubmitButton>button { background-color: #3b82f6 !important; color: white !important; border: 2px solid #2563eb !important; border-radius: 8px !important; font-size: 1.2rem !important; height: 50px; width: 100%; font-family: 'NeoDunggeunmo', sans-serif !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .stButton>button:hover, .stFormSubmitButton>button:hover { background-color: #2563eb !important; transform: scale(1.02); }
        .stTextInput input { background-color: rgba(255,255,255,0.9) !important; color: #111111 !important; border: 2px solid #3b82f6 !important; font-size: 1.3rem !important; text-align: center !important; border-radius: 8px !important; }
        
        /* 🔥 폼 테두리 및 여백 완전 제거 (다이어트) */
        [data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; }
        div[data-testid="stForm"] > div { row-gap: 5px !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧩 한글 자모음 분해 함수 & 단어장
# ==========================================
def decompose_hangul(word):
    CHOSUNG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    
    result = []
    for char in word:
        if '가' <= char <= '힣':
            char_code = ord(char) - 0xAC00
            result.append(CHOSUNG[char_code // (21 * 28)])
            result.append(JUNGSUNG[(char_code % (21 * 28)) // 28])
            if JONGSUNG[(char_code % (21 * 28)) % 28] != '':
                result.append(JONGSUNG[(char_code % (21 * 28)) % 28])
        else:
            result.append(char)
    return result

WORD_POOL = [
    "가방", "가족", "가을", "감사", "감자", "거북", "거울", "거인", "겨울", "공기",
    "과일", "구름", "국가", "글씨", "기분", "기억", "기적", "기린", "그림", "나물",
    "남자", "내일", "냄비", "냄새", "노력", "노을", "도움", "딸기", "마늘", "마당",
    "마술", "마을", "마음", "맥주", "매력", "문제", "문화", "미술", "바닥", "바늘",
    "바람", "반지", "보람", "보름", "보석", "봄비", "사람", "사랑", "사막", "산소",
    "사탕", "사진", "새싹", "소금", "소년", "소설", "소원", "수건", "수박", "수첩",
    "숙제", "승리", "시간", "시골", "시험", "실패", "악마", "안내", "어른", "역사",
    "여름", "열쇠", "오늘", "우산", "우정", "용서", "이름", "이슬", "인사", "자연",
    "장미", "점수", "저녁", "주말", "참새", "천사", "축하", "침대", "콜라", "태양",
    "팔찌", "편지", "평화", "학교", "하늘", "현재", "화산", "휴일", "희망", "김치",
    "호박", "당근", "양파", "생강", "참외", "앵두", "안경", "지갑", "홍차", "라면",
    "약국", "은행", "서점", "호텔", "공원", "시장", "시민", "혜성", "유성", "태풍",
    "안개", "장마", "번개"
]

# ==========================================
# 🧠 세션 상태 (메모리) 초기화
# ==========================================
if "wordle_nickname" not in st.session_state:
    st.session_state.wordle_nickname = None

if "wordle_secret" not in st.session_state:
    st.session_state.wordle_secret = random.choice(WORD_POOL)
    st.session_state.wordle_jamo = decompose_hangul(st.session_state.wordle_secret)
    st.session_state.wordle_guesses = []
    st.session_state.wordle_game_over = False
    st.session_state.wordle_won = False

def reset_wordle():
    st.session_state.wordle_secret = random.choice(WORD_POOL)
    st.session_state.wordle_jamo = decompose_hangul(st.session_state.wordle_secret)
    st.session_state.wordle_guesses = []
    st.session_state.wordle_game_over = False
    st.session_state.wordle_won = False

def get_jamo_statuses():
    statuses = {}
    target_jamo = st.session_state.wordle_jamo
    for guess in st.session_state.wordle_guesses:
        guess_jamo = decompose_hangul(guess)
        for i in range(min(len(guess_jamo), 5)):
            char = guess_jamo[i]
            if char == target_jamo[i]: statuses[char] = "correct"
            elif char in target_jamo:
                if statuses.get(char) != "correct": statuses[char] = "present"
            else:
                if char not in statuses: statuses[char] = "absent"
    return statuses

# ==========================================
# 🖥️ 게임 화면 구현 (UI)
# ==========================================
st.markdown("<h1>📝 한글 자모 워들</h1>", unsafe_allow_html=True)

# 🚪 로그인 화면 (DB 없이 이름만 기억)
if st.session_state.wordle_nickname is None:
    st.markdown("<p style='text-align:center;'>공책에 이름을 적고 게임을 시작하세요!</p>", unsafe_allow_html=True)
    nickname_input = st.text_input("닉네임", placeholder="예: 워들고수99", label_visibility="collapsed")
    if st.button("✏️ 공책 펴고 시작하기"):
        if nickname_input.strip():
            st.session_state.wordle_nickname = nickname_input.strip()
            st.rerun()
        else:
            st.warning("이름을 적어주세요!")

# 🎮 실제 게임 화면
else:
    st.markdown(f"<p style='text-align:right; font-weight:bold; color:#3b82f6;'>👤 {st.session_state.wordle_nickname}의 공책</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6b7280; margin-top:-10px;'>5개의 자모음 단어를 맞춰보세요! (기회 6번)</p>", unsafe_allow_html=True)
    
    # 🟩 5x6 워들 격자판 그리기
    target_jamo = st.session_state.wordle_jamo
    for row_idx in range(6):
        html_row = '<div class="wordle-row">'
        if row_idx < len(st.session_state.wordle_guesses):
            guess_word = st.session_state.wordle_guesses[row_idx]
            guess_jamo = decompose_hangul(guess_word)
            tile_classes = ["tile-absent"] * 5
            taken = [False] * 5
            for i in range(5):
                if guess_jamo[i] == target_jamo[i]: tile_classes[i] = "tile-correct"; taken[i] = True
            for i in range(5):
                if tile_classes[i] == "tile-correct": continue
                for j in range(5):
                    if not taken[j] and guess_jamo[i] == target_jamo[j]: tile_classes[i] = "tile-present"; taken[j] = True; break
            for i in range(5):
                html_row += f'<div class="wordle-tile {tile_classes[i]}">{guess_jamo[i]}</div>'
        else:
            for i in range(5): html_row += '<div class="wordle-tile tile-empty"></div>'
        html_row += '</div>'
        st.markdown(html_row, unsafe_allow_html=True)

    # ⌨️ 실시간 음영 처리 가상 키보드 (4줄 완벽 배열)
    jamo_statuses = get_jamo_statuses()
    keyboard_layout = [
        ['ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ', 'ㅒ', 'ㅖ'],
        ['ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ'],
        ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ'],
        ['ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅠ', 'ㅜ', 'ㅡ']
    ]
    kb_html = '<div class="kb-container">'
    for row in keyboard_layout:
        kb_html += '<div class="kb-row">'
        for char in row:
            status = jamo_statuses.get(char, 'unused')
            kb_html += f'<div class="kb-key kb-{status}">{char}</div>'
        kb_html += '</div>'
    kb_html += '</div>'
    st.markdown(kb_html, unsafe_allow_html=True)

    # 🎮 유저 입력 폼 (가로로 합치고 다이어트!)
    if not st.session_state.wordle_game_over:
        with st.form("wordle_input_form", clear_on_submit=True, border=False):
            col1, col2 = st.columns([3, 1]) # 입력창과 버튼을 3:1 비율로 한 줄 배치
            with col1:
                user_guess = st.text_input("단어 입력", max_chars=6, placeholder="정답 입력...", label_visibility="collapsed").strip()
            with col2:
                submit_button = st.form_submit_button("엔터 ⏎")
                
            if submit_button:
                guess_decomposed = decompose_hangul(user_guess)
                if len(guess_decomposed) != 5:
                    st.warning(f"⚠️ 5칸 자모음 규격에 맞지 않습니다! (분해 시 {len(guess_decomposed)}칸)")
                else:
                    st.session_state.wordle_guesses.append(user_guess)
                    if user_guess == st.session_state.wordle_secret:
                        st.session_state.wordle_game_over = True
                        st.session_state.wordle_won = True
                        st.rerun()
                    elif len(st.session_state.wordle_guesses) >= 6:
                        st.session_state.wordle_game_over = True
                        st.rerun()
                    else:
                        st.rerun()
    else:
        # 🎉 결과 화면
        if st.session_state.wordle_won:
            st.success(f"🎉 정답입니다! [{st.session_state.wordle_nickname}]님이 {len(st.session_state.wordle_guesses)}번째 시도 만에 맞추셨습니다!")
        else:
            st.error(f"😢 기회를 모두 소진하셨습니다. 정답은 💡 [{st.session_state.wordle_secret}] 이었습니다.")
            
        st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <a href="https://ko.dict.naver.com/#/search?query={st.session_state.wordle_secret}" target="_blank" 
                   style="background-color: #538d4e; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-family: 'NeoDunggeunmo', sans-serif; font-size: 1.1rem; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                   📖 [{st.session_state.wordle_secret}] 단어 뜻 확인하기 (국어사전)
                </a>
            </div>
        """, unsafe_allow_html=True)
            
        if st.button("🔄 다음 공책 펴기 (새 게임)"):
            reset_wordle()
            st.rerun()
