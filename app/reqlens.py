import joblib

from analyzer import (
    find_vague_words,
    generate_suggestions,
    find_missing_constraints,
    find_missing_quantitative_info,
    find_conflicts
)

from config import (
    MODEL_FILE,
    VECTORIZER_FILE
)


# ==================================================
# LOAD ML MODEL
# ==================================================

model = joblib.load(
    MODEL_FILE
)

vectorizer = joblib.load(
    VECTORIZER_FILE
)


# ==================================================
# SEVERITY
# ==================================================

def get_severity(category):

    if category == "CLEAR":
        return "LOW"

    elif category == "MISSING_CONSTRAINT":
        return "MEDIUM"

    elif category == "VAGUE":
        return "HIGH"

    return "UNKNOWN"


# ==================================================
# ISSUE DESCRIPTION
# ==================================================

def get_issue_description(category):

    if category == "CLEAR":

        return (
            "No major ambiguity was detected."
        )

    elif category == "VAGUE":

        return (
            "The requirement contains vague "
            "or subjective wording."
        )

    elif category == "MISSING_CONSTRAINT":

        return (
            "The requirement may be missing "
            "important constraints or details."
        )

    return (
        "The requirement could not be categorized."
    )


# ==================================================
# ML PREDICTION DETAILS
# ==================================================

def get_prediction_details(requirement):

    requirement_tfidf = vectorizer.transform(
        [requirement]
    )

    probabilities = model.predict_proba(
        requirement_tfidf
    )[0]

    classes = model.classes_

    prediction_index = probabilities.argmax()

    prediction = classes[
        prediction_index
    ]

    confidence = probabilities[
        prediction_index
    ]

    probability_details = {}

    for category, probability in zip(
        classes,
        probabilities
    ):

        probability_details[
            category
        ] = probability

    return (
        prediction,
        confidence,
        probability_details
    )


# ==================================================
# COMBINED CLASSIFICATION
# ==================================================

def classify_requirement(requirement):

    (
        ml_prediction,
        ml_confidence,
        probability_details
    ) = get_prediction_details(
        requirement
    )


    vague_words = find_vague_words(
        requirement
    )

    missing_constraints = find_missing_constraints(
        requirement
    )

    missing_quantitative_info = (
        find_missing_quantitative_info(
            requirement
        )
    )


    if vague_words:

        category = "VAGUE"

    elif (
        missing_constraints
        or missing_quantitative_info
    ):

        category = "MISSING_CONSTRAINT"

    else:

        category = ml_prediction


    return (
        category,
        ml_prediction,
        ml_confidence,
        probability_details,
        vague_words,
        missing_constraints,
        missing_quantitative_info
    )


# ==================================================
# ANALYZE SINGLE REQUIREMENT
# ==================================================

def analyze_requirement(requirement):

    (
        category,
        ml_prediction,
        ml_confidence,
        probability_details,
        vague_words,
        missing_constraints,
        missing_quantitative_info
    ) = classify_requirement(
        requirement
    )


    suggestions = []


    if category == "VAGUE":

        suggestions.extend(
            generate_suggestions(
                vague_words
            )
        )

    elif category == "MISSING_CONSTRAINT":

        suggestions.extend(
            missing_constraints
        )

        suggestions.extend(
            missing_quantitative_info
        )


    suggestions = list(
        dict.fromkeys(
            suggestions
        )
    )


    severity = get_severity(
        category
    )


    issue = get_issue_description(
        category
    )


    return (
        category,
        severity,
        issue,
        vague_words,
        suggestions
    )


# ==================================================
# ANALYZE MULTIPLE REQUIREMENTS
# ==================================================

def analyze_requirements(requirements):

    analyses = []


    for requirement in requirements:

        result = analyze_requirement(
            requirement
        )

        analyses.append(
            result
        )


    conflicts = find_conflicts(
        requirements
    )


    return (
        analyses,
        conflicts
    )


# ==================================================
# CREATE TEXT REPORT
# ==================================================

def create_report(
    requirements,
    analyses,
    conflicts
):

    report_lines = []


    report_lines.append(
        "=" * 60
    )

    report_lines.append(
        "                 ReqLens Report"
    )

    report_lines.append(
        "=" * 60
    )

    report_lines.append(
        "\nRequirement Analysis"
    )

    report_lines.append(
        "=" * 60
    )


    for index, requirement in enumerate(
        requirements
    ):

        (
            category,
            severity,
            issue,
            vague_words,
            suggestions
        ) = analyses[index]


        report_lines.append(
            f"\nRequirement {index + 1}:"
        )

        report_lines.append(
            requirement
        )

        report_lines.append(
            f"\nCategory: {category}"
        )

        report_lines.append(
            f"Severity: {severity}"
        )

        report_lines.append(
            f"Detected Issue: {issue}"
        )


        if vague_words:

            report_lines.append(
                "\nVague Words:"
            )

            report_lines.append(
                ", ".join(vague_words)
            )


        if suggestions:

            report_lines.append(
                "\nSuggestions:"
            )


            for suggestion in suggestions:

                report_lines.append(
                    "- " + suggestion
                )


        report_lines.append(
            "-" * 60
        )


    report_lines.append(
        "\nPotential Conflicts"
    )

    report_lines.append(
        "=" * 60
    )


    if conflicts:

        report_lines.append(
            f"{len(conflicts)} potential "
            "conflict(s) detected."
        )


        for index, (
            requirement_a,
            requirement_b,
            message
        ) in enumerate(
            conflicts,
            start=1
        ):

            report_lines.append(
                f"\nConflict {index}:"
            )

            report_lines.append(
                "\nRequirement 1:"
            )

            report_lines.append(
                requirement_a
            )

            report_lines.append(
                "\nRequirement 2:"
            )

            report_lines.append(
                requirement_b
            )

            report_lines.append(
                "\nIssue:"
            )

            report_lines.append(
                message
            )

            report_lines.append(
                "-" * 60
            )


    else:

        report_lines.append(
            "No potential conflicts detected."
        )


    return "\n".join(
        report_lines
    )


# ==================================================
# CLI
# ==================================================

def run_cli():

    print(
        "\n" + "=" * 60
    )

    print(
        "                 ReqLens"
    )

    print(
        "      Software Requirement Analyzer"
    )

    print(
        "=" * 60
    )

    print(
        "\nEnter a requirement to analyze."
    )

    print(
        "Type 'exit' to stop ReqLens."
    )


    while True:

        requirement = input(
            "\nRequirement: "
        )


        if requirement.lower() == "exit":

            print(
                "\nReqLens stopped."
            )

            break


        if not requirement.strip():

            print(
                "Please enter a requirement."
            )

            continue


        (
            category,
            severity,
            issue,
            vague_words,
            suggestions
        ) = analyze_requirement(
            requirement
        )


        print(
            "\n" + "-" * 60
        )

        print(
            "Category:",
            category
        )

        print(
            "Severity:",
            severity
        )

        print(
            "Detected Issue:",
            issue
        )


        if vague_words:

            print(
                "Vague words:",
                vague_words
            )


        if suggestions:

            print(
                "\nSuggestions:"
            )


            for suggestion in suggestions:

                print(
                    "-",
                    suggestion
                )


        print(
            "-" * 60
        )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    run_cli()

