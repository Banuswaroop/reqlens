# 🔍 ReqLens

**AI-powered software requirement ambiguity detector**

ReqLens analyzes software requirements and identifies vague wording, missing constraints, and potential conflicts before they become development problems.

---

## 📌 Problem

Software requirements are often written using unclear or subjective language such as:

* "The system should respond quickly."
* "The application should be easy to use."
* "Users should be able to upload large files."
* "The system should provide high performance."

These requirements may be difficult for developers and testers to implement because important details are not clearly defined.

ReqLens helps identify these issues and suggests what information should be clarified.

---

## 🎯 Features

* Detects **vague requirements**
* Detects **missing constraints**
* Detects **potential conflicts between requirements**
* Uses a **Machine Learning classification model**
* Uses **rule-based NLP analysis**
* Generates clarification suggestions
* Automatically monitors requirement files
* Automatically generates analysis reports
* Provides an interactive Streamlit interface
* Maintains application logs
* Supports multiple requirements at once

---

## 🏗️ Project Architecture

```text
                    Software Requirements
                            │
                            ▼
                   ┌─────────────────┐
                   │   Input File    │
                   │ / Streamlit UI  │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   TF-IDF        │
                   │  Vectorization  │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Logistic        │
                   │ Regression ML   │
                   └────────┬────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │ Requirement Classification │
              └─────────────┬───────────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
           CLEAR          VAGUE       MISSING
                                     CONSTRAINT
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                   Rule-Based Analysis
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Vague Words   Missing Details   Conflicts
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    Suggestions
                            │
                            ▼
                     Analysis Report
```

---

## 🤖 Machine Learning Workflow

ReqLens uses a traditional supervised Machine Learning pipeline.

```text
Dataset
   ↓
Train/Test Split
   ↓
TF-IDF Vectorization
   ↓
Logistic Regression
   ↓
Model Evaluation
   ↓
Save Model + Vectorizer
   ↓
Use Model for Predictions
```

### Dataset

The current dataset contains **150 synthetic software requirements**:

| Category           | Examples |
| ------------------ | -------: |
| CLEAR              |       50 |
| VAGUE              |       50 |
| MISSING_CONSTRAINT |       50 |
| **Total**          |  **150** |

The dataset is balanced across the three categories.

### Features

The text requirements are converted into numerical features using **TF-IDF (Term Frequency–Inverse Document Frequency)**.

The classifier used is **Logistic Regression**.

---

## 📊 Model Results

The current model achieved:

```text
Test Accuracy: 93.3%
```

Classification performance on the test set:

```text
                    precision    recall    f1-score

CLEAR                  1.00       1.00       1.00
MISSING_CONSTRAINT     0.90       0.90       0.90
VAGUE                  0.90       0.90       0.90

Accuracy: 0.93
```

The evaluation uses a held-out test set from the current **synthetic dataset of 150 requirements**. Therefore, this result should not be interpreted as real-world production accuracy.

---

## 🧠 Requirement Analysis

After ML classification, ReqLens performs additional rule-based analysis.

### Vague Words

ReqLens detects words such as:

```text
quickly
easy
user-friendly
efficient
secure
large
many
reliable
scalable
```

For example:

```text
The application should load quickly.
```

ReqLens can identify:

```text
Vague Word:
quickly

Suggestion:
Specify a maximum response or loading time,
such as 2 seconds.
```

---

### Missing Constraints

ReqLens checks whether important details may be missing.

Example:

```text
Users should be able to upload reports.
```

ReqLens may suggest:

```text
Specify the maximum file size and
allowed file formats.
```

---

### Potential Conflicts

ReqLens can also compare multiple requirements.

Example:

```text
The system must respond within 2 seconds.

The system should wait at least 10 seconds
before responding.
```

ReqLens detects this as a potential response-time conflict.

---

## ⚙️ Automation

ReqLens includes a file-monitoring automation system.

```text
Developer modifies requirements_input.txt
                    ↓
              File change detected
                    ↓
              ReqLens starts analysis
                    ↓
               ML prediction
                    ↓
             Rule-based analysis
                    ↓
             Conflict detection
                    ↓
              Report generated
                    ↓
              Log entry created
```

The automation process checks the requirement file periodically.

Current polling interval:

```text
2 seconds
```

The generated report is stored in:

```text
reports/reqlens_report.txt
```

Application logs are stored in:

```text
logs/reqlens.log
```

---

## 🖥️ Streamlit Interface

ReqLens also provides an interactive web interface using Streamlit.

The interface allows users to:

1. Enter multiple requirements.
2. Analyze all requirements.
3. View ML classifications.
4. View severity levels.
5. View detected issues.
6. View vague words.
7. View clarification suggestions.
8. View potential conflicts.
9. Download the generated report.

---

## 📁 Project Structure

```text
reqlens/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── analyzer.py
│   ├── reqlens.py
│   ├── automation.py
│   ├── ui.py
│   ├── train_model.py
│   └── predict.py
│
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── data/
│   └── dataset.csv
│
├── reports/
│   └── reqlens_report.txt
│
├── logs/
│   └── reqlens.log
│
├── requirements_input.txt
├── requirements.txt
└── README.md
```

---

## 🔧 Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-learn
* TF-IDF
* Logistic Regression

### Data Processing

* Pandas

### Model Persistence

* Joblib

### User Interface

* Streamlit

### Development Tools

* VS Code
* Git
* GitHub

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd reqlens
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Train the Model

From the project root:

```bash
python app/train_model.py
```

This trains the model and creates:

```text
models/model.pkl
models/vectorizer.pkl
```

---

## 🔮 Test Predictions

Run:

```bash
python app/predict.py
```

This uses the trained model to classify sample requirements.

---

## 🖥️ Run the Web Interface

From the project root:

```bash
streamlit run app/ui.py
```

Streamlit will start the local web application.

---

## ⚡ Run Automation

From another terminal with the virtual environment activated:

```bash
python app/automation.py
```

ReqLens will monitor:

```text
requirements_input.txt
```

Modify the file to trigger automatic analysis.

Press:

```text
Ctrl + C
```

to stop the automation process.

---

## 📝 Example Input

Add requirements such as:

```text
The application must display the dashboard within 3 seconds.
The website should be incredibly easy to navigate.
Users should be able to upload reports.
The system must retain customer records for 5 years.
The application should provide outstanding performance.
The system should send notifications.
```

ReqLens analyzes each requirement and generates classifications, severity levels, issues, and suggestions.

---

## 📄 Generated Report

The analysis report is automatically generated at:

```text
reports/reqlens_report.txt
```

The report contains:

* Requirement
* Category
* Severity
* Detected issue
* Vague words
* Suggestions
* Potential conflicts

---

## 📋 Severity Levels

ReqLens currently maps categories to severity levels as follows:

| Category           | Severity |
| ------------------ | -------- |
| CLEAR              | LOW      |
| MISSING_CONSTRAINT | MEDIUM   |
| VAGUE              | HIGH     |

These are application-defined severity levels intended to prioritize clarification work.

---

## 🔍 Example Workflow

```text
Requirement:
"The application should load quickly."

        ↓

ML Classification:
VAGUE

        ↓

Severity:
HIGH

        ↓

Detected Issue:
The requirement contains vague or subjective wording.

        ↓

Detected Word:
quickly

        ↓

Suggestion:
Specify a maximum response or loading time,
such as 2 seconds.
```

---

## 🧩 Design Approach

ReqLens combines multiple techniques rather than relying on a single component.

### Machine Learning

Used for:

```text
Requirement → Category
```

### Rule-Based Analysis

Used for:

```text
Category → Specific issue
```

### Automation

Used for:

```text
File change → Automatic analysis
```

### Reporting

Used for:

```text
Analysis → Persistent report
```

This separation keeps the project modular and makes individual components easier to test and improve.

---

## 🔮 Future Improvements

Potential future enhancements include:

* Larger real-world requirement datasets
* More requirement categories
* Advanced NLP models
* Transformer-based classification
* Better conflict detection
* Requirement completeness scoring
* Confidence scores
* Improved clarification generation
* REST API
* Database storage
* User authentication
* Cloud deployment
* CI/CD automation
* Integration with GitHub Issues or project management tools

---

## 👨‍💻 Project Purpose

ReqLens was developed as a practical project to explore the complete workflow of an AI/ML application:

```text
Problem Definition
      ↓
Dataset Creation
      ↓
Data Processing
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Rule-Based Analysis
      ↓
Automation
      ↓
User Interface
      ↓
Report Generation
      ↓
Testing
      ↓
Deployment
```

The project demonstrates how Machine Learning, NLP-style rule analysis, software engineering, and automation can be combined into a single practical application.
