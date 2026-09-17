import streamlit as st
from huggingface_hub import InferenceClient
import os
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="QuizCraft AI",
    page_icon="🧠",
    layout="wide"
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
    max-width: 1100px;
    padding-top: 2rem;
}

/* Main Header */

.hero {
    text-align: center;
    padding: 35px 20px 25px 20px;
}

.hero-icon {
    font-size: 55px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    margin: 5px 0;
}

.hero-subtitle {
    font-size: 18px;
    color: #cbd5e1;
}

/* Cards */

.card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 18px;
    padding: 25px;
    margin: 18px 0;
    backdrop-filter: blur(12px);
}

.question-number {
    font-size: 14px;
    color: #a5b4fc;
    font-weight: 700;
    text-transform: uppercase;
}

.question-text {
    font-size: 20px;
    font-weight: 650;
    margin-top: 8px;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: 700;
}

/* Download */

.stDownloadButton > button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-weight: 700;
}

/* Footer */

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
QuizCraft AI
</div>

<div class="hero-subtitle">
Create smart, customized multiple-choice quizzes with Artificial Intelligence
</div>

</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Quiz Settings")

    num_questions = st.slider(
        "🔢 Number of Questions",
        min_value=1,
        max_value=20,
        value=5
    )

    difficulty = st.selectbox(
        "🎚️ Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    st.divider()

    st.markdown("### ✨ QuizCraft AI")

    st.write(
        "Generate personalized MCQs using an LLM."
    )

# =========================================================
# TOPIC INPUT
# =========================================================

st.markdown("## 📝 Create Your Quiz")

topic = st.text_input(
    "Enter your topic",
    placeholder="Example: Python Programming, DBMS, Artificial Intelligence..."
)

generate = st.button(
    "🚀 Generate My Quiz"
)

# =========================================================
# SESSION STATE
# =========================================================

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "raw_result" not in st.session_state:
    st.session_state.raw_result = ""

# =========================================================
# GENERATE QUIZ
# =========================================================

if generate:

    if not topic.strip():

        st.warning("⚠️ Please enter a topic first.")

    else:

        api_token = os.getenv("HF_TOKEN")

        if not api_token:

            st.error("❌ HF_TOKEN is missing.")

            st.info(
                "Set your Hugging Face token in the terminal before running the app."
            )

            st.stop()

        client = InferenceClient(
            provider="auto",
            api_key=api_token
        )

        prompt = f"""
You are an expert educational MCQ generator.

Create exactly {num_questions} multiple-choice questions
about:

{topic}

Difficulty level: {difficulty}

Requirements:

1. Generate exactly {num_questions} questions.
2. Each question must have exactly four options.
3. Label options A, B, C, D.
4. Only one answer must be correct.
5. Questions must match the selected difficulty.
6. Avoid duplicate questions.
7. Provide the correct answer.
8. Keep questions clear and educational.

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

Continue until all {num_questions} questions are generated.
"""

        with st.spinner("🤖 QuizCraft AI is creating your quiz..."):

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

                st.session_state.raw_result = result

                # -------------------------------------------------
                # Parse Questions
                # -------------------------------------------------

                pattern = r"Question\s+\d+:(.*?)(?=Question\s+\d+:|$)"

                matches = re.findall(
                    pattern,
                    result,
                    re.DOTALL | re.IGNORECASE
                )

                quiz_data = []

                for match in matches:

                    question_match = re.search(
                        r"^(.*?)\n\s*A\)",
                        match.strip(),
                        re.DOTALL
                    )

                    options = re.findall(
                        r"([A-D])\)\s*(.*)",
                        match
                    )

                    answer_match = re.search(
                        r"Correct Answer:\s*([A-D])\)\s*(.*)",
                        match,
                        re.IGNORECASE
                    )

                    if question_match and len(options) >= 4:

                        question = question_match.group(1).strip()

                        answer = None

                        if answer_match:
                            answer = answer_match.group(1).upper()

                        quiz_data.append(
                            {
                                "question": question,
                                "options": options[:4],
                                "answer": answer
                            }
                        )

                st.session_state.quiz = quiz_data

                st.success(
                    f"🎉 Successfully generated {len(quiz_data)} questions!"
                )

            except Exception as e:

                st.error("❌ Error while generating the quiz.")

                st.code(str(e))

# =========================================================
# DISPLAY QUIZ
# =========================================================

if st.session_state.quiz:

    st.divider()

    st.markdown("## 📚 Your AI Generated Quiz")

    st.caption(
        f"Topic: {topic}  •  Difficulty: {difficulty}  •  "
        f"Questions: {len(st.session_state.quiz)}"
    )

    # ---------------------------------------------------------
    # Individual MCQ Cards
    # ---------------------------------------------------------

    for index, q in enumerate(
        st.session_state.quiz,
        start=1
    ):

        st.markdown(
            f"""
            <div class="card">

            <div class="question-number">
            QUESTION {index}
            </div>

            <div class="question-text">
            {q["question"]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # Options

        for letter, option in q["options"]:

            st.write(
                f"**{letter})** {option}"
            )

        # -----------------------------------------------------
        # Hide / Reveal Answer
        # -----------------------------------------------------

        with st.expander("👁️ Reveal Correct Answer"):

            if q["answer"]:

                answer_text = ""

                for letter, option in q["options"]:

                    if letter.upper() == q["answer"]:

                        answer_text = option

                st.success(
                    f"✅ Correct Answer: {q['answer']}) {answer_text}"
                )

            else:

                st.info(
                    "Correct answer was not detected."
                )

        st.write("")

    # =========================================================
    # DOWNLOAD
    # =========================================================

    st.divider()

    st.markdown("## 📥 Save Your Quiz")

    download_text = (
        "QUIZCRAFT AI - GENERATED MCQs\n"
        + "=" * 50
        + "\n\n"
        + f"Topic: {topic}\n"
        + f"Difficulty: {difficulty}\n"
        + f"Number of Questions: {len(st.session_state.quiz)}\n\n"
    )

    for index, q in enumerate(
        st.session_state.quiz,
        start=1
    ):

        download_text += (
            f"Question {index}: {q['question']}\n\n"
        )

        for letter, option in q["options"]:

            download_text += (
                f"{letter}) {option}\n"
            )

        download_text += "\n"

        if q["answer"]:

            for letter, option in q["options"]:

                if letter.upper() == q["answer"]:

                    download_text += (
                        f"Correct Answer: "
                        f"{q['answer']}) {option}\n"
                    )

        download_text += "\n" + "-" * 50 + "\n\n"

    st.download_button(
        label="📥 Download MCQs",
        data=download_text,
        file_name="QuizCraft_AI_MCQs.txt",
        mime="text/plain"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

🧠 QuizCraft AI  
<br>
Powered by Python • Streamlit • Hugging Face • Large Language Model

</div>
""", unsafe_allow_html=True)