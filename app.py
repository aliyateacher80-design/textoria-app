import streamlit as st
import pandas as pd
from datetime import datetime

# --- БЕТ ӨЛШЕМДЕРІ ЖӘНЕ СТАЙЛИНГ ---
st.set_page_config(
    page_title="TEXTORIA — Reading Literacy (NIS Prep)",
    page_icon="📚",
    layout="wide"
)

# --- CSS СТИЛЬДЕРІ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@600;700&family=Nunito:wght@400;600;800&display=swap');

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
        padding: 10px 20px !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6) !important;
    }

    .book-shelf-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #38bdf8;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2);
    }
    
    .top-panel {
        background: rgba(30, 41, 59, 0.9);
        border: 2px solid #6366f1;
        border-radius: 15px;
        padding: 15px 20px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ИНИЦИАЛИЗАЦИЯСЫ ---
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'completed_texts' not in st.session_state:
    st.session_state.completed_texts = set()
if 'current_view' not in st.session_state:
    st.session_state.current_view = "bookcase"
if 'selected_text_id' not in st.session_state:
    st.session_state.selected_text_id = 1
if 'student_results' not in st.session_state:
    st.session_state.student_results = []
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'student_class' not in st.session_state:
    st.session_state.student_class = "5 «Ә»"

# --- 9 МӘТІН ЖӘНЕ ТАПСЫРМАЛАР БАЗАСЫ ---
TEXTS_DATABASE = {
    1: {
        "title": "Adeliya’s Daily Routine",
        "genre": "Personal Narrative",
        "icon": "⏰",
        "text": """
        Adeliya is a student studying at a gymnasium in Almaty. During the school term, she follows a structured daily routine. Her day begins early in the morning around 7 o'clock. After getting ready, her grandmother accompanies her to school on foot.
        She usually attends six lessons daily, with Kazakh being her favorite subject. At mid-morning, she has a break to enjoy snacks with classmates. When school ends at 2 p.m., her grandmother meets her to return home together. 
        In the afternoons, Adeliya focuses on her homework and preparation for upcoming classes. Three times a week, she attends music school to participate in choir practice. Even with a busy schedule, she finds time to help her family and spend evenings walking with friends and her brother Dias.
        """,
        "quiz": [
            {"question": "1. Why does Adeliya walk home with her grandma after school?", "options": ["A) Because her parents are at school.", "B) Because her grandma meets her after school.", "C) Because she doesn't like eating at school.", "D) Because her friends invite her."], "answer": "B) Because her grandma meets her after school.", "explanation": "Her grandma meets her after school."},
            {"question": "2. Which activity does Adeliya do three days a week?", "options": ["A) She plays basketball.", "B) She learns Kazakh.", "C) She attends music school.", "D) She goes shopping."], "answer": "C) She attends music school.", "explanation": "She attends music school three days a week."},
            {"question": "3. What can we understand about Adeliya from the text?", "options": ["A) She doesn't enjoy studying.", "B) She is hardworking and has a busy routine.", "C) She never helps her family.", "D) She always gets up late."], "answer": "B) She is hardworking and has a busy routine.", "explanation": "She is hardworking and has a busy routine."},
            {"question": "4. What does Adeliya usually do after lunch?", "options": ["A) She watches television all afternoon.", "B) She goes to the park alone.", "C) She does her homework and prepares for the next day.", "D) She goes straight to music school every day."], "answer": "C) She does her homework and prepares for the next day.", "explanation": "She does her homework and prepares for the next day."},
            {"question": "5. Which statement best describes Adeliya's daily life?", "options": ["A) She spends most of her day playing computer games.", "B) She balances school, homework, music and family time.", "C) She only studies and never meets her friends.", "D) She dislikes spending time with her family."], "answer": "B) She balances school, homework, music and family time.", "explanation": "She balances school, homework, music and family time."}
        ],
        "matching": {"7 o'clock": "Adeliya gets up", "11 a.m.": "Brunch with classmates", "2 p.m.": "School finishes and grandma meets her", "3 days a week": "Attends music school (choir practice)", "10 p.m.": "Adeliya goes to bed"}
    },
    2: {
        "title": "Beth’s School Life and Interests",
        "genre": "Informal Letter / Blog",
        "icon": "🎾",
        "text": """
        Beth is a 13-year-old student attending high school in Brighton. She enjoys her classes and works diligently alongside her classmates. While academic lessons are shared, sports lessons differ between boys and girls. Beth has a strong passion for sports, particularly basketball and tennis, admiring players like Rafael Nadal. However, she dislikes football. Her absolute favorite subject is music, guided by an enthusiastic pop-loving teacher.
        """,
        "quiz": [
            {"question": "1. What is the best title of this text?", "options": ["A) A Day at the Sports Centre", "B) Beth’s School Life and Interests", "C) Rafael Nadal’s Career", "D) The Best Music Groups"], "answer": "B) Beth’s School Life and Interests", "explanation": "Beth describes her school life, sports, and music interests."},
            {"question": "2. What is the main idea of this text?", "options": ["A) Beth describes her school, favourite subjects and sports interests.", "B) Beth explains how to become a tennis player.", "C) Beth talks only about her music teacher.", "D) Beth describes her school holidays."], "answer": "A) Beth describes her school, favourite subjects and sports interests.", "explanation": "The text focuses on her daily school experiences and hobbies."},
            {"question": "3. Which part of the text tells us how Beth plays tennis?", "options": ["A) The first paragraph, where she talks about sports lessons and summer.", "B) The part where she introduces herself.", "C) The part where she describes her music teacher.", "D) The final greeting."], "answer": "A) The first paragraph, where she talks about sports lessons and summer.", "explanation": "She mentions playing tennis during games lessons in summer."},
            {"question": "4. Which word is missing? Beth is really into basketball and tennis, but she ______ football.", "options": ["A) loves", "B) enjoys", "C) hates", "D) plays"], "answer": "C) hates", "explanation": "Beth states she hates football."},
            {"question": "5. What does the sentence “I’m really into basketball and tennis” mean?", "options": ["A) Beth watches basketball and tennis on TV every day.", "B) Beth is very interested in basketball and tennis.", "C) Beth doesn't understand basketball and tennis.", "D) Beth teaches basketball and tennis."], "answer": "B) Beth is very interested in basketball and tennis.", "explanation": "Being into something means being very interested in it."}
        ],
        "matching": {"Liberty High School": "Beth's school in Brighton", "Rafael Nadal": "Beth's favourite tennis player", "Football": "The sport Beth hates", "Music": "Beth's favourite lesson", "Be really into": "To be very interested in something"}
    },
    3: {
        "title": "Almaty — Home to Many Nationalities",
        "genre": "Informative Article",
        "icon": "🏙️",
        "text": """
        Almaty stands as Kazakhstan's largest urban center, accommodating nearly two million residents. Approximately half of the population consists of ethnic Kazakhs, while the other half represents diverse cultural backgrounds and ancestral roots from regions such as Russia, China, Ukraine, and Korea. This multicultural blend creates a rich community fabric.
        """,
        "quiz": [
            {"question": "1. How many people live in Almaty?", "options": ["A) Almost 1 million", "B) Almost 2 million", "C) Almost 3 million", "D) Almost 5 million"], "answer": "B) Almost 2 million", "explanation": "Almaty has almost 2 million people."},
            {"question": "2. Approximately what percentage of Almaty’s population is Kazakh?", "options": ["A) 25%", "B) 30%", "C) 50%", "D) 75%"], "answer": "C) 50%", "explanation": "Around 50% of them are Kazakh."},
            {"question": "3. Where do around a third of the people in Almaty have family roots?", "options": ["A) Russia", "B) China", "C) Korea", "D) Ukraine"], "answer": "A) Russia", "explanation": "Around a third have families from Russia."},
            {"question": "4. Almaty is the ______ city in Kazakhstan.", "options": ["A) oldest", "B) smallest", "C) biggest", "D) newest"], "answer": "C) biggest", "explanation": "Almaty is the biggest city."},
            {"question": "5. Which countries are mentioned in the text as places where residents’ families come from?", "options": ["A) Russia, China, Korea and Ukraine", "B) France, Italy, Spain and Germany", "C) Japan, India, Egypt and Turkey", "D) Canada, Australia, Brazil and Mexico"], "answer": "A) Russia, China, Korea and Ukraine", "explanation": "China, Korea, Ukraine and Russia are mentioned."}
        ],
        "matching": {"Biggest city": "Almaty", "Almost 2 million": "Population of Almaty", "50%": "Percentage of Kazakh population in Almaty", "Around a third": "People with family roots from Russia", "China, Korea, Ukraine": "Other countries mentioned in the text"}
    },
    4: {
        "title": "My Day (Darby in India)",
        "genre": "Autobiography / Blog",
        "icon": "🤝",
        "text": """
        Darby works as a volunteer teacher at a school in India, primarily teaching English and occasionally geography. The school day begins with physical exercises to help students relax and focus. Despite lacking modern equipment, the students demonstrate a strong desire to learn because they value education. Local mothers frequently join classes as well. Darby concludes work at midday to lunch with friends, spend afternoons preparing lessons, and socialize with villagers.
        """,
        "quiz": [
            {"question": "1. What is Darby’s job at the school?", "options": ["A) She is a doctor.", "B) She is a volunteer.", "C) She is a student.", "D) She is a school director."], "answer": "B) She is a volunteer.", "explanation": "She is a volunteer at a school."},
            {"question": "2. Which subjects does Darby sometimes teach?", "options": ["A) English and geography", "B) Maths and science", "C) History and English", "D) Geography and art"], "answer": "A) English and geography", "explanation": "She teaches English and sometimes geography."},
            {"question": "3. Why do the students start the day with exercise?", "options": ["A) To prepare for a sports competition.", "B) To help them relax and focus.", "C) To make them tired.", "D) To learn geography."], "answer": "B) To help them relax and focus.", "explanation": "It helps everyone relax and focus."},
            {"question": "4. The school is old and it doesn’t have ______.", "options": ["A) any students", "B) any teachers", "C) new equipment", "D) any classrooms"], "answer": "C) new equipment", "explanation": "It doesn't have new equipment."},
            {"question": "5. Why do the children want to learn?", "options": ["A) They think education is important in life.", "B) They want to leave the village.", "C) They want to become teachers immediately.", "D) Their school has new equipment."], "answer": "A) They think education is important in life.", "explanation": "They know education is important in life."}
        ],
        "matching": {"Darby": "Volunteer teacher in India", "Morning exercise": "Helps students relax and focus", "Mothers of children": "Come to school to learn too", "Till midday": "Darby's working hours", "Afternoon": "Lesson preparation and meeting village friends"}
    },
    5: {
        "title": "Danger! Humans!",
        "genre": "Environmental Science",
        "icon": "🐅",
        "text": """
        While media often highlights dangerous animal attacks, human actions pose a far greater threat to global wildlife. Millions of sharks and other animals are affected annually due to human consumption, commercial hunting, and habitat destruction. In Kazakhstan, red-listed species face dangers from pollution and urban expansion. Protecting habitats and modifying human behavior is essential to prevent extinctions.
        """,
        "quiz": [
            {"question": "1. What is the main idea of the text?", "options": ["A) Animals are more dangerous than humans.", "B) Humans harm animals, and we need to protect them.", "C) Animals should live only in zoos.", "D) People should stop eating fish."], "answer": "B) Humans harm animals, and we need to protect them.", "explanation": "Humans cause harm to animals and action is needed."},
            {"question": "2. Which paragraph explains why some animal species are disappearing?", "options": ["A) The paragraph about animal attacks in the news.", "B) The paragraph about the number of sharks killed.", "C) The paragraph about pollution, construction and changes to habitats.", "D) The paragraph about people eating meat."], "answer": "C) The paragraph about pollution, construction and changes to habitats.", "explanation": "Habitat changes drive extinction."},
            {"question": "3. Which word best completes the sentence? People sometimes kill animals for food, fur or ______.", "options": ["A) fun", "B) education", "C) transport", "D) medicine"], "answer": "A) fun", "explanation": "Hunted for fur or for fun."},
            {"question": "4. What does the phrase “time is running out for some animals” mean?", "options": ["A) Animals are moving to different places.", "B) Some animals may disappear soon.", "C) Animals need more time to hunt.", "D) Animals are becoming faster."], "answer": "B) Some animals may disappear soon.", "explanation": "Refers to imminent extinction risks."},
            {"question": "5. What does the word “our” refer to in the phrase “our pollution and construction”?", "options": ["A) Animals", "B) Humans", "C) Scientists", "D) Newspapers"], "answer": "B) Humans", "explanation": "Refers to human actions."}
        ],
        "matching": {"100 million": "Sharks killed by humans every year", "Kazakhstan Red List": "Includes leopards, lynx, bears and otters", "Habitat destruction": "Caused by human pollution and construction", "Extinct": "Animals disappearing completely from Earth", "Time is running out": "Some animals may disappear very soon"}
    },
    6: {
        "title": "Altyn-Emel National Park",
        "genre": "Geography & Nature",
        "icon": "⛰️",
        "text": """
        Spanning 4,600 square kilometers in southeast Kazakhstan, Altyn-Emel National Park features diverse ecosystems, rare bird species, singing sand dunes, and ancient archaeological artifacts. Despite arid conditions, it hosts rich flora and fauna, making it an exceptional destination for nature lovers and researchers.
        """,
        "quiz": [
            {"question": "1. What makes Altyn-Emel National Park special despite its dry environment?", "options": ["A) It has many shopping centres.", "B) It has a rich variety of plants, fish and animals.", "C) It receives heavy rainfall every day.", "D) It has no endangered species."], "answer": "B) It has a rich variety of plants, fish and animals.", "explanation": "Rich wildlife and plant species."},
            {"question": "2. Which geographical features surround the park?", "options": ["A) The River Ili and the Aktau Mountains", "B) The Caspian Sea and the Altai Mountains", "C) The River Irtysh and the Tian Shan Mountains", "D) The Aral Sea and the Khangai Mountains"], "answer": "A) The River Ili and the Aktau Mountains", "explanation": "Lies between River Ili and Aktau Mountains."},
            {"question": "3. How many species of plants are found in the park?", "options": ["A) Around 260", "B) 32", "C) Around 1,800", "D) 11"], "answer": "C) Around 1,800", "explanation": "Around 1,800 species of plants."},
            {"question": "4. Why is the park a paradise for birdwatchers?", "options": ["A) It has many rare birds, including four types of eagle.", "B) All birds in Kazakhstan live there.", "C) Visitors can feed the eagles.", "D) It is the only place with birds in Kazakhstan."], "answer": "A) It has many rare birds, including four types of eagle.", "explanation": "Features four types of eagle and rare birds."},
            {"question": "5. What causes the singing sand dunes to make a sound?", "options": ["A) Birds sing above the dunes.", "B) Water flows under the sand.", "C) The wind moves the sand.", "D) People walk across the dunes."], "answer": "C) The wind moves the sand.", "explanation": "Wind moving the sand creates the sound."}
        ],
        "matching": {"4,600 km2": "Total area of Altyn-Emel National Park", "1,800 species": "Plant species found in the park", "Four types of eagle": "Imperial, golden eagles and other rare birds", "Singing dunes": "3 km long, 500 m high sand dunes", "Wind moving sand": "Makes a sound like an organ"}
    },
    7: {
        "title": "Asanaly Ashimov",
        "genre": "Biography & Culture",
        "icon": "🎭",
        "text": """
        Asanaly Ashimov is a renowned figure in Kazakh theatre and cinema. Starting his film career while studying at the conservatory, he joined the M. Auezov theatre troupe and gained fame through iconic stage and movie roles. Later, he expanded his artistic contributions by directing successful films and mentoring upcoming generations.
        """,
        "quiz": [
            {"question": "1. When did Ashimov first appear in a film?", "options": ["A) After becoming a director", "B) After graduating from university", "C) While he was still a student", "D) After joining the theatre troupe"], "answer": "C) While he was still a student", "explanation": "Appeared in his first film while a student."},
            {"question": "2. What does the word “troupe” mean in the fourth paragraph?", "options": ["A) A group of actors who perform together", "B) A school for young musicians", "C) A company that produces books", "D) A building where films are shown"], "answer": "A) A group of actors who perform together", "explanation": "A theatrical group of actors."},
            {"question": "3. What does the word “This” refer to in the sentence “This is a historic thriller and an extremely successful Kazakh film”?", "options": ["A) Kyz-Zhibek", "B) The End of Ataman", "C) The Year of the Dragon", "D) Kozy Korpesh"], "answer": "B) The End of Ataman", "explanation": "Refers to The End of Ataman."},
            {"question": "4. Which statement about Ashimov is correct according to the text?", "options": ["A) He worked only in cinema.", "B) He became a director before becoming an actor.", "C) He performed the role of Dr Clausen over 100 times.", "D) He studied drama in a village."], "answer": "C) He performed the role of Dr Clausen over 100 times.", "explanation": "Performed Dr Clausen over 100 times."},
            {"question": "5. Which of the following films was directed by Ashimov?", "options": ["A) Kyz-Zhibek", "B) The End of Ataman", "C) The Year of the Dragon", "D) Blood and Sweat"], "answer": "C) The Year of the Dragon", "explanation": "His first directed film was The Year of the Dragon."}
        ],
        "matching": {"1958": "First film appearance while a student", "M. Auezov troupe": "Joined after graduation to act on stage", "Dr Clausen": "Role in Before Sunset performed over 100 times", "The End of Ataman": "1972 historic thriller film", "The Year of the Dragon": "His first directed film in 1984"}
    },
    8: {
        "title": "The Internet",
        "genre": "Technology & History",
        "icon": "🌐",
        "text": """
        Originating in 1969 as ARPANET for academic communication, the internet evolved significantly through major milestones like Ray Tomlinson's email innovation and Tim Berners-Lee's creation of the World Wide Web. Today, modern search engines and mobile connectivity make web access ubiquitous, fundamentally reshaping modern daily life.
        """,
        "quiz": [
            {"question": "1. What is the main idea of the text?", "options": ["A) The history and development of the internet", "B) The invention of smartphones", "C) The life of famous scientists", "D) The history of computer games"], "answer": "A) The history and development of the internet", "explanation": "Traces the evolution and history of the internet."},
            {"question": "2. What was the internet originally used for?", "options": ["A) Watching videos and playing games", "B) Buying music and downloading books", "C) Sharing ideas and information between universities", "D) Sending messages on social media"], "answer": "C) Sharing ideas and information between universities", "explanation": "Used by universities to share ideas and information."},
            {"question": "3. Which event happened first?", "options": ["A) Tim Berners-Lee invented the World Wide Web.", "B) Ray Tomlinson sent the first email.", "C) Google became popular.", "D) ARPANET started in the USA."], "answer": "D) ARPANET started in the USA.", "explanation": "Started in 1969."},
            {"question": "4. What does the word “enormous” mean in the second paragraph?", "options": ["A) Very expensive", "B) Very large", "C) Very modern", "D) Very fast"], "answer": "B) Very large", "explanation": "Enormous means very large."},
            {"question": "5. What does the word “these” refer to in the sentence “Lycos was one of the first of these”?", "options": ["A) Universities", "B) Websites", "C) Search engines", "D) Computers"], "answer": "C) Search engines", "explanation": "Refers to search engines."}
        ],
        "matching": {"1969": "ARPANET started in the USA", "Ray Tomlinson": "Sent the first email in 1971 using @", "Tim Berners-Lee": "Invented the World Wide Web in 1989", "info.cern.ch": "First website created in Switzerland", "Lycos": "One of the early search engines"}
    },
    9: {
        "title": "Almaty Marathon",
        "genre": "Sport & Community",
        "icon": "🏃‍♂️",
        "text": """
        Established to encourage healthier active lifestyles, the Almaty Marathon has grown into a major international sporting event since 2012. Besides promoting physical endurance and community engagement, the marathon serves a charitable purpose by raising funds to support sports programs for disabled children.
        """,
        "quiz": [
            {"question": "1. Why is it important to train for several months before running a marathon?", "options": ["A) Because it is impossible to run 42 km without preparation.", "B) Because volunteers will not help untrained runners.", "C) Because only professionals are allowed to run.", "D) Because the route changes every month."], "answer": "A) Because it is impossible to run 42 km without preparation.", "explanation": "Requires months of training for 42 km."},
            {"question": "2. When was the first Almaty Marathon held?", "options": ["A) 2010", "B) 2012", "C) 2015", "D) 2020"], "answer": "B) 2012", "explanation": "Started in 2012."},
            {"question": "3. What is one charity goal of the Almaty Marathon?", "options": ["A) To build new roads in Almaty", "B) To raise money for disabled children to do sport", "C) To pay professional athletes", "D) To buy running shoes for all participants"], "answer": "B) To raise money for disabled children to do sport", "explanation": "Raises money for disabled children."},
            {"question": "4. Who can volunteer at the marathon?", "options": ["A) Only professional runners", "B) Only people born in Almaty", "C) Anyone with a lot of energy", "D) Only students"], "answer": "C) Anyone with a lot of energy", "explanation": "Anyone can volunteer with enough energy."},
            {"question": "5. What is the main reason organizers created the marathon?", "options": ["A) To sell sportswear", "B) To promote healthier lifestyles", "C) To invite famous celebrities", "D) To close main roads for a day"], "answer": "B) To promote healthier lifestyles", "explanation": "Promote healthier lifestyles."}
        ],
        "matching": {"2012": "First Almaty Marathon held with 2,500 runners", "2015": "Number of runners increased to 19,000", "42 km": "Distance of the main marathon race", "Disabled children": "Group for which the event raises money", "Volunteers": "Give runners food, drink and direction"}
    }
}

# =========================================================
# --- ЖОТАРҒЫ БӨЛІК: ОҚУШЫ ПРОФИЛІ ЖӘНЕ БАСҚАРУ МӘЗІРІ ---
# =========================================================
st.markdown('<div class="top-panel">', unsafe_allow_html=True)
col_p1, col_p2, col_p3, col_p4 = st.columns([2, 1, 1, 1])

with col_p1:
    st.session_state.student_name = st.text_input("👤 Оқушының аты-жөні:", value=st.session_state.student_name, placeholder="Мысалы: Асан Әлішер")

with col_p2:
    st.session_state.student_class = st.selectbox("🏫 Сыныбы:", ["5 «А»", "5 «Ә»", "6 «А»", "6 «Ә»", "7 «А»", "7 «Ә»"])

with col_p3:
    current_xp = st.session_state.xp
    level = (current_xp // 100) + 1
    st.markdown(f"**Деңгей:** 🏆 {level}-деңгей")
    st.markdown(f"**XP Ұпай:** ⚡ {current_xp} XP")

with col_p4:
    completed_count = len(st.session_state.completed_texts)
    st.markdown(f"**Орындалған:** {completed_count}/9 мәтін")

st.markdown("---")

# Навигация батырмалары
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("📚 Кітап Сөресі", use_container_width=True):
        st.session_state.current_view = "bookcase"
        st.rerun()
with nav_col2:
    if st.button("📊 Мұғалім панелі (Dashboard)", use_container_width=True):
        st.session_state.current_view = "dashboard"
        st.rerun()
with nav_col3:
    if st.button("🗑️ Базаны тазалау", use_container_width=True):
        st.session_state.student_results = []
        st.session_state.completed_texts = set()
        st.session_state.xp = 0
        st.success("База сәтті тазартылды!")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# --- НЕГІЗГІ БЕТ ИНТЕРФЕЙСІ ---
# =========================================================
if st.session_state.current_view == "bookcase":
    st.title("📚 TEXTORIA — Кітап сөресі (Bookcase)")
    st.markdown("«Ойла. Талда. Жетістікке жет!» Оқу үшін төмендегі мәтіндердің бірін таңдаңыз:")
    st.markdown("---")
    
    cols = st.columns(3)
    for idx, (text_id, data) in enumerate(TEXTS_DATABASE.items()):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class="book-shelf-card">
                <h2>{data['icon']}</h2>
                <h4>{data['title']}</h4>
                <p><b>Жанр:</b> {data['genre']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"📖 Мәтінді ашу #{text_id}", key=f"book_btn_{text_id}", use_container_width=True):
                st.session_state.selected_text_id = text_id
                st.session_state.current_view = "reader"
                st.rerun()

elif st.session_state.current_view == "reader":
    current_text = TEXTS_DATABASE[st.session_state.selected_text_id]
    
    if st.button("⬅️ Кітап сөресіне қайту"):
        st.session_state.current_view = "bookcase"
        st.rerun()

    st.title(f"{current_text['icon']} {current_text['title']}")
    st.markdown("«Ойла. Талда. Жетістікке жет!»")

    tab1, tab2, tab3 = st.tabs(["📖 1. Мәтінді Оқу", "✍️ 2. Тест Тапсырмалары", "🧩 3. Сәйкестендіру Тапсырмалары"])

    with tab1:
        st.subheader("Reading Text")
        st.markdown(f"""
        <div class="text-card">
            {current_text['text'].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.subheader("NIS Форматындағы Тест Сұрақтары (5 сұрақ)")
        
        with st.form(key=f"quiz_form_{st.session_state.selected_text_id}"):
            user_answers = {}
            for i, q in enumerate(current_text["quiz"]):
                st.markdown(f"**{q['question']}**")
                user_answers[i] = st.radio(
                    label=f"Сұрақ {i+1} жауабы:", 
                    options=q["options"], 
                    key=f"q_{st.session_state.selected_text_id}_{i}",
                    label_visibility="collapsed"
                )
                st.write("")
            
            submit_button = st.form_submit_button(label="🚀 Жауаптарды тексеру")

        if submit_button:
            if not st.session_state.student_name:
                st.error("⚠️ Өтініш, алдымен жоғарғы панельге аты-жөніңізді енгізіңіз!")
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
                
                st.session_state.student_results.append({
                    "Оқушы аты-жөні": st.session_state.student_name,
                    "Сыныбы": st.session_state.student_class,
                    "Мәтін атауы": current_text["title"],
                    "Нәтиже": f"{score}/{total}",
                    "Жинаған XP": earned_xp,
                    "Тапсырған уақыты": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                st.balloons()
                st.success(f"🎉 Құттықтаймыз, {st.session_state.student_name}! Сіз {score}/{total} ұпай жинадыңыз (+{earned_xp} XP)!")

    with tab3:
        st.subheader("🧩 Vocabulary / Fact Matching (Сәйкестендіру)")
        if "matching" in current_text:
            matching_dict = current_text["matching"]
            left_items = list(matching_dict.keys())
            right_items = list(matching_dict.values())
            
            user_match_answers = {}
            for idx, left in enumerate(left_items):
                st.markdown(f"**{left}**")
                user_match_answers[left] = st.selectbox(
                    f"Таңдау {idx+1}:", 
                    options=["-- Таңдаңыз --"] + right_items,
                    key=f"match_{st.session_state.selected_text_id}_{idx}"
                )
            
            if st.button("🚀 Сәйкестікті тексеру"):
                correct_matches = 0
                for left, right in matching_dict.items():
                    if user_match_answers[left] == right:
                        correct_matches += 1
                
                if correct_matches == len(matching_dict):
                    st.balloons()
                    st.success(f"🌟 Керемет! Барлық {correct_matches}/{len(matching_dict)} сәйкестік дұрыс табылды!")
                else:
                    st.warning(f"🎯 Сіз {correct_matches}/{len(matching_dict)} сәйкестікті дұрыс таптыңыз. Қайтадан байқап көріңіз!")
        else:
            st.info("Бұл мәтін үшін сәйкестендіру тапсырмасы қарастырылмаған.")

elif st.session_state.current_view == "dashboard":
    st.title("📊 Оқушылардың нәтижелері (Teacher Dashboard)")
    st.markdown("Бұл бөлімде оқушылардың тест тапсыру нәтижелері автоматты түрде жинақталып көрсетіледі.")
    
    if st.button("⬅️ Кітап сөресіне қайту"):
        st.session_state.current_view = "bookcase"
        st.rerun()
        
    st.markdown("---")
    
    if len(st.session_state.student_results) == 0:
        st.info("📭 Әзірге ешқандай оқушы нәтижесі тіркелген жоқ.")
    else:
        df_results = pd.DataFrame(st.session_state.student_results)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Барлық тапсырулар саны", len(df_results))
        col2.metric("Қатысқан оқушылар", df_results["Оқушы аты-жөні"].nunique())
        col3.metric("Жалпы берілген XP", int(df_results["Жинаған XP"].sum()))
        
        st.markdown("### 📋 Нәтижелер кестесі")
        st.dataframe(df_results, use_container_width=True)
        
        st.markdown("---")
        if st.button("🗑️ Барлық нәтижелер базасын тазалау"):
            st.session_state.student_results = []
            st.success("✅ База сәтті тазартылды!")
            st.rerun()
