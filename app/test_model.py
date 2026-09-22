import pandas as pd
import joblib

from config import (
    MODEL_FILE,
    VECTORIZER_FILE
)


# --------------------------------------------------
# Load Model
# --------------------------------------------------

model = joblib.load(
    MODEL_FILE
)


vectorizer = joblib.load(
    VECTORIZER_FILE
)


# --------------------------------------------------
# Load Test Dataset
# --------------------------------------------------

test_data = pd.read_csv(
    "data/test_requirements.csv"
)


requirements = test_data[
    "requirement"
]


expected_labels = test_data[
    "expected_label"
]


# --------------------------------------------------
# Predictions
# --------------------------------------------------

predicted_labels = []


for requirement in requirements:

    requirement_tfidf = vectorizer.transform(
        [requirement]
    )


    prediction = model.predict(
        requirement_tfidf
    )[0]


    predicted_labels.append(
        prediction
    )


# --------------------------------------------------
# Display Results
# --------------------------------------------------

print(
    "\n" + "=" * 70
)

print(
    "                    ReqLens Model Test"
)

print(
    "=" * 70
)


correct = 0


for index in range(
    len(requirements)
):

    requirement = requirements.iloc[index]

    expected = expected_labels.iloc[index]

    predicted = predicted_labels[index]


    print(
        f"\nTest {index + 1}"
    )

    print(
        "Requirement:",
        requirement
    )

    print(
        "Expected:",
        expected
    )

    print(
        "Predicted:",
        predicted
    )


    if expected == predicted:

        print(
            "Result: PASS"
        )

        correct += 1

    else:

        print(
            "Result: FAIL"
        )


# --------------------------------------------------
# Accuracy
# --------------------------------------------------

total = len(
    requirements
)


accuracy = (
    correct / total
) * 100


print(
    "\n" + "=" * 70
)


print(
    "Testing completed."
)


print(
    f"Correct predictions: {correct}/{total}"
)


print(
    f"Test accuracy: {accuracy:.2f}%"
)


print(
    "=" * 70
)
