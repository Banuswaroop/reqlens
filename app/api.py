from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from reqlens import (
    analyze_requirement,
    analyze_requirements,
    get_prediction_details
)

from explanation import generate_explanation


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="ReqLens API",
    description="API for software requirement ambiguity analysis",
    version="1.0.0"
)


# ==================================================
# REQUEST MODELS
# ==================================================

class RequirementRequest(BaseModel):

    requirement: str = Field(
        ...,
        min_length=1,
        description="Software requirement to analyze"
    )

    @field_validator("requirement")
    @classmethod
    def validate_requirement(cls, value):

        if not value.strip():
            raise ValueError(
                "Requirement cannot be empty."
            )

        return value.strip()


class BatchRequirementRequest(BaseModel):

    requirements: list[str] = Field(
        ...,
        min_length=1,
        description="List of software requirements"
    )

    @field_validator("requirements")
    @classmethod
    def validate_requirements(cls, values):

        cleaned_requirements = []

        for requirement in values:

            if not isinstance(
                requirement,
                str
            ):
                raise ValueError(
                    "Every requirement must be a string."
                )

            requirement = requirement.strip()

            if not requirement:
                raise ValueError(
                    "Requirements cannot be empty."
                )

            cleaned_requirements.append(
                requirement
            )

        return cleaned_requirements


# ==================================================
# ROOT ENDPOINT
# ==================================================

@app.get("/")
def root():

    return {
        "message": "ReqLens API is running"
    }


# ==================================================
# SINGLE REQUIREMENT ANALYSIS
# ==================================================

@app.post("/analyze")
def analyze(request: RequirementRequest):

    (
        category,
        severity,
        issue,
        vague_words,
        suggestions
    ) = analyze_requirement(
        request.requirement
    )

    (
        ml_prediction,
        ml_confidence,
        probability_details
    ) = get_prediction_details(
        request.requirement
    )

    explanation_result = generate_explanation(
        request.requirement,
        category,
        vague_words,
        suggestions
    )

    return {

        "requirement":
            request.requirement,

        "category":
            category,

        "severity":
            severity,

        "detected_issue":
            issue,

        "vague_words":
            vague_words,

        "suggestions":
            suggestions,

        "improved_requirement":
            explanation_result[
                "rewritten_requirement"
            ],

        "explanation":
            explanation_result[
                "explanation"
            ],

        "machine_learning": {

            "prediction":
                ml_prediction,

            "confidence":
                float(
                    ml_confidence
                ),

            "probability_distribution": {

                category:
                    float(
                        probability
                    )

                for category, probability
                in probability_details.items()
            }
        }
    }


# ==================================================
# BATCH REQUIREMENT ANALYSIS
# ==================================================

@app.post("/analyze-batch")
def analyze_batch(
    request: BatchRequirementRequest
):

    requirements = request.requirements

    analyses, conflicts = analyze_requirements(
        requirements
    )

    results = []

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

        (
            ml_prediction,
            ml_confidence,
            probability_details
        ) = get_prediction_details(
            requirement
        )

        explanation_result = generate_explanation(
            requirement,
            category,
            vague_words,
            suggestions
        )

        results.append(
            {

                "requirement":
                    requirement,

                "category":
                    category,

                "severity":
                    severity,

                "detected_issue":
                    issue,

                "vague_words":
                    vague_words,

                "suggestions":
                    suggestions,

                "improved_requirement":
                    explanation_result[
                        "rewritten_requirement"
                    ],

                "explanation":
                    explanation_result[
                        "explanation"
                    ],

                "machine_learning": {

                    "prediction":
                        ml_prediction,

                    "confidence":
                        float(
                            ml_confidence
                        ),

                    "probability_distribution": {

                        category:
                            float(
                                probability
                            )

                        for category, probability
                        in probability_details.items()
                    }
                }
            }
        )

    return {

        "total_requirements":
            len(requirements),

        "results":
            results,

        "potential_conflicts": [

            {
                "requirement_1":
                    conflict[0],

                "requirement_2":
                    conflict[1],

                "issue":
                    conflict[2]
            }

            for conflict in conflicts
        ]
    }