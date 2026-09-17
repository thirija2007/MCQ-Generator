import streamlit as st
from huggingface_hub import InferenceClient
import os
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="QuizForge AI",
    page_icon="🧠",
    layout="centered"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b, #312e81);
    color: white;
}

.block-container {
    max-width: 950px;
    padding-top: 2rem;
}

/* ================= HEADER ================= */

.hero {
    text-align: center;
    padding: 25px 10px 25px 10px;
}

.hero-icon {
    font-size: 55px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: white !important;
    margin: 5px 0;
}

.hero-subtitle {
    font-size: 18px;
    color: #cbd5e1 !important;
}

/* ================= SECTION HEADINGS ================= */

h2, h3 {
    color: white !important;
}

/* ================= INPUT LABELS ================= */

label {
    color: white !important;
}

/* ================= TEXT AREA ================= */

.stTextArea textarea {
    background-color: #f8fafc !important;
    color: #111827 !important;
    border-radius: 12px !important;
}

/* ================= NUMBER INPUT ================= */

.stNumberInput input {
    background-color: #f8fafc !important;
    color: #111827 !important;
}

/* ================= SELECT BOX ================= */

.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
}

/* ================= GENERATE BUTTON ================= */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 17px;
    font-weight: 700;
    background-color: #6366f1 !important;
    color: white !important;
    border: none !important;
}

.stButton > button:hover {
    background-color: #4f46e5 !important;
    color: white !important;
}

/* ================= QUESTION CARD ================= */

.question-card {
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 18px;
    padding: 22px;
    margin: 20px 0 10px 0;
    backdrop-filter: blur(10px);
}

.question-number {
    font-size: 14px;
    color: #a5b4fc !important;
    font-weight: 700;
    text-transform: uppercase;
}

.question-text {
    font-size: 20px;
    font-weight: 650;
    color: white !important;
    margin-top: 8px;
}

/* ================= OPTIONS ================= */

.option-text {
    background: rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 11px 15px;
    margin: 7px 0;
    color: white !important;
}

.option-text b {
    color: #c7d2fe !important;
}

/* ================= REVEAL ANSWER ================= */

[data-testid="stExpander"] {
    background-color: white !important;
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    margin-top: 12px !important;
}

[data-testid="stExpander"] summary {
    color: #1e293b !important;
}

[data-testid="stExpander"] summary span {
    color: #1e293b !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] p {
    color: #1e293b !important;
}

[data-testid="stExpander"] div {
    color: #1e293b;
}

/* ================= DOWNLOAD BUTTON ================= */

.stDownloadButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-weight: 700;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #94a3b8;
    padding: 30px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-icon">🧠</div>

<div class="hero-title">
QuizForge AI
</div>

<div class="hero-subtitle">
Create smart quizzes instantly with Artificial Intelligence
</div>

</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# QUIZ SETTINGS
# =========================================================

st.markdown("## 📝 Create Your Quiz")

topic = st.text_area(
    "Enter your topic",
    placeholder="Example: Python Programming, DBMS, Artificial Intelligence...",
    height=100
)

col1, col2 = st.columns(2)

with col1:

    num_questions = st.number_input(
        "🔢 Number of Questions",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )

with col2:

    difficulty = st.selectbox(
        "🎚️ Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

generate = st.button(
    "🚀 Generate My Quiz",
    use_container_width=True
)

# =========================================================
# SESSION STATE
# =========================================================

if "quiz_text" not in st.session_state:
    st.session_state.quiz_text = None

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "difficulty" not in st.session_state:
    st.session_state.difficulty = ""

# =========================================================
# GENERATE QUIZ
# =========================================================

if generate:

    if not topic.strip():

        st.warning("⚠️ Please enter your topic first.")

    else:

        api_token = os.getenv("HF_TOKEN")

        if not api_token:

            st.error("❌ HF_TOKEN is missing.")

            st.info(
                "Set your Hugging Face token in the terminal "
                "before running the app."
            )

            st.stop()

        client = InferenceClient(
            provider="auto",
            api_key=api_token
        )

        prompt = f"""
You are an expert educational MCQ generator.

Generate exactly {num_questions} multiple-choice questions
about the topic:

{topic}

Difficulty level: {difficulty}

Requirements:

1. Generate exactly {num_questions} questions.
2. Each question must have exactly four options.
3. Label the options A, B, C, and D.
4. Only one option should be correct.
5. Questions must match the selected difficulty.
6. Avoid duplicate questions.
7. Provide the correct answer.
8. Keep questions clear and suitable for students.

Use EXACTLY this format:

Question 1: Your question

A) Option A
B) Option B
C) Option C
D) Option D

Correct Answer: A) Option A

Question 2: Your question

A) Option A
B) Option B
C) Option C
D) Option D

Correct Answer: B) Option B

Continue until exactly {num_questions} questions are generated.
"""

        with st.spinner(
            "🤖 QuizForge AI is creating your quiz..."
        ):

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=4000
                )

                result = response.choices[0].message.content

                st.session_state.quiz_text = result
                st.session_state.topic = topic
                st.session_state.difficulty = difficulty

                st.success(
                    "🎉 MCQs generated successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ Error while generating MCQs."
                )

                st.code(str(e))

# =========================================================
# DISPLAY GENERATED MCQs
# =========================================================

if st.session_state.quiz_text:

    st.divider()

    st.markdown("## 📚 Your AI Generated Quiz")

    st.caption(
        f"Topic: {st.session_state.topic}  •  "
        f"Difficulty: {st.session_state.difficulty}"
    )

    result = st.session_state.quiz_text

    # Split questions
    questions = re.split(
        r'(?=Question\s*\d+\s*:)',
        result,
        flags=re.IGNORECASE
    )

    question_count = 0

    for block in questions:

        block = block.strip()

        if not block:
            continue

        # Question text
        question_match = re.search(
            r'Question\s*\d+\s*:\s*(.*?)(?=\n\s*A\))',
            block,
            re.IGNORECASE | re.DOTALL
        )

        # Options
        option_matches = re.findall(
            r'^\s*([A-D])\)\s*(.+)$',
            block,
            re.IGNORECASE | re.MULTILINE
        )

        # Correct answer
        answer_match = re.search(
            r'Correct Answer\s*:\s*([A-D])\)\s*(.+)',
            block,
            re.IGNORECASE
        )

        # =================================================
        # DISPLAY VALID QUESTION
        # =================================================

        if question_match and len(option_matches) >= 4:

            question_count += 1

            question_text = question_match.group(1).strip()

            st.markdown(
                f"""
                <div class="question-card">

                <div class="question-number">
                QUESTION {question_count}
                </div>

                <div class="question-text">
                {question_text}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # OPTIONS
            # =================================================

            for letter, option in option_matches[:4]:

                st.markdown(
                    f"""
                    <div class="option-text">
                    <b>{letter.upper()})</b> {option}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # =================================================
            # REVEAL ANSWER
            # =================================================

            if answer_match:

                answer_letter = (
                    answer_match.group(1).upper()
                )

                answer_text = (
                    answer_match.group(2).strip()
                )

                with st.expander(
                    "👁️ Reveal Correct Answer"
                ):

                    st.markdown(
                        f"""
                        <div style="
                            background-color: #dcfce7;
                            color: #166534;
                            padding: 14px;
                            border-radius: 10px;
                            font-weight: 700;
                            margin-top: 5px;
                        ">
                        ✅ Correct Answer:
                        {answer_letter}) {answer_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.write("")

    # =========================================================
    # FALLBACK
    # =========================================================

    if question_count == 0:

        st.warning(
            "The questions could not be formatted automatically. "
            "Showing the original AI response."
        )

        st.markdown("### 🤖 AI Response")

        st.markdown(result)

    # =========================================================
    # DOWNLOAD
    # =========================================================

    st.divider()

    st.markdown("## 📥 Save Your Quiz")

    st.download_button(
        label="📥 Download MCQs",
        data=result,
        file_name="QuizForge_AI_MCQs.txt",
        mime="text/plain",
        use_container_width=True
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer">

🧠 QuizForge AI

<br>

Powered by Python • Streamlit • Hugging Face • Large Language Model

</div>
""", unsafe_allow_html=True)
