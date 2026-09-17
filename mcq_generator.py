from huggingface_hub import InferenceClient
import os

API_TOKEN = os.getenv("HF_TOKEN")

if not API_TOKEN:
    print("Error: HF_TOKEN environment variable is not set.")
    exit()

client = InferenceClient(
    provider="auto",
    api_key=API_TOKEN
)

topic = input("Enter the topic: ")

num_questions = int(
    input("Enter number of questions: ")
)

prompt = f"""
You are an expert educational question generator.

Generate exactly {num_questions} multiple-choice questions
about the topic:

{topic}

Requirements:

1. Generate exactly {num_questions} questions.
2. Each question must have exactly 4 options.
3. Label the options A, B, C, and D.
4. Only one option should be correct.
5. Provide the correct answer.
6. Questions should be clear and suitable for students.
7. Avoid duplicate questions.

Use this format:

Question 1: [Question]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Correct Answer: A) [Answer]

Repeat this format for all questions.
"""

try:

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=3000
    )

    result = response.choices[0].message.content

    print("\n" + "=" * 60)
    print("GENERATED MCQs")
    print("=" * 60)

    print(result)

    print("=" * 60)

except Exception as e:

    print("\nError while generating MCQs:")
    print(e)