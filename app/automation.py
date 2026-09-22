import os
import time
import logging

from config import (
    REQUIREMENTS_FILE,
    REPORT_FILE,
    PDF_REPORT_FILE,
    LOG_FILE,
    AUTOMATION_INTERVAL
)

from reqlens import (
    analyze_requirements,
    create_report
)

from report_generator import generate_pdf_report


# ==================================================
# LOGGING SETUP
# ==================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==================================================
# READ REQUIREMENTS
# ==================================================

def read_requirements():
    if not os.path.exists(REQUIREMENTS_FILE):
        return []

    with open(
        REQUIREMENTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    requirements = []

    for line in lines:
        line = line.strip()

        if line:
            requirements.append(line)

    return requirements


# ==================================================
# GENERATE REPORTS
# ==================================================

def generate_reports():
    requirements = read_requirements()

    if not requirements:
        print("No requirements found.")
        logging.warning(
            "No requirements found in input file."
        )
        return

    print(
        f"\nAnalyzing {len(requirements)} requirement(s)..."
    )

    analyses, conflicts = analyze_requirements(
        requirements
    )

    # ----------------------------------------------
    # TEXT REPORT
    # ----------------------------------------------

    report = create_report(
        requirements,
        analyses,
        conflicts
    )

    report_directory = os.path.dirname(
        REPORT_FILE
    )

    if report_directory:
        os.makedirs(
            report_directory,
            exist_ok=True
        )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print(
        f"Text report generated: {REPORT_FILE}"
    )

    # ----------------------------------------------
    # PDF REPORT
    # ----------------------------------------------

    pdf_report = generate_pdf_report(
        requirements,
        analyses,
        conflicts
    )

    pdf_directory = os.path.dirname(
        PDF_REPORT_FILE
    )

    if pdf_directory:
        os.makedirs(
            pdf_directory,
            exist_ok=True
        )

    with open(
        PDF_REPORT_FILE,
        "wb"
    ) as file:

        file.write(pdf_report)

    print(
        f"PDF report generated: {PDF_REPORT_FILE}"
    )

    logging.info(
        "ReqLens analyzed %d requirement(s).",
        len(requirements)
    )

    logging.info(
        "Text report generated: %s",
        REPORT_FILE
    )

    logging.info(
        "PDF report generated: %s",
        PDF_REPORT_FILE
    )

    if conflicts:
        logging.warning(
            "%d potential conflict(s) detected.",
            len(conflicts)
        )

    print(
        "\nReqLens automation completed successfully."
    )


# ==================================================
# FILE MONITORING
# ==================================================

def monitor_requirements():

    print("\n" + "=" * 60)
    print("                 ReqLens")
    print("          Automation Monitor")
    print("=" * 60)

    print(
        f"\nMonitoring: {REQUIREMENTS_FILE}"
    )

    print(
        f"Check interval: {AUTOMATION_INTERVAL} seconds"
    )

    print(
        "\nWaiting for requirement changes..."
    )

    logging.info(
        "ReqLens automation started."
    )

    last_modified_time = None

    while True:

        try:

            if os.path.exists(
                REQUIREMENTS_FILE
            ):

                modified_time = os.path.getmtime(
                    REQUIREMENTS_FILE
                )

                if (
                    last_modified_time is None
                    or modified_time != last_modified_time
                ):

                    print(
                        "\nRequirement file changed."
                    )

                    logging.info(
                        "Requirement file changed."
                    )

                    generate_reports()

                    last_modified_time = (
                        modified_time
                    )

            time.sleep(
                AUTOMATION_INTERVAL
            )

        except KeyboardInterrupt:

            print(
                "\n\nReqLens automation stopped."
            )

            logging.info(
                "ReqLens automation stopped."
            )

            break

        except Exception as error:

            print(
                "\nAutomation error:",
                error
            )

            logging.exception(
                "Automation error occurred."
            )

            time.sleep(
                AUTOMATION_INTERVAL
            )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    monitor_requirements()