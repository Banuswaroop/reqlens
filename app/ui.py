import streamlit as st

from reqlens import (
    analyze_requirements,
    classify_requirement
)

from report_generator import generate_pdf_report
from explanation import generate_explanation


st.set_page_config(
    page_title="ReqLens",
    page_icon="🔍",
    layout="centered"
)


st.title("🔍 ReqLens")

st.write(
    "AI-powered software requirement ambiguity detector"
)


st.subheader("Enter Requirements")


requirements_text = st.text_area(
    "Requirements:",
    placeholder=(
        "Enter one requirement per line...\n\n"
        "Example:\n"
        "The application must respond within 2 seconds.\n"
        "The website should be very easy to use."
    ),
    height=200
)


if st.button("Analyze Requirements"):

    if not requirements_text.strip():

        st.warning(
            "Please enter at least one requirement."
        )

    else:

        requirements = [
            line.strip()
            for line in requirements_text.split("\n")
            if line.strip()
        ]

        analyses, conflicts = analyze_requirements(
            requirements
        )

        st.success(
            "Requirements analyzed successfully!"
        )


        # ==================================================
        # EXECUTIVE DASHBOARD
        # ==================================================

        st.subheader("Executive Summary")


        total_count = len(requirements)

        clear_count = 0
        vague_count = 0
        missing_count = 0


        for analysis in analyses:

            category = analysis[0]

            if category == "CLEAR":

                clear_count += 1

            elif category == "VAGUE":

                vague_count += 1

            elif category == "MISSING_CONSTRAINT":

                missing_count += 1


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Total",
                total_count
            )


        with col2:

            st.metric(
                "Clear",
                clear_count
            )


        with col3:

            st.metric(
                "Vague",
                vague_count
            )


        with col4:

            st.metric(
                "Missing",
                missing_count
            )


        # ==================================================
        # CATEGORY DISTRIBUTION
        # ==================================================

        st.subheader(
            "Requirement Classification"
        )


        chart_data = {
            "Category": [
                "Clear",
                "Vague",
                "Missing Constraints"
            ],
            "Count": [
                clear_count,
                vague_count,
                missing_count
            ]
        }


        st.bar_chart(
            chart_data,
            x="Category",
            y="Count"
        )


        # ==================================================
        # DETAILED ANALYSIS
        # ==================================================

        st.subheader(
            "Detailed Analysis"
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


            # --------------------------------------------------
            # Get ML Prediction Details
            # --------------------------------------------------

            (
                _,
                ml_prediction,
                ml_confidence,
                probability_details,
                _,
                _,
                _
            ) = classify_requirement(
                requirement
            )


            # --------------------------------------------------
            # Generate Explanation
            # --------------------------------------------------

            explanation_result = generate_explanation(
                requirement,
                category,
                vague_words,
                suggestions
            )


            explanation = explanation_result[
                "explanation"
            ]


            rewritten_requirement = explanation_result[
                "rewritten_requirement"
            ]


            # ----------------------------------------------
            # Requirement Card
            # ----------------------------------------------

            with st.expander(
                f"Requirement {index + 1}: {requirement}"
            ):

                # ------------------------------------------
                # Classification
                # ------------------------------------------

                st.write(
                    "**Classification**"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        f"Category: **{category}**"
                    )


                with col2:

                    st.write(
                        f"Severity: **{severity}**"
                    )


                st.divider()


                # ------------------------------------------
                # ML Prediction
                # ------------------------------------------

                st.write(
                    "**ML Model Prediction**"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.write(
                        f"Prediction: **{ml_prediction}**"
                    )


                with col2:

                    st.write(
                        f"Confidence: **{ml_confidence:.2%}**"
                    )


                st.progress(
                    float(ml_confidence)
                )


                # ------------------------------------------
                # Probability Distribution
                # ------------------------------------------

                st.write(
                    "**ML Probability Distribution**"
                )


                probability_data = {
                    "Category": [
                        "CLEAR",
                        "MISSING_CONSTRAINT",
                        "VAGUE"
                    ],
                    "Probability": [
                        probability_details.get(
                            "CLEAR",
                            0
                        ),
                        probability_details.get(
                            "MISSING_CONSTRAINT",
                            0
                        ),
                        probability_details.get(
                            "VAGUE",
                            0
                        )
                    ]
                }


                st.bar_chart(
                    probability_data,
                    x="Category",
                    y="Probability"
                )


                st.divider()


                # ------------------------------------------
                # Detected Issue
                # ------------------------------------------

                st.write(
                    "**1. Detected Issue**"
                )


                st.write(
                    issue
                )


                # ------------------------------------------
                # Explanation
                # ------------------------------------------

                st.write(
                    "**2. Why was this detected?**"
                )


                st.info(
                    explanation
                )


                # ------------------------------------------
                # Detected Vague Words
                # ------------------------------------------

                if vague_words:

                    st.write(
                        "**3. Vague Words Detected**"
                    )


                    st.write(
                        ", ".join(vague_words)
                    )


                # ------------------------------------------
                # Clarification Suggestions
                # ------------------------------------------

                if suggestions:

                    st.write(
                        "**4. Clarification Suggestions**"
                    )


                    for suggestion in suggestions:

                        st.write(
                            f"- {suggestion}"
                        )


                # ------------------------------------------
                # Rewritten Requirement
                # ------------------------------------------

                st.write(
                    "**5. Example of an Improved Requirement**"
                )


                st.success(
                    rewritten_requirement
                )


                # ------------------------------------------
                # Status
                # ------------------------------------------

                if category == "CLEAR":

                    st.success(
                        "✓ This requirement appears sufficiently specific."
                    )


                elif category == "VAGUE":

                    st.error(
                        "⚠ This requirement contains vague or subjective wording."
                    )


                elif category == "MISSING_CONSTRAINT":

                    st.warning(
                        "⚠ This requirement may need additional constraints or details."
                    )


        # ==================================================
        # POTENTIAL CONFLICTS
        # ==================================================

        st.subheader(
            "Potential Conflicts"
        )


        if conflicts:

            st.warning(
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

                with st.expander(
                    f"Conflict {index}"
                ):

                    st.write(
                        "**Requirement 1:**"
                    )


                    st.write(
                        requirement_a
                    )


                    st.write(
                        "**Requirement 2:**"
                    )


                    st.write(
                        requirement_b
                    )


                    st.write(
                        f"**Issue:** {message}"
                    )


        else:

            st.success(
                "No potential conflicts detected."
            )


        # ==================================================
        # PDF REPORT
        # ==================================================

        st.subheader(
            "PDF Report"
        )


        try:

            pdf_bytes = generate_pdf_report(
                requirements,
                analyses,
                conflicts
            )


            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="reqlens_report.pdf",
                mime="application/pdf"
            )


        except Exception as error:

            st.error(
                "PDF generation failed."
            )


            st.exception(
                error
            )
