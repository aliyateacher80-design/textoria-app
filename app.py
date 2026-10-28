import streamlit as st
import time

# --- БЕТ ӨЛШЕМДЕРІ ЖӘНЕ СТАЙЛИНГ ---
st.set_page_config(
    page_title="TEXTORIA — Оқылым сауаттылығы",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS СТИЛЬДЕРІ (Геймификация, анимациялар, түстер) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@600;700&family=Nunito:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* Басты градиент фоны */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        color: #f8fafc;
    }

    /* Карточкалар мен контейнерлер */
    div[data-testid="stExpander"], div.stCard, .text-card {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 2px solid #6366f1 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(10px);
    }

    /* Батырмалар стилі */
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
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6) !important;
    }

    /* Кітап сөресі карточкалары */
    .book-shelf-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #38bdf8;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        transition: transform 0.3s;
    }
    .book-shelf-card:hover {
        transform: translateY(-5px);
        border-color: #f43f5e;
    }

    /* Жетістік бейдждері */
    .badge-box {
        display: inline-block;
        background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
        color: #78350f;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.9rem;
        margin: 5px;
        box-shadow: 0 4px 10px rgba(251, 191, 36, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ SESSION STATE (Оқушы прогресін сақтау) ---
if 'xp' not in st.session_state:
    st.session_state.xp = 120
if 'level' not in st.session_state:
    st.session_state.level = 2
if 'completed_texts' not in st.session_state:
    st.session_state.completed_texts = set()
if 'current_view' not in st.session_state:
    st.session_state.current_view = "bookcase"
if 'selected_text_id' not in st.session_state:
    st.session_state.selected_text_id = 1
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "text"

# --- ДЕРЕКТЕР БАЗАСЫ (МӘТІНДЕР, ТЕСТТЕР ЖӘНЕ СӘЙКЕС ТАПСЫРМАЛАР) ---
TEXTS_DATABASE = {
    1: {
        "title": "Марсқа саяхат және болашақ колониясы",
        "genre": "Ғылыми-фантастика",
        "icon": "🚀",
        "text": """
        2045 жылы Адамзат Марс ғаламшарында алғашқы тұрақты колониясын құрды. Бұл миссияның негізгі мақсаты — басқа ғаламшарда өмір сүру мүмкіндіктерін зерттеу болатын. Марстағы атмосфера негізінен көмірқұшық газынан тұрады, ал температура 0-ден кейде минус 120 градусқа дейін төмендейді. 
        
        Ғалымдар өсімдіктерді өсіру үшін арнайы био-күмбездер (Bio-domes) салып, онда атмосфералық қысым мен оттегі деңгейін Жердегідей қалыпқа келтірді. Су мәселесі Марстың полюстеріндегі мұздықтарды ерткізу арқылы шешілуде. Оқушылар мен зерттеушілер бұл миссияның болашақта басқа да ғаламшарларды игеруге жол ашатынына сенеді.
        """,
        "quiz": [
            {
                "question": "1. Марстағы колония қай жылы құрылды?",
                "options": ["2035 жыл", "2045 жыл", "2050 жыл", "2040 жыл"],
                "answer": "2045 жыл"
            },
            {
                "question": "2. Марста өсімдіктерді өсіру үшін не қолданылды?",
                "options": ["Ашық жылыжайлар", "Гидропоника", "Био-күмбездер", "Марс топырағы"],
                "answer": "Био-күмбездер"
            },
            {
                "question": "3. Марста су мәселесі қалай шешілуде?",
                "options": ["Жерден тасымалдау", "Мұздықтарды ерткізу", "Жаңбыр суын жинау", "Жасанды су жасау"],
                "answer": "Мұздықтарды ерткізу"
            }
        ],
        "matching": {
            "Био-күмбез": "Өсімдік өсіруге арналған жабық кешен",
            "Марс атмосферасы": "Негізінен көмірқұшық газынан тұрады",
            "Су көзі": "Полюстердегі мұздықтар",
            "Миссия мақсаты": "Басқа ғаламшарда өмір сүруді зерттеу"
        }
    },
    2: {
        "title": "Жасанды Интеллект және Болашақ Мамандықтары",
        "genre": "Технология",
        "icon": "🤖",
        "text": """
        Жасанды интеллект (ЖИ) заманауи әлемде қарқынды дамып келеді. Ол үлкен көлемдегі деректерді талдауға, күрделі есептерді шешуге және тіпті шығармашылық тапсырмаларды орындауға қабілетті. Алайда, ЖИ адамның эмоциясын, эмоционалды интеллектін және терең сыни ойлауын толық алмастыра алмайды.
        
        Болашақта көптеген рутиналық мамандықтар жойылғанымен, ЖИ жүйелерін басқаратын, этикалық шекараларды белгілейтін және деректерді сараптайтын жаңа мамандықтар пайда болады. Сонымен бірге, оқылым сауаттылығы мен логикалық талдау кез келген мамандық үшін негізгі дағды болып қала береді.
        """,
        "quiz": [
            {
                "question": "1. Жасанды интеллект адамның қай қасиетін толық алмастыра алмайды?",
                "options": ["Деректерді есептеуді", "Эмоционалды интеллектті", "Жылдам ақпарат табуды", "Мәтінді аударуды"],
                "answer": "Эмоционалды интеллектті"
            },
            {
                "question": "2. Мәтінге сәйкес, болашақта қандай мамандықтар пайда болады?",
                "options": ["ЖИ жүйелерін басқаратын мамандықтар", "Тек механикалық жұмысшылар", "Қағазбен жұмыс істейтін мамандар", "Тек робототехника мұғалімдері"],
                "answer": "ЖИ жүйелерін басқаратын мамандықтар"
            }
        ],
        "matching": {
            "ЖИ қабілеті": "Үлкен көлемдегі деректерді талдау",
            "Адам артықшылығы": "Эмоционалды интеллект пен сыни ойлау",
            "Болашақ дағдысы": "Оқылым сауаттылығы мен логика"
        }
    }
}

# --- БАҚЫЛАУ ПАНЕЛІ (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🛡️ **ОҚУШЫ ПРОФИЛІ**")
    st.markdown(f"**Деңгей:** 🏆 `{st.session_state.level}-деңгей (Зерттеуші)`")
    st.markdown(f"**XP Ұпай:** ⚡ `{st.session_state.xp} XP`")
    
    # XP прогресс бар
    progress = (st.session_state.xp % 100) / 100
    st.progress(progress)
    st.caption(f"Келесі деңгейге: {100 - (st.session_state.xp % 100)} XP қалды")

    st.markdown("---")
    st.markdown("### 🏅 **Жетістіктер**")
    st.markdown('<span class="badge-box">🔍 Оқылым шебері</span>', unsafe_allow_html=True)
    st.markdown('<span class="badge-box">⚡ Жылдам талдаушы</span>', unsafe_allow_html=True)
    if len(st.session_state.completed_texts) > 0:
        st.markdown('<span class="badge-box">🎯 Бірінші Жеңіс</span>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("📚 Кітап Сөресіне оралу", use_container_width=True):
        st.session_state.current_view = "bookcase"
        st.rerun()

# --- НЕГІЗГІ ХЕДЕР ---
st.markdown("<h1 style='text-align: center; color: #818cf8; font-family: Comfortaa;'>✨ TEXTORIA ✨</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #cbd5e1;'>«Ойла. Талда. Жетістікке жет!»</h4>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================================
# VIEW 1: BOOKCASE (КІТАП СӨРЕСІ)
# =====================================================================
if st.session_state.current_view == "bookcase":
    st.subheader("📚 Кітап Сөресі (Мәтіндерді таңдаңыз)")
    st.info("💡 Дарынды мектептерге іріктеуге дайындалу үшін мәтінді таңдап, талдау тапсырмаларын орындаңыз!")

    cols = st.columns(2)
    for idx, (t_id, data) in enumerate(TEXTS_DATABASE.items()):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="book-shelf-card">
                <h2>{data['icon']} {data['title']}</h2>
                <p><b>Жанры:</b> {data['genre']}</p>
                <p><i>6-сынып оқылым сауаттылығы тапсырмасы</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            is_done = t_id in st.session_state.completed_texts
            btn_label = "✅ Орындалды (Қайталау)" if is_done else "🚀 Мәтінді Оқу және Тапсырмалар"
            
            if st.button(btn_label, key=f"select_{t_id}", use_container_width=True):
                st.session_state.selected_text_id = t_id
                st.session_state.current_view = "workspace"
                st.rerun()

# =====================================================================
# VIEW 2: WORKSPACE (МӘТІН, ТЕСТ ЖӘНЕ СӘЙКЕС ТАПСЫРМА)
# =====================================================================
elif st.session_state.current_view == "workspace":
    current_data = TEXTS_DATABASE[st.session_state.selected_text_id]
    
    st.markdown(f"### {current_data['icon']} {current_data['title']}")
    
    # Батырмалар/Табтар арқылы ауысу
    tab1, tab2, tab3 = st.tabs(["📖 1. Мәтінді Оқу", "📝 2. Тест Тапсырмалары", "🔗 3. Сәйкестендіру"])

    # ------------------ TAB 1: МӘТІН ------------------
    with tab1:
        st.markdown('<div class="text-card">', unsafe_allow_html=True)
        st.markdown(current_data['text'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.success("👉 Мәтінді оқып болсаңыз, жоғарыдағы **«2. Тест Тапсырмалары»** немесе **«3. Сәйкестендіру»** табына өтіңіз!")

    # ------------------ TAB 2: ТЕСТ ------------------
    with tab2:
        st.subheader("📝 Мәтін бойынша тест")
        st.caption("Әрбір дұрыс жауап үшін +15 XP беріледі!")
        
        user_answers = {}
        with st.form("quiz_form"):
            for q_idx, q in enumerate(current_data['quiz']):
                st.markdown(f"**{q['question']}**")
                user_answers[q_idx] = st.radio(
                    "Жауапты таңдаңыз:",
                    q['options'],
                    key=f"q_{st.session_state.selected_text_id}_{q_idx}",
                    index=None
                )
                st.markdown("---")
            
            submit_quiz = st.form_submit_button("🎯 Тест Жауаптарын Тексеру")

        if submit_quiz:
            score = 0
            total = len(current_data['quiz'])
            
            for q_idx, q in enumerate(current_data['quiz']):
                if user_answers[q_idx] == q['answer']:
                    score += 1

            gained_xp = score * 15
            st.session_state.xp += gained_xp
            
            # Нәтижені визуалды көрсету
            st.balloons()
            st.markdown(f"### 📊 Сіздің нәтижеңіз: **{score} / {total}** ({int(score/total*100)}%)")
            st.info(f"⚡ Тамаша! Сіз **+{gained_xp} XP** ұпай жинадыңыз!")
            
            # Автоматты Кері Байланыс (Feedback)
            pct = score / total
            if pct == 1.0:
                st.success("🌟 **Керемет!** Мәтінді толықтай түсінгенің көрініп тұр. Талдау қабілетің өте жоғары!")
            elif pct >= 0.5:
                st.warning("👍 **Жақсы нәтиже!** Бірақ кейбір детальдарға қайта назар аударғаның жөн.")
            else:
                st.error("💡 **Қайталап оқыған жөн!** Мәтінді тағы бір рет мұқият оқып шығып, қайта тапсырып көр.")

    # ------------------ TAB 3: СӘЙКЕС ТАПСЫРМА ------------------
    with tab3:
        st.subheader("🔗 Ұғымдар мен Анықтамаларды Сәйкестендіру")
        st.caption("Сол жақтағы ұғымға оң жақтағы дұрыс анықтамасын таңдаңыз:")
        
        matching_data = current_data['matching']
        left_items = list(matching_data.keys())
        right_options = list(matching_data.values())
        
        user_matching = {}
        with st.form("matching_form"):
            for item in left_items:
                st.markdown(f"📌 **{item}**")
                user_matching[item] = st.selectbox(
                    "Сәйкес анықтамасын таңдаңыз:",
                    ["-- Таңдаңыз --"] + right_options,
                    key=f"match_{st.session_state.selected_text_id}_{item}"
                )
                st.write("")

            submit_match = st.form_submit_button("✅ Сәйкестікті Тексеру")

        if submit_match:
            correct_count = 0
            for item, correct_val in matching_data.items():
                if user_matching[item] == correct_val:
                    correct_count += 1
            
            total_match = len(matching_data)
            if correct_count == total_match:
                st.balloons()
                st.success(f"🎉 **Тамаша!** Барлық {total_match} сәйкестік дұрыс табылды! (+30 XP)")
                st.session_state.xp += 30
                st.session_state.completed_texts.add(st.session_state.selected_text_id)
            else:
                st.warning(f"🎯 Сіз **{correct_count} / {total_match}** сәйкестікті таптыңыз. Қайта байқап көріңіз!")
