import streamlit as st
import random

# --- 🎮 Web Page Configuration ---
st.set_page_config(page_title="Hangul Jamo Wordle", page_icon="🟩", layout="centered")

# ==========================================
# 🎨 UI Style Sheet (레트로 워들 스타일)
# ==========================================
st.markdown("""
    <style>
        @import url('https://cdn.jsdelivr.net/gh/neodgm/neodgm-webfont@1.530/neodgm/style.css');
        [data-testid="stAppViewContainer"] { background-color: #121213 !important; }
        
        h1, h2, h3, p, span, div, label { font-family: 'NeoDunggeunmo', sans-serif !important; color: white; }
        h1 { color: #ffffff !important; text-align: center !important; font-size: 3rem !important; margin-bottom: 20px !important;}
        
        /* 워들 타일 스타일 */
        .wordle-row { display: flex; justify-content: center; margin-bottom: 6px; }
        .wordle-tile {
            width: 55px; height: 55px; line-height: 52px;
            border: 2px solid #3a3a3c; border-radius: 4px;
            text-align: center; font-size: 1.6rem; font-weight: bold;
            margin: 0 3px; user-select: none;
        }
        .tile-correct { background-color: #538d4e !important; border-color: #538d4e !important; color: white !important; }
        .tile-present { background-color: #b59f3b !important; border-color: #b59f3b !important; color: white !important; }
        .tile-absent { background-color: #3a3a3c !important; border-color: #3a3a3c !important; color: #787c7e !important; }
        .tile-empty { background-color: #121213; color: #565758; border-color: #3a3a3c; }
        
        .stButton>button { background-color: #818384 !important; color: white !important; border: none !important; border-radius: 4px !important; font-size: 1.1rem !important; height: 50px; width: 100%; }
        .stButton>button:hover { background-color: #565758 !important; transform: scale(1.02); }
        .stTextInput input { background-color: #121213 !important; color: white !important; border: 2px solid #3a3a3c !important; font-size: 1.3rem !important; text-align: center !important; }
        .stTextInput input:focus { border-color: #818384 !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧩 한글 자모음 분해 함수 (Pure Python)
# ==========================================
def decompose_hangul(word):
    CHOSUNG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNGSUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONGSUNG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    
    result = []
    for char in word:
        if '가' <= char <= '힣':
            char_code = ord(char) - 0xAC00
            cho = char_code // (21 * 28)
            jung = (char_code % (21 * 28)) // 28
            jong = (char_code % (21 * 28)) % 28
            
            result.append(CHOSUNG[cho])
            result.append(JUNGSUNG[jung])
            if JONGSUNG[jong] != '':
                result.append(JONGSUNG[jong])
        else:
            result.append(char)
    return result

# ==========================================
# 📂 5자모 규격 확장 단어 데이터셋 (정확히 5칸으로 떨어지는 단어들)
# ==========================================
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

# ==========================================
# 🖥️ 게임 화면 구현 (UI)
# ==========================================
st.markdown("<h1>🔠 한글 자모 워들</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#818384; margin-top:-10px;'>5개의 자모음으로 이루어진 단어를 맞추세요! (기회 6번)</p>", unsafe_allow_html=True)
st.write("")

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
            if guess_jamo[i] == target_jamo[i]:
                tile_classes[i] = "tile-correct"
                taken[i] = True
                
        for i in range(5):
            if tile_classes[i] == "tile-correct":
                continue
            for j in range(5):
                if not taken[j] and guess_jamo[i] == target_jamo[j]:
                    tile_classes[i] = "tile-present"
                    taken[j] = True
                    break
                    
        for i in range(5):
            html_row += f'<div class="wordle-tile {tile_classes[i]}">{guess_jamo[i]}</div>'
            
    else:
        for i in range(5):
            html_row += '<div class="wordle-tile tile-empty"></div>'
            
    html_row += '</div>'
    st.markdown(html_row, unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================
# 🎮 유저 입력 및 게임 상태 컨트롤
# ==========================================
if not st.session_state.wordle_game_over:
    with st.form("wordle_input_form", clear_on_submit=True):
        user_guess = st.text_input("단어 입력 (예: 하늘, 구름, 수박)", max_chars=6, placeholder="정답 예측하기...").strip()
        submit_button = st.form_submit_button("제출하기 (ENTER)")
        
        if submit_button:
            guess_decomposed = decompose_hangul(user_guess)
            
            if len(guess_decomposed) != 5:
                st.warning(f"⚠️ 5칸 자모음 규격에 맞지 않습니다! 입력하신 단어는 분해 시 {len(guess_decomposed)}칸입니다. (예: 하+ㄴ+ㅡ+ㄹ = 5칸)")
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
    if st.session_state.wordle_won:
        st.success(f"🎉 대단합니다! {len(st.session_state.wordle_guesses)}번째 시도 만에 정답 [{st.session_state.wordle_secret}]을 맞히셨습니다!")
    else:
        st.error(f"😢 아쉽습니다! 모든 기회를 소진하셨습니다. 정답은 💡 [{st.session_state.wordle_secret}] 이었습니다.")
        
    # --- 🔗 💡 국어사전 연동 버튼 마크다운 추가 ---
    st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="https://ko.dict.naver.com/#/search?query={st.session_state.wordle_secret}" target="_blank" 
               style="background-color: #538d4e; color: white; padding: 12px 25px; text-decoration: none; border-radius: 6px; font-family: 'NeoDunggeunmo', sans-serif; font-size: 1.1rem; display: inline-block; border: 2px solid #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
               📖 [{st.session_state.wordle_secret}] 단어 뜻 확인하기 (국어사전)
            </a>
        </div>
    """, unsafe_allow_html=True)
    # ---------------------------------------------
        
    if st.button("🔄 다음 단어 도전하기"):
        reset_wordle()
        st.rerun()
