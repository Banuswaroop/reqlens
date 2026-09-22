def generate_explanation(
    requirement,
    category,
    vague_words,
    suggestions
):

    # --------------------------------------------------
    # CLEAR REQUIREMENT
    # --------------------------------------------------

    if category == "CLEAR":

        return {
            "explanation": (
                "The requirement contains a measurable "
                "or sufficiently specific condition and "
                "does not show any major ambiguity."
            ),
            "rewritten_requirement": requirement
        }


    # --------------------------------------------------
    # VAGUE REQUIREMENT
    # --------------------------------------------------

    if category == "VAGUE":

        if vague_words:

            vague_word_text = ", ".join(
                vague_words
            )

            explanation = (
                "The requirement contains vague or "
                "subjective wording: "
                f"{vague_word_text}. "
                "These terms can be interpreted differently "
                "by different users or developers."
            )

        else:

            explanation = (
                "The requirement appears to contain "
                "vague or subjective language."
            )


        # ----------------------------------------------
        # Requirement-specific rewrites
        # ----------------------------------------------

        requirement_lower = requirement.lower()


        if (
            "easy" in requirement_lower
            or "easy-to-use" in requirement_lower
            or "user-friendly" in requirement_lower
            or "intuitive" in requirement_lower
        ):

            rewritten_requirement = (
                "The website must allow a new user to "
                "complete the primary task without "
                "assistance and within a defined time limit."
            )


        elif (
            "fast" in requirement_lower
            or "quickly" in requirement_lower
            or "very fast" in requirement_lower
            or "soon" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must complete the requested "
                "operation within 2 seconds under the "
                "expected normal workload."
            )


        elif (
            "efficient" in requirement_lower
            or "highly efficient" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must process the requested "
                "operation within a defined response time "
                "while remaining within the specified "
                "resource limits."
            )


        elif (
            "reliable" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must maintain at least 99.9% "
                "availability during each calendar month."
            )


        elif (
            "secure" in requirement_lower
            or "strong" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must enforce authentication, "
                "authorization, encrypted communication, "
                "and the security controls defined by the "
                "project security requirements."
            )


        elif (
            "large" in requirement_lower
            or "many" in requirement_lower
            or "huge" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must support up to a defined "
                "maximum number of records or resources "
                "under the expected workload."
            )


        elif (
            "smooth" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must complete the specified "
                "user interaction within the defined "
                "response-time limit without noticeable "
                "processing delays."
            )


        elif (
            "professional" in requirement_lower
            or "attractive" in requirement_lower
            or "pleasant" in requirement_lower
        ):

            rewritten_requirement = (
                "The interface must follow the project's "
                "defined visual design guidelines, including "
                "layout, typography, spacing, and accessibility "
                "requirements."
            )


        elif (
            "simple" in requirement_lower
        ):

            rewritten_requirement = (
                "The system must complete the specified "
                "workflow using a defined number of user "
                "steps and clearly documented actions."
            )


        else:

            rewritten_requirement = (
                "Replace the vague wording with measurable "
                "criteria such as a time limit, quantity, "
                "capacity, quality target, or user action."
            )


        return {
            "explanation": explanation,
            "rewritten_requirement": rewritten_requirement
        }


    # --------------------------------------------------
    # MISSING CONSTRAINT
    # --------------------------------------------------

    if category == "MISSING_CONSTRAINT":

        explanation = (
            "The requirement describes a system capability "
            "but may not specify important constraints such "
            "as limits, timing, capacity, formats, or "
            "expected behavior."
        )


        requirement_lower = requirement.lower()


        # ----------------------------------------------
        # Upload requirement
        # ----------------------------------------------

        if "upload" in requirement_lower:

            rewritten_requirement = (
                requirement
                + " The system must support files up to "
                "10 MB in PDF, DOCX, and TXT formats."
            )


        # ----------------------------------------------
        # Notification requirement
        # ----------------------------------------------

        elif (
            "notification" in requirement_lower
            or "notifications" in requirement_lower
        ):

            rewritten_requirement = (
                requirement
                + " Notifications must be delivered "
                "within 1 minute of the triggering event."
            )


        # ----------------------------------------------
        # Search requirement
        # ----------------------------------------------

        elif "search" in requirement_lower:

            rewritten_requirement = (
                requirement
                + " Search results must be returned "
                "within 2 seconds and limited to "
                "20 results per page."
            )


        # ----------------------------------------------
        # Payment requirement
        # ----------------------------------------------

        elif "payment" in requirement_lower:

            rewritten_requirement = (
                requirement
                + " Payment processing must complete "
                "within 5 seconds and clearly report "
                "success or failure."
            )


        # ----------------------------------------------
        # Backup requirement
        # ----------------------------------------------

        elif "backup" in requirement_lower:

            rewritten_requirement = (
                requirement
                + " Backups must run at least once every "
                "24 hours and be retained for 30 days."
            )


        # ----------------------------------------------
        # Storage / retention requirement
        # ----------------------------------------------

        elif (
            "store" in requirement_lower
            or "retain" in requirement_lower
        ):

            rewritten_requirement = (
                requirement
                + " The system must define the data "
                "retention period, storage capacity, "
                "and deletion policy."
            )


        # ----------------------------------------------
        # Generic missing constraint
        # ----------------------------------------------

        else:

            rewritten_requirement = (
                requirement
                + " The requirement must define the "
                "expected limits, timing, capacity, "
                "supported formats, and failure behavior."
            )


        return {
            "explanation": explanation,
            "rewritten_requirement": rewritten_requirement
        }


    # --------------------------------------------------
    # UNKNOWN CATEGORY
    # --------------------------------------------------

    return {
        "explanation": (
            "ReqLens could not generate a detailed "
            "explanation for this requirement."
        ),
        "rewritten_requirement": requirement
    }

