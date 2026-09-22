import re


# ==================================================
# VAGUE WORD DETECTION
# ==================================================

VAGUE_WORDS = [
    "quickly",
    "fast",
    "very fast",
    "easy",
    "easy-to-use",
    "user-friendly",
    "efficient",
    "highly efficient",
    "simple",
    "pleasant",
    "excellent",
    "strong",
    "secure",
    "soon",
    "large",
    "many",
    "huge",
    "smooth",
    "professional",
    "attractive",
    "intuitive",
    "reliable",
    "scalable"
]


# ==================================================
# SUGGESTIONS
# ==================================================

SUGGESTIONS = {

    "quickly":
        "Specify a maximum response or loading time, such as 2 seconds.",

    "fast":
        "Specify a measurable response time, such as within 2 seconds.",

    "very fast":
        "Define a maximum acceptable response time.",

    "easy":
        "Describe measurable usability requirements or specific user actions.",

    "easy-to-use":
        "Specify usability requirements or measurable user interaction goals.",

    "user-friendly":
        "Define specific usability requirements or user experience criteria.",

    "efficient":
        "Specify measurable performance targets such as processing time or resource usage.",

    "highly efficient":
        "Define measurable performance or resource-usage targets.",

    "simple":
        "Specify what aspects of the design or workflow should be simple.",

    "pleasant":
        "Define measurable user experience or usability criteria.",

    "excellent":
        "Replace subjective wording with measurable quality requirements.",

    "strong":
        "Specify the exact security or performance requirement.",

    "secure":
        "Define specific security requirements, controls, or standards.",

    "soon":
        "Specify an exact time limit or deadline.",

    "large":
        "Specify a measurable size, capacity, or quantity.",

    "many":
        "Specify the expected number or maximum quantity.",

    "huge":
        "Specify a measurable size, capacity, or quantity.",

    "smooth":
        "Define measurable performance or interaction criteria.",

    "professional":
        "Specify concrete design or quality requirements.",

    "attractive":
        "Define specific visual or design requirements.",

    "intuitive":
        "Specify measurable usability requirements or user actions.",

    "reliable":
        "Define an availability, failure-rate, or uptime target.",

    "scalable":
        "Specify the expected growth or maximum workload."
}


# ==================================================
# FIND VAGUE WORDS
# ==================================================

def find_vague_words(requirement):

    requirement_lower = requirement.lower()

    found_words = []


    for word in VAGUE_WORDS:

        if word in requirement_lower:

            found_words.append(
                word
            )


    return found_words


# ==================================================
# GENERATE SUGGESTIONS
# ==================================================

def generate_suggestions(vague_words):

    suggestions = []


    for word in vague_words:

        if word in SUGGESTIONS:

            suggestions.append(
                SUGGESTIONS[word]
            )


    return suggestions


# ==================================================
# FIND MISSING CONSTRAINTS
# ==================================================

def find_missing_constraints(requirement):

    requirement_lower = requirement.lower()

    missing = []


    # --------------------------------------------------
    # Upload
    # --------------------------------------------------

    if "upload" in requirement_lower:

        if (
            "mb" not in requirement_lower
            and "gb" not in requirement_lower
        ):

            missing.append(
                "Specify the maximum file size and allowed file formats."
            )


    # --------------------------------------------------
    # Storage / Retention
    # --------------------------------------------------

    if (
        "store" in requirement_lower
        or "retain" in requirement_lower
    ):

        if (
            "year" not in requirement_lower
            and "month" not in requirement_lower
        ):

            missing.append(
                "Specify what data should be stored and how long it should be retained."
            )


    # --------------------------------------------------
    # Notifications
    # --------------------------------------------------

    if (
        "notification" in requirement_lower
        or "notifications" in requirement_lower
    ):

        if (
            "within" not in requirement_lower
            and "minute" not in requirement_lower
        ):

            missing.append(
                "Specify when the notification should be sent and the delivery time requirement."
            )


    # --------------------------------------------------
    # Payment
    # --------------------------------------------------

    if "payment" in requirement_lower:

        if (
            "second" not in requirement_lower
            and "minute" not in requirement_lower
        ):

            missing.append(
                "Specify payment processing time, supported payment methods, and failure handling."
            )


    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    if "search" in requirement_lower:

        if (
            "result" not in requirement_lower
            or "page" not in requirement_lower
        ):

            missing.append(
                "Specify expected response time and the number of results returned per page."
            )


    # --------------------------------------------------
    # Backup
    # --------------------------------------------------

    if "backup" in requirement_lower:

        if (
            "hour" not in requirement_lower
            and "day" not in requirement_lower
        ):

            missing.append(
                "Specify the backup frequency and how long backups should be retained."
            )


    return missing


# ==================================================
# FIND MISSING QUANTITATIVE INFORMATION
# ==================================================

def find_missing_quantitative_info(requirement):

    requirement_lower = requirement.lower()

    missing = []


    # --------------------------------------------------
    # Performance words
    # --------------------------------------------------

    performance_words = [
        "efficient",
        "efficiently",
        "performance",
        "perform",
        "process",
        "processing"
    ]


    if any(
        word in requirement_lower
        for word in performance_words
    ):

        has_time = bool(
            re.search(
                r"\d+(?:\.\d+)?\s*"
                r"(?:ms|milliseconds?|seconds?|minutes?)",
                requirement_lower
            )
        )


        if not has_time:

            missing.append(
                "Specify a measurable performance target such as response time, processing time, or throughput."
            )


    # --------------------------------------------------
    # Handle / Support / Users
    # --------------------------------------------------

    capacity_words = [
        "handle",
        "support",
        "users",
        "customers",
        "requests",
        "transactions"
    ]


    if any(
        word in requirement_lower
        for word in capacity_words
    ):

        has_number = bool(
            re.search(
                r"\b\d+(?:\.\d+)?\b",
                requirement_lower
            )
        )


        if not has_number:

            missing.append(
                "Specify the expected capacity or maximum number of users, requests, transactions, or resources."
            )


        elif (
            "user" in requirement_lower
            or "users" in requirement_lower
        ):

            if (
                "concurrent" not in requirement_lower
                and "simultaneous" not in requirement_lower
            ):

                missing.append(
                    "Clarify whether the user count refers to total registered users or concurrent users."
                )


    # --------------------------------------------------
    # Data / Records
    # --------------------------------------------------

    data_words = [
        "data",
        "records",
        "database"
    ]


    if any(
        word in requirement_lower
        for word in data_words
    ):

        if not re.search(
            r"\b\d+(?:\.\d+)?\s*"
            r"(?:mb|gb|tb|records?|entries?)\b",
            requirement_lower
        ):

            if (
                "store" in requirement_lower
                or "retain" in requirement_lower
                or "database" in requirement_lower
            ):

                missing.append(
                    "Specify expected data volume, storage capacity, or record limits."
                )


    # --------------------------------------------------
    # File size
    # --------------------------------------------------

    if (
        "file" in requirement_lower
        or "files" in requirement_lower
    ):

        if (
            "mb" not in requirement_lower
            and "gb" not in requirement_lower
        ):

            missing.append(
                "Specify the maximum file size and supported file formats."
            )


    return missing


# ==================================================
# EXTRACT RESPONSE TIME
# ==================================================

def extract_response_time(requirement):

    requirement_lower = requirement.lower()


    # --------------------------------------------------
    # Within X seconds/minutes
    # --------------------------------------------------

    within_match = re.search(
        r"within\s+(\d+(?:\.\d+)?)\s*(second|seconds|minute|minutes)",
        requirement_lower
    )


    if within_match:

        value = float(
            within_match.group(1)
        )

        unit = within_match.group(2)


        if "minute" in unit:

            value *= 60


        return (
            "within",
            value
        )


    # --------------------------------------------------
    # At least X seconds/minutes
    # --------------------------------------------------

    at_least_match = re.search(
        r"at\s+least\s+(\d+(?:\.\d+)?)\s*(second|seconds|minute|minutes)",
        requirement_lower
    )


    if at_least_match:

        value = float(
            at_least_match.group(1)
        )

        unit = at_least_match.group(2)


        if "minute" in unit:

            value *= 60


        return (
            "at_least",
            value
        )


    # --------------------------------------------------
    # Maximum X seconds/minutes
    # --------------------------------------------------

    maximum_match = re.search(
        r"(?:maximum|max)\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*(second|seconds|minute|minutes)",
        requirement_lower
    )


    if maximum_match:

        value = float(
            maximum_match.group(1)
        )

        unit = maximum_match.group(2)


        if "minute" in unit:

            value *= 60


        return (
            "within",
            value
        )


    # --------------------------------------------------
    # Minimum X seconds/minutes
    # --------------------------------------------------

    minimum_match = re.search(
        r"(?:minimum|min)\s+(?:of\s+)?(\d+(?:\.\d+)?)\s*(second|seconds|minute|minutes)",
        requirement_lower
    )


    if minimum_match:

        value = float(
            minimum_match.group(1)
        )

        unit = minimum_match.group(2)


        if "minute" in unit:

            value *= 60


        return (
            "at_least",
            value
        )


    return None


# ==================================================
# EXTRACT CAPACITY CONSTRAINT
# ==================================================

def extract_capacity_constraint(requirement):

    requirement_lower = requirement.lower()


    # --------------------------------------------------
    # Maximum capacity
    # --------------------------------------------------

    maximum_match = re.search(
        r"(?:at\s+most|maximum|max(?:imum)?(?:\s+of)?)\s+(\d+(?:\.\d+)?)\s*"
        r"(users?|customers?|records?|files?|requests?|transactions?|items?|"
        r"products?|documents?|accounts?|connections?)",
        requirement_lower
    )


    if maximum_match:

        value = float(
            maximum_match.group(1)
        )

        unit = maximum_match.group(2)


        return (
            "maximum",
            value,
            unit
        )


    # --------------------------------------------------
    # Minimum capacity
    # --------------------------------------------------

    minimum_match = re.search(
        r"(?:at\s+least|minimum|min(?:imum)?(?:\s+of)?)\s+(\d+(?:\.\d+)?)\s*"
        r"(users?|customers?|records?|files?|requests?|transactions?|items?|"
        r"products?|documents?|accounts?|connections?)",
        requirement_lower
    )


    if minimum_match:

        value = float(
            minimum_match.group(1)
        )

        unit = minimum_match.group(2)


        return (
            "minimum",
            value,
            unit
        )


    return None


# ==================================================
# FIND CONFLICTS
# ==================================================

def find_conflicts(requirements):

    conflicts = []


    # ==================================================
    # Response-Time Conflicts
    # ==================================================

    for i in range(
        len(requirements)
    ):

        requirement_a = requirements[i]

        time_a = extract_response_time(
            requirement_a
        )


        if time_a is None:

            continue


        type_a, value_a = time_a


        for j in range(
            i + 1,
            len(requirements)
        ):

            requirement_b = requirements[j]

            time_b = extract_response_time(
                requirement_b
            )


            if time_b is None:

                continue


            type_b, value_b = time_b


            if (
                type_a == "within"
                and type_b == "at_least"
                and value_a < value_b
            ):

                conflicts.append(
                    (
                        requirement_a,
                        requirement_b,
                        "Potential response-time conflict detected: "
                        f"one requirement allows at most {value_a:g} seconds "
                        f"while the other requires waiting at least "
                        f"{value_b:g} seconds."
                    )
                )


            elif (
                type_b == "within"
                and type_a == "at_least"
                and value_b < value_a
            ):

                conflicts.append(
                    (
                        requirement_a,
                        requirement_b,
                        "Potential response-time conflict detected: "
                        f"one requirement allows at most {value_b:g} seconds "
                        f"while the other requires waiting at least "
                        f"{value_a:g} seconds."
                    )
                )


    # ==================================================
    # Capacity Conflicts
    # ==================================================

    for i in range(
        len(requirements)
    ):

        requirement_a = requirements[i]

        capacity_a = extract_capacity_constraint(
            requirement_a
        )


        if capacity_a is None:

            continue


        type_a, value_a, unit_a = capacity_a


        for j in range(
            i + 1,
            len(requirements)
        ):

            requirement_b = requirements[j]

            capacity_b = extract_capacity_constraint(
                requirement_b
            )


            if capacity_b is None:

                continue


            type_b, value_b, unit_b = capacity_b


            # --------------------------------------------------
            # Same resource only
            # --------------------------------------------------

            if unit_a.rstrip("s") != unit_b.rstrip("s"):

                continue


            # --------------------------------------------------
            # Maximum vs Minimum conflict
            # --------------------------------------------------

            if (
                type_a == "maximum"
                and type_b == "minimum"
                and value_a < value_b
            ):

                conflicts.append(
                    (
                        requirement_a,
                        requirement_b,
                        "Potential capacity conflict detected: "
                        f"one requirement allows at most {value_a:g} "
                        f"{unit_a} while the other requires at least "
                        f"{value_b:g} {unit_b}."
                    )
                )


            elif (
                type_b == "maximum"
                and type_a == "minimum"
                and value_b < value_a
            ):

                conflicts.append(
                    (
                        requirement_a,
                        requirement_b,
                        "Potential capacity conflict detected: "
                        f"one requirement allows at most {value_b:g} "
                        f"{unit_b} while the other requires at least "
                        f"{value_a:g} {unit_a}."
                    )
                )


    return conflicts

