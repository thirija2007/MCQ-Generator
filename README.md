# MCQ Generator

## 📌 Project Overview

**MCQ Generator** is a Python-based LLM application that automatically generates multiple-choice questions (MCQs) on any given topic.

The application uses the **Hugging Face Inference API** with the **OpenAI GPT-OSS-120B** model to generate questions, four options, and the correct answer.

The application runs directly in the **VS Code terminal**.

---

# 🧠 QuizForge AI – MCQ Generator

An AI-powered Multiple Choice Question Generator using Python, Streamlit, Hugging Face, and LLM.

## 🚀 Live Demo

👉 https://mcq-generator-yeezwrpso3m8fhpwzx4pzm.streamlit.app/


## 🎯 Objective

The main objective of this project is to generate educational MCQs quickly using a Large Language Model (LLM).

The user provides:

* A topic
* The number of questions required

The application then generates MCQs with:

* Questions
* Four options (A, B, C, D)
* Correct answers

---

## ✨ Features

* Generate MCQs on any topic
* User-defined number of questions
* Exactly four options for each question
* Provides the correct answer
* Avoids duplicate questions
* Simple terminal-based interface
* Uses an LLM through Hugging Face
* Easy to run and use

---

## 🛠️ Technologies Used

* **Python**
* **Hugging Face Inference API**
* **Hugging Face Hub**
* **OpenAI GPT-OSS-120B**
* **VS Code**
* **Large Language Model (LLM)**

---

## 🔄 Workflow

```text
User
  ↓
Enter Topic
  ↓
Enter Number of Questions
  ↓
Python Application
  ↓
Hugging Face Inference API
  ↓
GPT-OSS-120B Model
  ↓
Generate MCQs
  ↓
Display Questions & Answers
```

---

## 📂 Project Structure

```text
MCQ Generator/
│
├── MCQ Generator.py
└── requirements.txt
```

### Files Description

| File               | Description                          |
| ------------------ | ------------------------------------ |
| `MCQ Generator.py` | Main Python application              |
| `requirements.txt` | Contains the required Python package |

---

## ⚙️ Installation

### Step 1: Clone or Download the Project

Open the project folder in **VS Code**.

### Step 2: Install Required Package

Open the VS Code terminal and run:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
huggingface_hub
```

---

## 🔑 Hugging Face API Token

This project requires a **Hugging Face Access Token** to access the inference service.

Set the token as an environment variable.

### Windows PowerShell

```powershell
$env:HF_TOKEN="YOUR_HUGGINGFACE_TOKEN"
```

Verify that the environment variable is set:

```powershell
echo $env:HF_TOKEN
```

> **Security Note:** Never upload your Hugging Face token to GitHub or include it directly inside the Python source code.

---

## ▶️ How to Run

Open the terminal inside the project folder and run:

```bash
python "MCQ Generator.py"
```

The application will ask:

```text
Enter the topic:
```

Enter a topic, for example:

```text
Python Programming
```

Then enter the number of questions:

```text
Enter number of questions: 5
```

The application will generate the requested MCQs.

---

## 📝 Sample Input

```text
Enter the topic: Python Programming
Enter number of questions: 5
```

---

## 📄 Sample Output

```text
============================================================
GENERATED MCQs
============================================================

Question 1: Which keyword is used to define a function in Python?

A) function
B) def
C) define
D) fun

Correct Answer: B) def

Question 2: Which data type is used to store multiple values in a sequence?

A) List
B) Integer
C) Boolean
D) Float

Correct Answer: A) List

...

============================================================
```

---

## 🧠 LLM Prompt

The application sends instructions to the LLM to generate:

1. The required number of questions
2. Four options for each question
3. Only one correct answer
4. Clear questions suitable for students
5. Non-duplicate questions
6. A consistent MCQ format

---

## 📥 Input

The application accepts:

```text
Topic
Number of Questions
```

Example:

```text
Topic: Artificial Intelligence
Number of Questions: 5
```

---

## 📤 Output

The application produces:

```text
Question
Option A
Option B
Option C
Option D
Correct Answer
```

for each generated MCQ.

---

## 🚀 Applications

This MCQ Generator can be useful for:

* Student practice
* Quiz preparation
* Educational activities
* Classroom assessments
* Self-learning
* Quick question generation
* Study material preparation

---

## 🔮 Future Enhancements

The project can be extended with:

* Difficulty level selection
* Subject/category selection
* Quiz mode
* Score calculation
* Timer
* Save MCQs as PDF
* Export questions to a file
* Web-based interface using Streamlit
* Database storage for generated questions

---

## 📌 Conclusion

The **MCQ Generator** demonstrates how a Large Language Model can be integrated with a Python application to automatically generate educational multiple-choice questions.

The project provides a simple and practical example of using **LLM technology, Hugging Face Inference API, and Python** to create an AI-powered educational application.
