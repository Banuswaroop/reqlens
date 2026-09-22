import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

from config import (
    DATASET_FILE,
    MODEL_FILE,
    VECTORIZER_FILE
)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

data = pd.read_csv(
    DATASET_FILE
)


X = data["requirement"]
y = data["label"]


print("Requirements:")
print(X)


print("\nLabels:")
print(y)


# --------------------------------------------------
# Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print(
    "\nTraining requirements:",
    len(X_train)
)

print(
    "Testing requirements:",
    len(X_test)
)


# --------------------------------------------------
# TF-IDF vectorization
# --------------------------------------------------

vectorizer = TfidfVectorizer()


X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)


print(
    "\nTraining data shape:",
    X_train_tfidf.shape
)

print(
    "Testing data shape:",
    X_test_tfidf.shape
)


# --------------------------------------------------
# Vocabulary
# --------------------------------------------------

print(
    "\nVocabulary:"
)

print(
    vectorizer.get_feature_names_out()
)


# --------------------------------------------------
# Train model
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train_tfidf,
    y_train
)


print(
    "\nModel training completed!"
)


# --------------------------------------------------
# Save model and vectorizer
# --------------------------------------------------

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    vectorizer,
    VECTORIZER_FILE
)


print(
    "Model saved successfully:"
)

print(
    MODEL_FILE
)

print(
    "Vectorizer saved successfully:"
)

print(
    VECTORIZER_FILE
)


# --------------------------------------------------
# Evaluate model
# --------------------------------------------------

y_pred = model.predict(
    X_test_tfidf
)


# --------------------------------------------------
# Incorrect predictions
# --------------------------------------------------

print(
    "\nIncorrect Predictions:"
)


for requirement, actual, predicted in zip(
    X_test,
    y_test,
    y_pred
):

    if actual != predicted:

        print(
            "\nRequirement:",
            requirement
        )

        print(
            "Actual:",
            actual
        )

        print(
            "Predicted:",
            predicted
        )


# --------------------------------------------------
# Accuracy
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)


print(
    "\nAccuracy:",
    accuracy
)


# --------------------------------------------------
# Classification report
# --------------------------------------------------

print(
    "\nClassification Report:"
)

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

