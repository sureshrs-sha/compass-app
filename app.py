# app.py
# Main Streamlit app for Compass

import streamlit as st
from assessment import QUESTIONS, compute_mastery
from recommender import generate_roadmap
from database import init_db, get_connection

# Initialize database
init_db()

# Page config
st.set_page_config(
    page_title="Compass",
    layout="centered"
)

# Custom styling
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        h1, h2, h3 { color: #2c3e50; }
        .stButton>button {
            background-color: #2980b9;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Session state setup
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "mastery" not in st.session_state:
    st.session_state.mastery = {}
if "roadmap" not in st.session_state:
    st.session_state.roadmap = []

# HOME PAGE
if st.session_state.page == "home":
    st.title("Compass")
    st.subheader("Your personal digital literacy guide")
    st.write("Welcome! Compass helps you learn how to use technology at your own pace.")
    st.write("")
    name = st.text_input("First, what is your name?", placeholder="Enter your name here")
    if st.button("Get Started"):
        if name.strip() == "":
            st.warning("Please enter your name to continue.")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?)", (name.strip(),))
            conn.commit()
            st.session_state.user_id = cursor.lastrowid
            st.session_state.user_name = name.strip()
            conn.close()
            st.session_state.page = "assessment"
            st.rerun()

# ASSESSMENT PAGE
elif st.session_state.page == "assessment":
    st.title("Quick Assessment")
    st.write(f"Hi {st.session_state.user_name}! Let's find out where you are starting from.")
    st.write("Answer honestly — there are no wrong answers.")
    st.write("")

    answers = {}
    for q in QUESTIONS:
        st.markdown(f"**{q['question']}**")
        option_labels = [opt[0] for opt in q["options"]]
        choice = st.radio("", option_labels, key=q["skill_id"], horizontal=False)
        score = dict(q["options"])[choice]
        answers[q["skill_id"]] = score
        st.write("")

    if st.button("See My Learning Path"):
        mastery = compute_mastery(answers)
        st.session_state.mastery = mastery

        conn = get_connection()
        cursor = conn.cursor()
        for skill_id, score in mastery.items():
            cursor.execute(
                "INSERT INTO mastery (user_id, skill_id, score) VALUES (?, ?, ?)",
                (st.session_state.user_id, skill_id, score)
            )
        conn.commit()
        conn.close()

        st.session_state.roadmap = generate_roadmap(mastery)
        st.session_state.page = "roadmap"
        st.rerun()

# ROADMAP PAGE
elif st.session_state.page == "roadmap":
    st.title("Your Learning Path")
    st.write(f"Based on your answers, here is what we recommend for you, {st.session_state.user_name}:")
    st.write("")

    if not st.session_state.roadmap:
        st.success("You have already mastered all the skills. Well done!")
    else:
        for i, skill in enumerate(st.session_state.roadmap, 1):
            with st.expander(f"Step {i}: {skill['label']}"):
                st.write(skill["description"])
                st.progress(skill["current_score"])
                st.caption(f"Current confidence: {int(skill['current_score'] * 100)}%")

    st.write("")
    if st.button("Start Learning"):
        st.session_state.current_lesson_index = 0
        st.session_state.page = "lesson"
        st.rerun()

# LESSON PAGE
elif st.session_state.page == "lesson":
    roadmap = st.session_state.roadmap
    index = st.session_state.current_lesson_index

    if index >= len(roadmap):
        st.session_state.page = "progress"
        st.rerun()

    skill = roadmap[index]
    st.title(skill["label"])
    st.write(skill["description"])
    st.write("")
    st.info("Take your time with this. You can always come back and review.")
    st.write("")

    if st.button("Mark as Complete"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO progress (user_id, skill_id) VALUES (?, ?)",
            (st.session_state.user_id, skill["skill_id"])
        )
        conn.commit()
        conn.close()
        st.session_state.current_lesson_index += 1
        st.rerun()

# PROGRESS PAGE
elif st.session_state.page == "progress":
    st.title("Your Progress")
    st.write(f"Well done, {st.session_state.user_name}! Here is what you have completed:")
    st.write("")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT skill_id FROM progress WHERE user_id = ?",
        (st.session_state.user_id,)
    )
    completed = [row["skill_id"] for row in cursor.fetchall()]
    conn.close()

    for skill_id in completed:
        st.success(skill_id.replace("_", " ").title())

    st.write("")
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
        