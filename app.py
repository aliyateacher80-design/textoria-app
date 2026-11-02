import streamlit as st
import pandas as pd
from datetime import datetime

# --- БЕТ ӨЛШЕМДЕРІ ЖӘНЕ СТАЙЛИНГ ---
st.set_page_config(
    page_title="TEXTORIA — Reading Literacy (NIS Prep)",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS СТИЛЬДЕРІ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        color: #f8fafc;
    }

    div[data-testid="stExpander"], div.stCard, .text-card {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid #6366f1 !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(10px);
        font-size: 1.1rem;
        line-height: 1.7;
        color: #ffffff !important;
    }

    .stMarkdown, p, span, label, div[data-baseweb="radio"] div, div[data-baseweb="select"] div {
        color: #ffffff !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 12px 28px !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ИНИЦИАЛИЗАЦИЯСЫ ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'completed_texts' not in st.session_state:
    st.session_state.completed_texts = set()
if 'selected_text_id' not in st.session_state:
    st.session_state.selected_text_id = 1
if 'student_results' not in st.session_state:
    st.session_state.student_results = []
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_class' not in st.session_state:
    st.session_state.student_class = "6 «Ә»"

# --- 9 МӘТІН ЖӘНЕ ТАПСЫРМАЛАР БАЗАСЫ ---
TEXTS_DATABASE = {
    1: {
        "title": "Adeliya’s Daily Routine",
        "genre": "Personal Narrative",
        "icon": "⏰",
        "text": """
        Meet Adeliya. She's a grade 6 student at Panfilov Kazakhstani-Russian Gymnasium, 54 in Almaty. It's a big school with about 1,500 students.
        During term time, Adeliya usually follows the same routine. Her day starts early. She usually gets up at 7 o'clock...
        """,
        "quiz": [
            {"question": "1. Why does Adeliya have lunch with her grandma after school?", "options": ["A) Because her parents are at school.", "B) Because her grandma meets her after school.", "C) Because she doesn't like eating at school.", "D) Because her friends invite her."], "answer": "B) Because her grandma meets her after school.", "explanation": "Her grandma meets her after school."}
        ]
    },
    2: {
        "title": "Beth’s School Life and Interests",
        "genre": "Informal Letter / Blog",
        "icon": "🎾",
        "text": """
        Hi, My name’s Beth. I’m 13 years old and I’m a student at Liberty High School in Brighton...
        """,
        "quiz": [
            {"question": "1. What is the best title of this text?", "options": ["A) A Day at the Sports Centre", "B) Beth’s School Life and Interests", "C) Rafael Nadal’s Career", "D) The Best Music Groups"], "answer": "B) Beth’s School Life and Interests", "explanation": "Мәтінде Beth өзінің мектебі мен қызығушылықтарын сипаттайды."}
        ]
    }
}

# =========================================================
# --- БҮЙІРЛІК ПАНЕЛЬ (SIDEBAR) ---
# =========================================================
with st.sidebar:
    st.title("👤 Оқушы профилі")
    
    st.session_state.student_name = st.text_input("Аты-жөніңіз:", value=st.session_state.student_name, placeholder="Мысалы: Асан Әлішер")
    st.session_state.student_class = st.selectbox("Сыныбыңыз:", ["5 «А»", "5 «Ә»", "6 «А»", "6 «Ә»", "7 «А»", "7 «Ә»"])
    
    current_xp = st.session_state.xp
    level = (current_xp // 100) + 1
    
    st.markdown(f"**Деңгей:** 🎖️ {level}-деңгей")
    st.markdown(f"**XP Ұпай:** ⚡ {current_xp} XP")
    
    st.markdown("---")
    st.subheader("📚 Мәтінді таңдау")
    text_options = {text_id: f"{data['icon']} {data['title']}" for text_id, data in TEXTS_DATABASE.items()}
    selected_id = st.selectbox(
        "Мәтінді таңдаңыз:", 
        options=list(text_options.keys()), 
        format_func=lambda x: text_options[x],
        label_visibility="collapsed"
    )
    st.session_state.selected_text_id = selected_id
    
    st.markdown("---")
    st.caption("Автор: Сұлтанова М.")

# =========================================================
# --- НЕГІЗГІ БЕТ ИНТЕРФЕЙСІ ЖӘНЕ МҰҒАЛІМ ПАНЕЛІ ---
# =========================================================

# Жоғарғы жаққа режимді таңдау қосамыз (Оқушы немесе Мұғалім)
mode = st.radio("Режимді таңдаңыз:", ["📖 Оқушы режимі", "👩‍🏫 Мұғалім панелі (Teacher Dashboard)"], horizontal=True)

if mode == "📖 Оқушы режимі":
    current_text = TEXTS_DATABASE[st.session_state.selected_text_id]

    st.title(f"{current_text['icon']} {current_text['title']}")
    st.markdown("«Оила. Талда. Жетістікке жет!»")

    tab1, tab2 = st.tabs(["📖 1. Мәтінді Оқу", "✍️ 2. Тест Тапсырмалары"])

    with tab1:
        st.subheader("Reading Text")
        st.markdown(f"""
        <div class="text-card">
            {current_text['text'].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("NIS Форматындағы Тест Сұрақтары")
        
        with st.form(key=f"quiz_form_{st.session_state.selected_text_id}"):
            user_answers = {}
            for i, q in enumerate(current_text["quiz"]):
                st.markdown(f"**{q['question']}**")
                user_answers[i] = st.radio(
                    label=f"Жауап {i+1}:", 
                    options=q["options"], 
                    key=f"q_{st.session_state.selected_text_id}_{i}",
                    label_visibility="collapsed"
                )
            
            submit_button = st.form_submit_button(label="🚀 Жауаптарды тексеру")

        if submit_button:
            if not st.session_state.student_name:
                st.error("⚠️ Өтініш, сол жақ панельге аты-жөніңізді енгізіңіз!")
            else:
                score = 0
                total = len(current_text["quiz"])
                for i, q in enumerate(current_text["quiz"]):
                    if user_answers[i] == q["answer"]:
                        score += 1
                
                earned_xp = score * 20
                if st.session_state.selected_text_id not in st.session_state.completed_texts:
                    st.session_state.completed_texts.add(st.session_state.selected_text_id)
                    st.session_state.xp += earned_xp
                
                # Нәтижені жалпы тізімге автоматты түрде қосу
                st.session_state.student_results.append({
                    "Оқушы аты-жөні": st.session_state.student_name,
                    "Сыныбы": st.session_state.student_class,
                    "Мәтін атауы": current_text["title"],
                    "Нәтиже": f"{score}/{total}",
                    "Жинаған XP": earned_xp,
                    "Тапсырған уақыты": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                st.balloons()
                st.success(f"🎉 Құттықтаймыз, {st.session_state.student_name}! Нәтижеңіз мұғалім базасына сәтті сақталды!")

else:
    # --- МҰҒАЛІМ ПАНЕЛІ (TEACHER DASHBOARD) ---
    st.title("👩‍🏫 Мұғалімнің басқару панелі (Teacher Dashboard)")
    st.markdown("Бұл бөлімде барлық оқушылардың тапсырған нәтижелері жинақталып көрсетіледі.")
    
    if len(st.session_state.student_results) == 0:
        st.info("📭 Әзірге ешқандай оқушы тест тапсырған жоқ немесе база тазаланған.")
    else:
        # Статистика көрсеткіштері
        df_results = pd.DataFrame(st.session_state.student_results)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Барлық тапсырулар саны", len(df_results))
        col2.metric("Қатысқан оқушылар", df_results["Оқушы аты-жөні"].nunique())
        col3.metric("Жалпы берілген XP", int(df_results["Жинаған XP"].sum()))
        
        st.markdown("### 📋 Оқушылардың нәтижелер кестесі")
        st.dataframe(df_results, use_container_width=True)
        
        st.markdown("---")
        # Базаны қажет кезде тазалау батырмасы
        if st.button("🗑️ Барлық нәтижелер базасын тазалау (Reset Database)"):
            st.session_state.student_results = []
            st.success("✅ База сәтті тазартылды!")
            st.rerun()
