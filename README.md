# 🔍 ReqLens

### AI/ML-Based Software Requirement Ambiguity Detection & Analysis System

> ReqLens analyzes software requirements to detect **vague wording, missing constraints, and potential conflicts**, then provides explanations, suggestions, and improved requirements.

---

🚀 Live Demo

Try ReqLens online:

👉 [**ReqLens Live Demo**](https://reqlens-project-demo.streamlit.app/)

---

## 🚀 Features

* 🤖 **ML-based requirement classification**
* 📝 **Vague-word detection**
* 📏 **Missing quantitative information detection**
* ⚙️ **Missing constraint detection**
* ⚠️ **Requirement conflict detection**
* 💡 **Automatic explanations & suggestions**
* ✨ **Improved requirement generation**
* 📊 **ML confidence & probability distribution**
* 📄 **Automatic TXT & PDF reports**
* 🔄 **File-change-based automation**
* 🌐 **Streamlit web interface**
* 🔌 **FastAPI REST API**
* 🧪 **18 automated tests**

---

## 🎯 Problem

Software requirements often contain unclear statements such as:

```text
❌ "The system should be very fast."

❌ "The website should be easy to use."

❌ "Users should be able to upload reports."

❌ "The system should handle many users."
```

These statements can be interpreted differently by developers and stakeholders.

### ✅ ReqLens

```text
Requirement
     ↓
🤖 ML Classification
     ↓
🔎 NLP + Rule Analysis
     ↓
⚠️ Ambiguity / Conflict Detection
     ↓
💡 Suggestions
     ↓
✨ Improved Requirement
     ↓
📄 Report
```

---

## 🤖 Machine Learning

ReqLens uses a traditional supervised ML pipeline:

```text
Dataset
   ↓
TF-IDF Vectorization
   ↓
Logistic Regression
   ↓
Requirement Category
```

### Categories

| Category                | Description                        |
| ----------------------- | ---------------------------------- |
| 🟢 `CLEAR`              | Specific or measurable requirement |
| 🔴 `VAGUE`              | Subjective or unclear wording      |
| 🟡 `MISSING_CONSTRAINT` | Missing important limits/details   |

### 📊 Dataset

**150 synthetic software requirements**

| Category           | Samples |
| ------------------ | ------: |
| CLEAR              |      50 |
| VAGUE              |      50 |
| MISSING_CONSTRAINT |      50 |
| **Total**          | **150** |

### 📈 Model Performance

**93.3% test accuracy** on the held-out test set.

A separate evaluation using **15 unseen requirements achieved 100% accuracy**.

> ⚠️ The dataset is synthetic, so these results should not be interpreted as real-world performance.

---

## 🔎 Requirement Analysis

Example:

```text
Requirement:
"The website should be very easy to use."

Category:
🔴 VAGUE

Severity:
🔴 HIGH

Detected:
"easy"

Suggestion:
Define measurable usability requirements
or specific user actions.
```

ReqLens can also detect missing information related to:

```text
📁 File size / formats
⏱️ Response time
👥 User capacity
💾 Data volume
🔔 Notifications
💳 Payments
🔎 Search
💿 Backups
🗄️ Data retention
```

---

## ⚠️ Conflict Detection

ReqLens can identify potentially conflicting requirements.

```text
Requirement 1:
"The application must respond within 2 seconds."

Requirement 2:
"The application must respond at least 5 seconds."

                    ↓

⚠️ Potential response-time conflict
```

It can also detect contradictory capacity constraints.

---

## 💡 Explanation & Improvement

```text
Original:
"The system should be very fast."

                    ↓

✨ Improved:
"The system must complete the requested
operation within 2 seconds under the
expected normal workload."
```

---

## 🌐 Web Interface

The Streamlit interface provides:

```text
📊 Dashboard
🤖 ML Prediction
📈 Confidence & Probability Distribution
🔎 Detailed Analysis
💡 Explanations
✨ Improved Requirements
⚠️ Conflict Detection
📄 PDF Report Download
```

---

## 🔌 REST API

Built with **FastAPI**.

| Method | Endpoint         | Purpose                       |
| ------ | ---------------- | ----------------------------- |
| `GET`  | `/`              | API health check              |
| `POST` | `/analyze`       | Analyze one requirement       |
| `POST` | `/analyze-batch` | Analyze multiple requirements |

Interactive API documentation is available through Swagger when the API is running.

---

## 🔄 Automation

ReqLens can automatically monitor the requirement input file:

```text
requirements_input.txt
        ↓
📝 File modified
        ↓
🔄 Automation triggered
        ↓
🔎 Requirements analyzed
        ↓
📄 TXT report
        ↓
📑 PDF report
        ↓
📋 Log generated
```

---

## 🧪 Testing

ReqLens currently has:

**18 automated tests — 18 passed ✅**

Tests cover:

* Core requirement analysis
* ML prediction
* Conflict detection
* FastAPI endpoints
* API validation
* Batch analysis
* Automation
* TXT/PDF report generation

Run:

```bash
pytest
```

---

## 🛠️ Tech Stack

```text
🐍 Python
🤖 Scikit-learn
📊 Pandas / NumPy
🧠 TF-IDF + Logistic Regression
⚡ FastAPI
🌐 Streamlit
📄 ReportLab
🧪 Pytest
🔧 Git / GitHub
```

---

## 📁 Project Structure

```text
reqlens/
│
├── app/
│   ├── analyzer.py
│   ├── api.py
│   ├── automation.py
│   ├── config.py
│   ├── explanation.py
│   ├── report_generator.py
│   ├── reqlens.py
│   ├── train_model.py
│   └── ui.py
│
├── data/
│   ├── dataset.csv
│   └── test_requirements.csv
│
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── tests/
│   ├── test_api.py
│   ├── test_automation.py
│   └── test_reqlens.py
│
├── requirements.txt
├── requirements_input.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

## ▶️ Run Locally

### 1️⃣ Clone

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/reqlens.git
cd reqlens
```

### 2️⃣ Create environment

```bash
python -m venv venv
```

### 3️⃣ Activate

```powershell
.\venv\Scripts\Activate.ps1
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run Streamlit

```bash
streamlit run app/ui.py
```

### 6️⃣ Run API

```bash
uvicorn api:app --reload --app-dir app
```

### 7️⃣ Run automation

```bash
python app/automation.py
```

### 8️⃣ Run tests

```bash
pytest
```

---

## 🔮 Future Improvements

* 🧠 Transformer/LLM-based analysis
* 📚 Larger real-world requirement dataset
* 🔎 Advanced conflict detection
* 🔗 GitHub requirement monitoring
* 🔄 CI/CD integration
* ☁️ Cloud deployment
* 👤 Authentication & requirement history

---

