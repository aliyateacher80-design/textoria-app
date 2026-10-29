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

# --- CSS СТИЛЬДЕРІ (Сұрақтар мен мәтіндерді ақ түске бояу) ---
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

    /* Тест және сәйкестендіру сұрақтарын ақ түске өзгерту */
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

    .book-shelf-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #38bdf8;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        color: #ffffff;
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
    st.session_state.student_class = "6 «Ә»"

# --- 9 МӘТІН ЖӘНЕ ТОЛЫҚ ТАПСЫРМАЛАР БАЗАСЫ ---
TEXTS_DATABASE = {
    1: {
        "title": "Adeliya’s Daily Routine",
        "genre": "Personal Narrative",
        "icon": "⏰",
        "text": """
        Meet Adeliya. She's a grade 6 student at Panfilov Kazakhstani-Russian Gymnasium, 54 in Almaty. It's a big school with about 1,500 students.

        During term time, Adeliya usually follows the same routine. Her day starts early. She usually gets up at 7 o'clock. Then she has a shower. Then she gets dressed and goes downstairs for breakfast. After breakfast, she finds the things she needs for school. When she's ready, her grandma, Raissa, takes her to school on foot.

        Adeliya usually has six lessons a day. Her favourite lesson is Kazakh, but she doesn't like P.E. At 11 a.m. there is a break, and Adeliya has brunch with her classmates. They usually have buns with tea or apple juice.

        When school finishes at 2 p.m., her grandma meets her and they go back home. They have lunch together and talk about their days. They usually have meatballs with mashed potatoes or chicken soup, because they are Adeliya's favourite foods. Adeliya is a very hard-working student, so in the afternoon she always does her homework and gets ready for the next day.

        Three days a week, Adeliya goes to a music school. She's in the choir and they practise singing and learn new songs. In the evening, she usually goes for a walk with her friends and her brother Dias. Adeliya is busy, but if she has time she helps her mother around the house. At 10 p.m. Adeliya goes to bed.
        """,
        "quiz": [
            {"question": "1. Why does Adeliya have lunch with her grandma after school?", "options": ["A) Because her parents are at school.", "B) Because her grandma meets her after school.", "C) Because she doesn't like eating at school.", "D) Because her friends invite her."], "answer": "B) Because her grandma meets her after school.", "explanation": "Her grandma meets her after school."},
            {"question": "2. Which activity does Adeliya do three days a week?", "options": ["A) She plays basketball.", "B) She learns Kazakh.", "C) She attends music school.", "D) She goes shopping."], "answer": "C) She attends music school.", "explanation": "She attends music school three days a week."},
            {"question": "3. What can we understand about Adeliya from the text?", "options": ["A) She doesn't enjoy studying.", "B) She is hardworking and has a busy routine.", "C) She never helps her family.", "D) She always gets up late."], "answer": "B) She is hardworking and has a busy routine.", "explanation": "She is hardworking and has a busy routine."},
            {"question": "4. What does Adeliya usually do after lunch?", "options": ["A) She watches television all afternoon.", "B) She goes to the park alone.", "C) She does her homework and prepares for the next day.", "D) She goes straight to music school every day."], "answer": "C) She does her homework and prepares for the next day.", "explanation": "She does her homework and prepares for the next day."},
            {"question": "5. Which statement best describes Adeliya's daily life?", "options": ["A) She spends most of her day playing computer games.", "B) She balances school, homework, music and family time.", "C) She only studies and never meets her friends.", "D) She dislikes spending time with her family."], "answer": "B) She balances school, homework, music and family time.", "explanation": "She balances school, homework, music and family time."}
        ],
        "matching": {"7 o'clock": "Adeliya gets up", "11 a.m.": "Brunch with classmates (buns with tea/juice)", "2 p.m.": "School finishes and grandma meets her", "3 days a week": "Attends music school (choir practice)", "10 p.m.": "Adeliya goes to bed"}
    },
    2: {
        "title": "Beth’s School Life and Interests",
        "genre": "Informal Letter / Blog",
        "icon": "🎾",
        "text": """
        Hi,
        My name’s Beth. I’m 13 years old and I’m a student at Liberty High School in Brighton.

        I like school. There are about 30 people in my class. We work hard, but we have fun too. We do a lot of our lessons together, but not sport. Girls and boys have different games lessons. I like sport, I’m really into basketball and tennis. My favourite tennis player is Rafael Nadal. I’m not in the school tennis team, but I play it in games lessons in the summer. Lots of people in my class play football, but I hate it.

        My favourite lesson is music. I think everyone enjoys it. We have such a great teacher. He’s really into pop music. I am too, but I haven’t got a favourite group.

        What about you and your class? What's your favourite team? Please write and send a photo if you’ve got one.
        Bye for now,
        Beth
        """,
        "quiz": [
            {"question": "1. What is the best title of this text?", "options": ["A) A Day at the Sports Centre", "B) Beth’s School Life and Interests", "C) Rafael Nadal’s Career", "D) The Best Music Groups"], "answer": "B) Beth’s School Life and Interests", "explanation": "Мәтінде Beth өзінің мектебі, спортқа қызығушылығы және музыка сабағы туралы әңгімелейді."},
            {"question": "2. What is the main idea of this text?", "options": ["A) Beth describes her school, favourite subjects and sports interests.", "B) Beth explains how to become a tennis player.", "C) Beth talks only about her music teacher.", "D) Beth describes her school holidays."], "answer": "A) Beth describes her school, favourite subjects and sports interests.", "explanation": "Мәтіннің негізгі ойы — Beth-тің мектептегі өмірі, сүйікті пәндері және спорттық қызығушылықтары."},
            {"question": "3. Which part of the text tells us how Beth plays tennis?", "options": ["A) The first paragraph, where she talks about sports lessons and summer.", "B) The part where she introduces herself.", "C) The part where she describes her music teacher.", "D) The final greeting."], "answer": "A) The first paragraph, where she talks about sports lessons and summer.", "explanation": "Бірінші абзацта Beth жаз мезгілінде дене шынықтыру сабақтарында теннис ойнайтынын айтады."},
            {"question": "4. Which word is missing? Beth is really into basketball and tennis, but she ______ football.", "options": ["A) loves", "B) enjoys", "C) hates", "D) plays"], "answer": "C) hates", "explanation": "Beth футболды ұнатпайтынын тікелей айтады: 'I hate it'."},
            {"question": "5. What does the sentence “I’m really into basketball and tennis” mean?", "options": ["A) Beth watches basketball and tennis on TV every day.", "B) Beth is very interested in basketball and tennis.", "C) Beth doesn't understand basketball and tennis.", "D) Beth teaches basketball and tennis."], "answer": "B) Beth is very interested in basketball and tennis.", "explanation": "'Be really into something' — бір нәрсеге қатты қызығу, ұнату дегенді білдіреді."}
        ],
        "matching": {"Liberty High School": "Beth's school in Brighton", "Rafael Nadal": "Beth's favourite tennis player", "Football": "The sport Beth hates", "Music": "Beth's favourite lesson", "Be really into": "To be very interested in something"}
    },
    3: {
        "title": "Almaty — Home to Many Nationalities",
        "genre": "Informative Article",
        "icon": "🏙️",
        "text": """
        Almaty is the biggest city in Kazakhstan and 58% of the population lives there. Almaty has almost 2 million people. Around 50% of them are Kazakh, but the other 50% have parents, grandparents and more distant ancestors from lots of different nations. For example, around a third of people have families from Russia, but there are also a lot from China, Korea, Ukraine and other places. Artur and Sofiia are two of those people.
        """,
        "quiz": [
            {"question": "1. How many people live in Almaty?", "options": ["A) Almost 1 million", "B) Almost 2 million", "C) Almost 3 million", "D) Almost 5 million"], "answer": "B) Almost 2 million", "explanation": "Мәтінде Алматыда шамамен 2 миллион адам тұратыны жазылған."},
            {"question": "2. Approximately what percentage of Almaty’s population is Kazakh?", "options": ["A) 25%", "B) 30%", "C) 50%", "D) 75%"], "answer": "C) 50%", "explanation": "Мәтінде қала тұрғындарының шамамен 50%-ы қазақтар екені айтылған."},
            {"question": "3. Where do around a third of the people in Almaty have family roots?", "options": ["A) Russia", "B) China", "C) Korea", "D) Ukraine"], "answer": "A) Russia", "explanation": "Мәтін бойынша тұрғындардың шамамен үштен бірінің отбасы Ресейден шыққан."},
            {"question": "4. Almaty is the ______ city in Kazakhstan.", "options": ["A) oldest", "B) smallest", "C) biggest", "D) newest"], "answer": "C) biggest", "explanation": "Biggest — 'ең үлкен' деген мағына береді."},
            {"question": "5. Which countries are mentioned in the text as places where residents’ families come from?", "options": ["A) Russia, China, Korea and Ukraine", "B) France, Italy, Spain and Germany", "C) Japan, India, Egypt and Turkey", "D) Canada, Australia, Brazil and Mexico"], "answer": "A) Russia, China, Korea and Ukraine", "explanation": "Мәтінде Ресей, Қытай, Корея және Украина аталған."}
        ],
        "matching": {"Biggest city": "Almaty", "Almost 2 million": "Population of Almaty", "50%": "Percentage of Kazakh population in Almaty", "Around a third": "People with family roots from Russia", "China, Korea, Ukraine": "Other countries mentioned in the text"}
    },
    4: {
        "title": "My Day (Darby in India)",
        "genre": "Autobiography / Blog",
        "icon": "🤝",
        "text": """
        My name’s Darby. I’m a volunteer at a school in India. I usually teach English, but sometimes I teach geography as well.

        At school, we always start the day early with exercise. It helps everyone relax and focus. The school is old and it doesn’t have new equipment, but the children want to learn. They come from poor families and they know education is important in life. The mothers of the children often come to school and sit in the class. They want to learn too.

        I only work till midday. Then I usually have lunch with friends. In the afternoon I prepare the lessons for the next day and meet my new friends in the village after they finish work.
        """,
        "quiz": [
            {"question": "1. What is Darby’s job at the school?", "options": ["A) She is a doctor.", "B) She is a volunteer.", "C) She is a student.", "D) She is a school director."], "answer": "B) She is a volunteer.", "explanation": "Darby өзін Үндістандағы мектепте ерікті болып жұмыс істейтін адам ретінде таныстырады."},
            {"question": "2. Which subjects does Darby sometimes teach?", "options": ["A) English and geography", "B) Maths and science", "C) History and English", "D) Geography and art"], "answer": "A) English and geography", "explanation": "Darby әдетте ағылшын тілінен сабақ береді, кейде географияны да оқытады."},
            {"question": "3. Why do the students start the day with exercise?", "options": ["A) To prepare for a sports competition.", "B) To help them relax and focus.", "C) To make them tired.", "D) To learn geography."], "answer": "B) To help them relax and focus.", "explanation": "Таңертеңгі жаттығу балаларға тынығуға және зейін қоюға көмектеседі."},
            {"question": "4. The school is old and it doesn’t have ______.", "options": ["A) any students", "B) any teachers", "C) new equipment", "D) any classrooms"], "answer": "C) new equipment", "explanation": "Мәтінде мектептің ескі екені және жаңа жабдықтары жоқ екені жазылған."},
            {"question": "5. Why do the children want to learn?", "options": ["A) They think education is important in life.", "B) They want to leave the village.", "C) They want to become teachers immediately.", "D) Their school has new equipment."], "answer": "A) They think education is important in life.", "explanation": "Балалар білімнің болашақ үшін маңызды екенін түсінеді."}
        ],
        "matching": {"Darby": "Volunteer teacher in India", "Morning exercise": "Helps students relax and focus", "Mothers of children": "Come to school to learn too", "Till midday": "Darby's working hours", "Afternoon": "Lesson preparation and meeting village friends"}
    },
    5: {
        "title": "Danger! Humans!",
        "genre": "Environmental Science",
        "icon": "🐅",
        "text": """
        When an animal attacks a person, there are always stories about it on TV and in the newspapers. But people are usually more dangerous than animals. Every year, we kill approximately 100 million sharks, but sharks only attack three or four people, and crocodiles six or seven. More people die in accidents with chairs!

        Animals aren’t really a problem for people, but we are a problem for animals. We eat millions of tonnes of fish and meat every year. But people don’t kill animals just for food. They also hunt them for fur or for fun. While you’re reading this, people are hunting animals all over the world.

        At the moment, animals are becoming extinct in every part of the world. The ‘red list’ of animals in danger in Kazakhstan includes species of horses, leopards, wild dogs, lynx, otter, bats and bears. We aren’t killing all these animals directly, but they are dying and becoming extinct because of human behaviour. Our pollution and construction is changing the climate and animals’ habitats, and time is running out for some animals. It’s important to change our actions now and save the animals.
        """,
        "quiz": [
            {"question": "1. What is the main idea of the text?", "options": ["A) Animals are more dangerous than humans.", "B) Humans harm animals, and we need to protect them.", "C) Animals should live only in zoos.", "D) People should stop eating fish."], "answer": "B) Humans harm animals, and we need to protect them.", "explanation": "Мәтіннің негізгі ойы: адамдар жануарларға зиян келтіреді, сондықтан оларды қорғау қажет."},
            {"question": "2. Which paragraph explains why some animal species are disappearing?", "options": ["A) The paragraph about animal attacks in the news.", "B) The paragraph about the number of sharks killed.", "C) The paragraph about pollution, construction and changes to habitats.", "D) The paragraph about people eating meat."], "answer": "C) The paragraph about pollution, construction and changes to habitats.", "explanation": "Қоршаған ортаның ластануы мен құрылыс жануарлардың тіршілік ортасын өзгерткені 3-абзацта айтылады."},
            {"question": "3. Which word best completes the sentence? People sometimes kill animals for food, fur or ______.", "options": ["A) fun", "B) education", "C) transport", "D) medicine"], "answer": "A) fun", "explanation": "Мәтінде адамдар жануарларды тамақ, терісі және көңіл көтеру (fun) үшін аулайтыны айтылған."},
            {"question": "4. What does the phrase “time is running out for some animals” mean?", "options": ["A) Animals are moving to different places.", "B) Some animals may disappear soon.", "C) Animals need more time to hunt.", "D) Animals are becoming faster."], "answer": "B) Some animals may disappear soon.", "explanation": "Бұл тіркес кейбір жануар түрлерінің жақын арада жойылып кетуі (extinct) мүмкін екенін білдіреді."},
            {"question": "5. What does the word “our” refer to in the phrase “our pollution and construction”?", "options": ["A) Animals", "B) Humans", "C) Scientists", "D) Newspapers"], "answer": "B) Humans", "explanation": "'Our' сөзі адамдардың (humans) әрекеттерін білдіреді."}
        ],
        "matching": {"100 million": "Sharks killed by humans every year", "Kazakhstan Red List": "Includes leopards, lynx, bears and otters", "Habitat destruction": "Caused by human pollution and construction", "Extinct": "Animals disappearing completely from Earth", "Time is running out": "Some animals may disappear very soon"}
    },
    6: {
        "title": "Altyn-Emel National Park",
        "genre": "Geography & Nature",
        "icon": "⛰️",
        "text": """
        The Altyn-Emel National Park is very big: it covers 4,600 km2 in south-east Kazakhstan. It lies between the River Ili and the Aktau Mountains. This is a very dry part of the country where life is hard. But in this difficult environment there are around 1,800 species of plants, including willows and honeysuckles; 32 types of fish, and around 260 species of vertebrates (animals with backbones), with 11 on Kazakhstan’s red list of endangered species. The rich wildlife makes the park a paradise for birdwatchers: along with other rare birds, you can see four types of eagle including imperial and golden eagles, as well as eagle owls.

        Other attractions of the park are the singing sand dunes and the Aktau Mountains. They are both amazingly beautiful and interesting landscapes. The dunes are over 3 km long and 500 m high. As the wind moves the sand it makes a sound like an organ. The sound is really loud in dry weather and can be heard several kilometres away.

        There are signs that people lived in this area many, many years ago. The paintings on some of the rocks of animals and everyday life are thousands of years old. There are archaeological sites from around 3,000 years ago.
        """,
        "quiz": [
            {"question": "1. What makes Altyn-Emel National Park special despite its dry environment?", "options": ["A) It has many shopping centres.", "B) It has a rich variety of plants, fish and animals.", "C) It receives heavy rainfall every day.", "D) It has no endangered species."], "answer": "B) It has a rich variety of plants, fish and animals.", "explanation": "Құрғақ аймақ болса да, саябақта өсімдіктердің, балықтардың және жануарлардың көптеген түрі бар."},
            {"question": "2. Which geographical features surround the park?", "options": ["A) The River Ili and the Aktau Mountains", "B) The Caspian Sea and the Altai Mountains", "C) The River Irtysh and the Tian Shan Mountains", "D) The Aral Sea and the Khangai Mountains"], "answer": "A) The River Ili and the Aktau Mountains", "explanation": "Саябақ Іле өзені мен Ақтау тауларының арасында орналасқан."},
            {"question": "3. How many species of plants are found in the park?", "options": ["A) Around 260", "B) 32", "C) Around 1,800", "D) 11"], "answer": "C) Around 1,800", "explanation": "Мәтінде шамамен 1 800 өсімдік түрі кездесетіні айтылған."},
            {"question": "4. Why is the park a paradise for birdwatchers?", "options": ["A) It has many rare birds, including four types of eagle.", "B) All birds in Kazakhstan live there.", "C) Visitors can feed the eagles.", "D) It is the only place with birds in Kazakhstan."], "answer": "A) It has many rare birds, including four types of eagle.", "explanation": "Саябақта сирек кездесетін құстар, соның ішінде бүркіттің төрт түрі бар."},
            {"question": "5. What causes the singing sand dunes to make a sound?", "options": ["A) Birds sing above the dunes.", "B) Water flows under the sand.", "C) The wind moves the sand.", "D) People walk across the dunes."], "answer": "C) The wind moves the sand.", "explanation": "Жел құмды қозғағанда, орган аспабына ұқсас дыбыс шығады."}
        ],
        "matching": {"4,600 km2": "Total area of Altyn-Emel National Park", "1,800 species": "Plant species found in the park", "Four types of eagle": "Imperial, golden eagles and other rare birds", "Singing dunes": "3 km long, 500 m high sand dunes", "Wind moving sand": "Makes a sound like an organ"}
    },
    7: {
        "title": "Asanaly Ashimov",
        "genre": "Biography & Culture",
        "icon": "🎭",
        "text": """
        Asanaly Ashimov is one of the best-known names in theatre and cinema in Kazakhstan, and he has received many awards for his work.
        He grew up in a village, but he loved to act and wanted to study drama, so he enrolled at the Kazakh State Conservatory in Almaty.
        He showed talent as a student and appeared in his first film in 1958, while he was still a student.
        After he graduated, he joined the M. Auezov theatre troupe in Almaty and started acting on stage. Some of the Kazakh roles he is famous for are Kodar in Kozy Korpesh, Kebek in Yenlik Kebek and Yelamen in Blood and Sweat.
        He has also played some famous roles in international plays. For example, he played Julius Caesar in Shakespeare’s play, the lead part in Don Juan, and Dr Clausen in Before Sunset by G. Hauptmann – a role he performed over 100 times.
        Some actors only work in one medium (cinema or theatre), but Ashimov worked in both. The early films that made him famous are Kyz-Zhibek, in 1970, and The End of Ataman, in 1972. This is a historic thriller and an extremely successful Kazakh film. The director was Ashimov’s father-in-law, but unfortunately he died soon after making it.
        Like many successful actors, Ashimov decided to try directing. His first film was The Year of the Dragon in 1984 and after that he spent more time directing films than appearing in them – but he also found time to work in the theatre.
        """,
        "quiz": [
            {"question": "1. When did Ashimov first appear in a film?", "options": ["A) After becoming a director", "B) After graduating from university", "C) While he was still a student", "D) After joining the theatre troupe"], "answer": "C) While he was still a student", "explanation": "Әшімов 1958 жылы студент кезінде алғашқы фильміне түскен."},
            {"question": "2. What does the word “troupe” mean in the fourth paragraph?", "options": ["A) A group of actors who perform together", "B) A school for young musicians", "C) A company that produces books", "D) A building where films are shown"], "answer": "A) A group of actors who perform together", "explanation": "Troupe — бірге өнер көрсететін актерлер тобы, яғни театр труппасы."},
            {"question": "3. What does the word “This” refer to in the sentence “This is a historic thriller and an extremely successful Kazakh film”?", "options": ["A) Kyz-Zhibek", "B) The End of Ataman", "C) The Year of the Dragon", "D) Kozy Korpesh"], "answer": "B) The End of Ataman", "explanation": "This сөзі 1972 жылы шыққан The End of Ataman фильміне қатысты."},
            {"question": "4. Which statement about Ashimov is correct according to the text?", "options": ["A) He worked only in cinema.", "B) He became a director before becoming an actor.", "C) He performed the role of Dr Clausen over 100 times.", "D) He studied drama in a village."], "answer": "C) He performed the role of Dr Clausen over 100 times.", "explanation": "Ол Before Sunset қойылымындағы доктор Клаузен рөлін 100-ден астам рет орындаған."},
            {"question": "5. Which of the following films was directed by Ashimov?", "options": ["A) Kyz-Zhibek", "B) The End of Ataman", "C) The Year of the Dragon", "D) Blood and Sweat"], "answer": "C) The Year of the Dragon", "explanation": "The Year of the Dragon — Әшімовтің 1984 жылы түсірген алғашқы режиссерлік фильмі."}
        ],
        "matching": {"1958": "First film appearance while a student", "M. Auezov troupe": "Joined after graduation to act on stage", "Dr Clausen": "Role in Before Sunset performed over 100 times", "The End of Ataman": "1972 historic thriller film", "The Year of the Dragon": "His first directed film in 1984"}
    },
    8: {
        "title": "The Internet",
        "genre": "Technology & History",
        "icon": "🌐",
        "text": """
        Where do you look for information, play games, watch videos, download e-books and buy music? What do you use to write emails or chat to friends on websites like Facebook or MySpace? More than 1.5 billion people do these things on the internet every day. Today, the internet is all over the world, but fifty years ago it did not exist.
        The internet started in 1969 in the USA. It was called ARPANET at first, but its name soon changed to ‘the internet’. Universities used it to communicate ideas and information. In those days, computers were enormous machines and not many people used them.
        This began to change in 1971 when Ray Tomlinson, an American engineer, sent the first email message. He chose the symbol @ on his keyboard to identify his email address.
        The internet didn’t become really popular until Tim Berners-Lee, an English scientist, invented the World Wide Web in 1989.
        His invention was very important because it became possible to do a lot more things on the internet like listening to music and watching videos. He created the first website and named it info.cern.ch. He used the symbol ‘ch’ for Switzerland because he worked in Geneva.
        After that, people created millions of websites on every topic. At first, it wasn’t easy to find information, so in the early 1990s many universities developed search engines. Lycos was one of the first of these and later, Yahoo! and Google became very popular.
        Today you don’t need a big computer to go on the internet. You can use a smartphone or a laptop with a Wi-Fi connection. Internet technology is changing all the time and it is changing our lives.
        """,
        "quiz": [
            {"question": "1. What is the main idea of the text?", "options": ["A) The history and development of the internet", "B) The invention of smartphones", "C) The life of famous scientists", "D) The history of computer games"], "answer": "A) The history and development of the internet", "explanation": "Мәтінде интернеттің пайда болуы, тарихы және уақыт өте дамуы туралы баяндалады."},
            {"question": "2. What was the internet originally used for?", "options": ["A) Watching videos and playing games", "B) Buying music and downloading books", "C) Sharing ideas and information between universities", "D) Sending messages on social media"], "answer": "C) Sharing ideas and information between universities", "explanation": "Алғашында интернетті университеттер идеялар мен ақпарат алмасу үшін пайдаланған."},
            {"question": "3. Which event happened first?", "options": ["A) Tim Berners-Lee invented the World Wide Web.", "B) Ray Tomlinson sent the first email.", "C) Google became popular.", "D) ARPANET started in the USA."], "answer": "D) ARPANET started in the USA.", "explanation": "ARPANET 1969 жылы пайда болған. Бұл қалған оқиғалардан бұрын болған."},
            {"question": "4. What does the word “enormous” mean in the second paragraph?", "options": ["A) Very expensive", "B) Very large", "C) Very modern", "D) Very fast"], "answer": "B) Very large", "explanation": "Enormous сөзі «өте үлкен» деген мағынаны білдіреді."},
            {"question": "5. What does the word “these” refer to in the sentence “Lycos was one of the first of these”?", "options": ["A) Universities", "B) Websites", "C) Search engines", "D) Computers"], "answer": "C) Search engines", "explanation": "These сөзі search engines (іздеу жүйелері) деген сөз тіркесіне қатысты."}
        ],
        "matching": {"1969": "ARPANET started in the USA", "Ray Tomlinson": "Sent the first email in 1971 using @", "Tim Berners-Lee": "Invented the World Wide Web in 1989", "info.cern.ch": "First website created in Switzerland", "Lycos": "One of the early search engines"}
    },
    9: {
        "title": "Almaty Marathon",
        "genre": "Sport & Community",
        "icon": "🏃‍♂️",
        "text": """
        Every April, the city of Almaty holds a marathon. It started as a small event in 2012, with around 2,500 runners, but in 2015 the number increased to 19,000. People come from many countries to take part. There are runners from Russia, Kyrgyzstan, the UK, the USA, Italy, Spain, Denmark and Norway, but most people come from Almaty and other parts of Kazakhstan.
        The organizers started the marathon to promote healthier lifestyles. Everyone knows exercise is good for you, but sometimes it is difficult to find the time to do sport. But people like challenges, and a marathon gives them something to aim for. It’s impossible to do nothing all year then run 42 km. You have to train and increase the distance you run over a number of months. Apart from the marathon, there are other shorter events in the year to keep people interested in running.
        Anyone living in Almaty can enter the marathon, so families and friends can enter together and this helps people feel part of the city. The event also raises money for disabled children to do sport and gives them a better life.
        Over 20,000 people enter and watch the marathon, so the organizers need lots of volunteers to give each runner food and drink and show them where to go. Anyone can volunteer; you don’t need to be from Almaty or good at running to do this, but you do need a lot of energy, and it is better to do something for your community than not do anything.
        """,
        "quiz": [
            {"question": "1. Why is it important to train for several months before a marathon?", "options": ["A) Because runners need to increase their running distance gradually", "B) Because all runners must become professional athletes", "C) Because the marathon takes several months to finish", "D) Because runners must travel to other countries"], "answer": "A) Because runners need to increase their running distance gradually", "explanation": "Марафонға дайындалу үшін бірнеше ай бойы жаттығып, жүгіретін қашықтықты біртіндеп арттыру қажет."},
            {"question": "2. Which statement is correct according to the text?", "options": ["A) Only professional athletes can enter the marathon.", "B) All volunteers must be good at running.", "C) The marathon raises money to help disabled children do sport.", "D) Most runners come from the USA and the UK."], "answer": "C) The marathon raises money to help disabled children do sport.", "explanation": "Марафон мүмкіндігі шектеулі балалардың спортпен айналысуына көмектесу үшін қаражат жинайды."},
            {"question": "3. What can we understand about volunteering at the Almaty Marathon?", "options": ["A) Volunteers must live in Almaty.", "B) Volunteers need to run 42 kilometres.", "C) Volunteering is a way to help the community.", "D) Only people with sports awards can volunteer."], "answer": "C) Volunteering is a way to help the community.", "explanation": "Ерікті болу арқылы адамдар қоғамға пайдалы іс жасайды. Ол үшін кәсіби жүгіруші болу міндетті емес."},
            {"question": "4. The Almaty Marathon takes place every April.", "options": ["A) True", "B) False", "C) Not given", "D) Cannot say"], "answer": "A) True", "explanation": "Мәтіннің басында Алматы марафоны жыл сайын сәуір айында өтетіні жазылған."},
            {"question": "5. The marathon organizers arrange shorter running events during the year to keep people interested.", "options": ["A) True", "B) False", "C) Not given", "D) Cannot say"], "answer": "A) True", "explanation": "Ұйымдастырушылар адамдардың жүгіруге қызығушылығын сақтау үшін жыл бойы қысқа қашықтықтағы жарыстар ұйымдастырады."}
        ],
        "matching": {"2012": "Almaty Marathon started as a small event", "42 km": "Distance of the main marathon", "Disabled children": "Raise money to help them do sport", "Volunteers": "Give runners food, drink and guidance", "Every April": "When the Almaty Marathon takes place"}
    }
}

# --- SIDEBAR (ОҚУШЫ ПАНЕЛІ ЖӘНЕ МҰҒАЛІМ ЖУРНАЛЫ) ---
with st.sidebar:
    st.markdown("## 🛡️ **ОҚУШЫ ПАНЕЛІ**")
    st.session_state.student_name = st.text_input("👤 Аты-жөніңіз:", value=st.session_state.student_name, placeholder="Мысалы: Айбек")
    st.session_state.student_class = st.text_input("🏫 Сыныбыңыз:", value=st.session_state.student_class, placeholder="Мысалы: 6 «Ә»")

    current_level = (st.session_state.xp // 100) + 1
    st.markdown(f"**Деңгей:** 🏆 `{current_level}-деңгей`")
    st.markdown(f"**Жинақталған XP:** ⚡ `{st.session_state.xp} XP`")
    
    st.markdown("---")
    if st.button("📚 Кітап Сөресіне оралу", use_container_width=True):
        st.session_state.current_view = "bookcase"
        st.rerun()

    st.markdown("---")
    st.markdown("### 👩‍🏫 **Мұғалім панелі**")
    if st.button("📊 Нәтижелер журналын ашу", use_container_width=True):
        st.session_state.current_view = "teacher_dashboard"
        st.rerun()

# --- НЕГІЗГІ ХЕДЕР ---
st.markdown("<h1 style='text-align: center; color: #818cf8; font-family: Comfortaa;'>✨ TEXTORIA ✨</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #cbd5e1;'>«Ойла. Талда. Жетістікке жет!» — Оқылым Сауаттылығы</h4>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================================
# VIEW 1: BOOKCASE (КІТАП СӨРЕСІ)
# =====================================================================
if st.session_state.current_view == "bookcase":
    st.subheader("📚 Кітап Сөресі (Мәтінді таңдаңыз)")
    st.info("💡 Тапсырманы бастамас бұрын сол жақ панельге **атыңыз бен сыныбыңызды** жазыңыз!")

    cols = st.columns(3)
    for idx, (t_id, data) in enumerate(TEXTS_DATABASE.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="book-shelf-card">
                <h2>{data['icon']} {data['title']}</h2>
                <p><b>Жанры:</b> {data['genre']}</p>
                <p><i>5 Сұрақ + Сәйкестендіру</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Мәтінді оқу", key=f"select_{t_id}", use_container_width=True):
                if not st.session_state.student_name.strip():
                    st.warning("⚠️ Өтінемін, сол жақ панельге аты-жөніңізді жазыңыз!")
                else:
                    st.session_state.selected_text_id = t_id
                    st.session_state.current_view = "workspace"
                    st.rerun()

# =====================================================================
# VIEW 2: WORKSPACE (МӘТІН, ТЕСТ ЖӘНЕ СӘЙКЕС ТАПСЫРМА)
# =====================================================================
elif st.session_state.current_view == "workspace":
    current_data = TEXTS_DATABASE[st.session_state.selected_text_id]
    
    st.markdown(f"### {current_data['icon']} {current_data['title']}")
    st.write(f"👤 Оқушы: **{st.session_state.student_name}** ({st.session_state.student_class})")
    
    tab1, tab2, tab3 = st.tabs(["📖 1. Мәтінді Оқу", "📝 2. Тест Тапсырмалары", "🔗 3. Сәйкестендіру"])

    # ------------------ TAB 1: МӘТІН ------------------
    with tab1:
        st.markdown('<div class="text-card">', unsafe_allow_html=True)
        st.markdown(current_data['text'])
        st.markdown('</div>', unsafe_allow_html=True)
        st.success("👉 Мәтінді оқып болсаңыз, жоғарыдағы **«2. Тест Тапсырмалары»** немесе **«3. Сәйкестендіру»** бөліміне өтіңіз!")

    # ------------------ TAB 2: ТЕСТ ------------------
    with tab2:
        st.subheader("📝 NIS Форматындағы Тест Сұрақтары")
        user_answers = {}
        with st.form(key=f"quiz_form_{st.session_state.selected_text_id}"):
            for q_idx, q in enumerate(current_data['quiz']):
                st.markdown(f"**{q['question']}**")
                user_answers[q_idx] = st.radio("Жауапты таңдаңыз:", q['options'], key=f"q_{st.session_state.selected_text_id}_{q_idx}", index=None)
                st.markdown("---")
            submit_quiz = st.form_submit_button("🎯 Жауаптарды Тексеру")

        if submit_quiz:
            score = 0
            total = len(current_data['quiz'])
            for q_idx, q in enumerate(current_data['quiz']):
                if user_answers[q_idx] == q['answer']:
                    score += 1

            gained_xp = score * 20
            st.session_state.xp += gained_xp
            
            result_record = {
                "Уақыты": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Аты-жөні": st.session_state.student_name,
                "Сыныбы": st.session_state.student_class,
                "Мәтін": current_data['title'],
                "Ұпай": f"{score}/{total}",
                "XP": f"+{gained_xp} XP"
            }
            st.session_state.student_results.append(result_record)

            st.balloons()
            st.success(f"📊 Сіздің нәтижеңіз: {score} / {total} ({int(score/total*100)}%) | Жинағаныңыз: +{gained_xp} XP")

    # ------------------ TAB 3: СӘЙКЕС ТАПСЫРМА ------------------
    with tab3:
        st.subheader("🔗 Ұғымдарды Сәйкестендіру")
        matching_data = current_data['matching']
        left_items = list(matching_data.keys())
        right_options = list(matching_data.values())
        
        user_matching = {}
        with st.form(key=f"matching_form_{st.session_state.selected_text_id}"):
            for item in left_items:
                st.markdown(f"📌 **{item}**")
                user_matching[item] = st.selectbox("Анықтамасын таңдаңыз:", ["-- Таңдаңыз --"] + right_options, key=f"match_{item}")
                st.write("")
            submit_match = st.form_submit_button("✅ Сәйкестікті Тексеру")

        if submit_match:
            correct_count = sum(1 for item, val in matching_data.items() if user_matching[item] == val)
            if correct_count == len(matching_data):
                st.balloons()
                st.success(f"🎉 Барлық сәйкестік дұрыс! (+50 XP)")
                st.session_state.xp += 50
            else:
                st.warning(f"🎯 Дұрыс табылмаған жұптар бар. Нәтиже: {correct_count} / {len(matching_data)}")

# =====================================================================
# VIEW 3: TEACHER DASHBOARD (МҰҒАЛІМНІҢ БАҚЫЛАУ ЖУРНАЛЫ)
# =====================================================================
elif st.session_state.current_view == "teacher_dashboard":
    st.subheader("📊 Мұғалім панелі: Оқушылардың нәтижелер журналы")
    st.info("Бұл жерде платформа арқылы тапсырма тапсырған барлық оқушылардың тізімі мен жинаған ұпайлары көрінеді.")

    if not st.session_state.student_results:
        st.warning("📭 Әзірге ешқандай оқушы нәтиже жіберген жоқ.")
    else:
        df = pd.DataFrame(st.session_state.student_results)
        st.dataframe(df, use_container_width=True)

        st.markdown("### ⚙️ Журналды басқару (Тазарту/Өшіру)")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Барлық нәтижелерді тазарту", use_container_width=True):
                st.session_state.student_results = []
                st.success("Журнал толығымен тазартылды!")
                st.rerun()
        with col2:
            row_to_delete = st.number_input("Өшіретін жолдың нөмірі (index):", min_value=0, max_value=max(0, len(st.session_state.student_results)-1), step=1)
            if st.button("❌ Таңдалған жолды кетіру", use_container_width=True):
                if st.session_state.student_results:
                    st.session_state.student_results.pop(row_to_delete)
                    st.success("Таңдалған жол сәтті өшірілді!")
                    st.rerun()

    if st.button("🔙 Басты бетке қайту"):
        st.session_state.current_view = "bookcase"
        st.rerun()
