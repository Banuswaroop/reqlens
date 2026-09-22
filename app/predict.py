import joblib

from config import (
MODEL_FILE,
VECTORIZER_FILE
)

# --------------------------------------------------

# Load trained ML model and TF-IDF vectorizer

# --------------------------------------------------

model = joblib.load(
MODEL_FILE
)

vectorizer = joblib.load(
VECTORIZER_FILE
)

# --------------------------------------------------

# Sample requirements

# --------------------------------------------------

requirements = [
"The application must display the user dashboard within 3 seconds.",
"The website should be incredibly easy to navigate.",
"Users should be able to upload reports.",
"The system must retain customer records for 5 years.",
"The application should provide outstanding performance.",
"The system should send notifications."
]

# --------------------------------------------------

# Make predictions

# --------------------------------------------------

for requirement in requirements:



 requirement_tfidf = vectorizer.transform(
    [requirement]
)

prediction = model.predict(
    requirement_tfidf
)

print("\nRequirement:")
print(requirement)

print("Predicted category:")
print(prediction[0])

