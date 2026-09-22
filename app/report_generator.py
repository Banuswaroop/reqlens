import joblib

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reqlens import classify_requirement
from explanation import generate_explanation


# ==================================================
# GENERATE PDF REPORT
# ==================================================

def generate_pdf_report(
    requirements,
    analyses,
    conflicts
):

    buffer = BytesIO()


    # ==================================================
    # DOCUMENT
    # ==================================================

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )


    # ==================================================
    # STYLES
    # ==================================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=6
    )


    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=18
    )


    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=12,
        spaceAfter=10
    )


    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )


    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontSize=9,
        leading=12
    )


    requirement_style = ParagraphStyle(
        "RequirementStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )


    # ==================================================
    # STORY
    # ==================================================

    story = []


    # ==================================================
    # TITLE
    # ==================================================

    story.append(
        Paragraph(
            "ReqLens",
            title_style
        )
    )


    story.append(
        Paragraph(
            "Software Requirement Analysis Report",
            subtitle_style
        )
    )


    generated_at = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )


    story.append(
        Paragraph(
            f"<b>Generated:</b> {generated_at}",
            small_style
        )
    )


    story.append(
        Spacer(
            1,
            12
        )
    )


    # ==================================================
    # EXECUTIVE SUMMARY
    # ==================================================

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


    story.append(
        Paragraph(
            "Executive Summary",
            section_style
        )
    )


    summary_data = [
        [
            "Metric",
            "Count"
        ],
        [
            "Total Requirements",
            str(len(requirements))
        ],
        [
            "Clear",
            str(clear_count)
        ],
        [
            "Vague",
            str(vague_count)
        ],
        [
            "Missing Constraints",
            str(missing_count)
        ],
        [
            "Potential Conflicts",
            str(len(conflicts))
        ]
    ]


    summary_table = Table(
        summary_data,
        colWidths=[
            110 * mm,
            40 * mm
        ]
    )


    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F2937")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )


    story.append(
        summary_table
    )


    story.append(
        Spacer(
            1,
            15
        )
    )


    # ==================================================
    # REQUIREMENT ANALYSIS
    # ==================================================

    story.append(
        Paragraph(
            "Requirement Analysis",
            section_style
        )
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
        # ML DETAILS
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
        # EXPLANATION
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


        rewritten_requirement = (
            explanation_result[
                "rewritten_requirement"
            ]
        )


        # --------------------------------------------------
        # Requirement heading
        # --------------------------------------------------

        story.append(
            Paragraph(
                f"<b>Requirement {index + 1}</b>",
                normal_style
            )
        )


        story.append(
            Spacer(
                1,
                4
            )
        )


        story.append(
            Paragraph(
                requirement,
                requirement_style
            )
        )


        # --------------------------------------------------
        # Classification
        # --------------------------------------------------

        details_data = [
            [
                "Category",
                category
            ],
            [
                "Severity",
                severity
            ],
            [
                "Detected Issue",
                issue
            ],
            [
                "ML Prediction",
                ml_prediction
            ],
            [
                "ML Confidence",
                f"{ml_confidence:.2%}"
            ]
        ]


        details_table = Table(
            details_data,
            colWidths=[
                40 * mm,
                110 * mm
            ]
        )


        details_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E5E7EB")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )


        story.append(
            details_table
        )


        # --------------------------------------------------
        # ML Probability Distribution
        # --------------------------------------------------

        story.append(
            Spacer(
                1,
                8
            )
        )


        story.append(
            Paragraph(
                "<b>ML Probability Distribution</b>",
                small_style
            )
        )


        probability_data = [
            [
                "Category",
                "Probability"
            ],
            [
                "CLEAR",
                f"{probability_details.get('CLEAR', 0):.2%}"
            ],
            [
                "MISSING_CONSTRAINT",
                f"{probability_details.get('MISSING_CONSTRAINT', 0):.2%}"
            ],
            [
                "VAGUE",
                f"{probability_details.get('VAGUE', 0):.2%}"
            ]
        ]


        probability_table = Table(
            probability_data,
            colWidths=[
                90 * mm,
                60 * mm
            ]
        )


        probability_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#F3F4F6")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )


        story.append(
            probability_table
        )


        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        story.append(
            Spacer(
                1,
                8
            )
        )


        story.append(
            Paragraph(
                "<b>Why was this detected?</b>",
                small_style
            )
        )


        story.append(
            Paragraph(
                explanation,
                small_style
            )
        )


        # --------------------------------------------------
        # Vague Words
        # --------------------------------------------------

        if vague_words:

            story.append(
                Spacer(
                    1,
                    7
                )
            )


            story.append(
                Paragraph(
                    "<b>Vague Words Detected</b>",
                    small_style
                )
            )


            story.append(
                Paragraph(
                    ", ".join(
                        vague_words
                    ),
                    small_style
                )
            )


        # --------------------------------------------------
        # Suggestions
        # --------------------------------------------------

        if suggestions:

            story.append(
                Spacer(
                    1,
                    7
                )
            )


            story.append(
                Paragraph(
                    "<b>Clarification Suggestions</b>",
                    small_style
                )
            )


            for suggestion in suggestions:

                story.append(
                    Paragraph(
                        f"• {suggestion}",
                        small_style
                    )
                )


        # --------------------------------------------------
        # Improved Requirement
        # --------------------------------------------------

        story.append(
            Spacer(
                1,
                7
            )
        )


        story.append(
            Paragraph(
                "<b>Example of an Improved Requirement</b>",
                small_style
            )
        )


        story.append(
            Paragraph(
                rewritten_requirement,
                small_style
            )
        )


        story.append(
            Spacer(
                1,
                14
            )
        )


    # ==================================================
    # PAGE BREAK
    # ==================================================

    story.append(
        PageBreak()
    )


    # ==================================================
    # POTENTIAL CONFLICTS
    # ==================================================

    story.append(
        Paragraph(
            "Potential Conflicts",
            section_style
        )
    )


    if conflicts:

        story.append(
            Paragraph(
                f"<b>{len(conflicts)}</b> "
                "potential conflict(s) detected.",
                normal_style
            )
        )


        story.append(
            Spacer(
                1,
                10
            )
        )


        for index, (
            requirement_a,
            requirement_b,
            message
        ) in enumerate(
            conflicts,
            start=1
        ):

            story.append(
                Paragraph(
                    f"<b>Conflict {index}</b>",
                    normal_style
                )
            )


            story.append(
                Spacer(
                    1,
                    6
                )
            )


            conflict_data = [
                [
                    "Requirement 1",
                    Paragraph(
                        requirement_a,
                        small_style
                    )
                ],
                [
                    "Requirement 2",
                    Paragraph(
                        requirement_b,
                        small_style
                    )
                ],
                [
                    "Issue",
                    Paragraph(
                        message,
                        small_style
                    )
                ]
            ]


            conflict_table = Table(
                conflict_data,
                colWidths=[
                    40 * mm,
                    110 * mm
                ]
            )


            conflict_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#E5E7EB")
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )


            story.append(
                conflict_table
            )


            story.append(
                Spacer(
                    1,
                    14
                )
            )


    else:

        story.append(
            Paragraph(
                "No potential conflicts were detected.",
                normal_style
            )
        )


    # ==================================================
    # FOOTER
    # ==================================================

    story.append(
        Spacer(
            1,
            20
        )
    )


    story.append(
        Paragraph(
            "Generated by ReqLens - "
            "Software Requirement Analysis System",
            small_style
        )
    )


    # ==================================================
    # BUILD PDF
    # ==================================================

    document.build(
        story
    )


    buffer.seek(
        0
    )


    return buffer.getvalue()
