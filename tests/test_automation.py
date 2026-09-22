import os

from app import automation


def test_read_requirements(tmp_path, monkeypatch):

    requirements_file = (
        tmp_path / "requirements_input.txt"
    )

    requirements_file.write_text(
        "The application must respond within 2 seconds.\n"
        "The website should be very easy to use.\n"
        "\n"
        "Users should be able to upload reports.\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        automation,
        "REQUIREMENTS_FILE",
        str(requirements_file)
    )

    requirements = (
        automation.read_requirements()
    )

    assert len(requirements) == 3

    assert requirements[0] == (
        "The application must respond within 2 seconds."
    )

    assert requirements[1] == (
        "The website should be very easy to use."
    )

    assert requirements[2] == (
        "Users should be able to upload reports."
    )


def test_generate_reports(tmp_path, monkeypatch):

    requirements_file = (
        tmp_path / "requirements_input.txt"
    )

    report_file = (
        tmp_path / "reports" / "reqlens_report.txt"
    )

    pdf_report_file = (
        tmp_path / "reports" / "reqlens_report.pdf"
    )

    log_file = (
        tmp_path / "logs" / "reqlens.log"
    )

    requirements_file.write_text(
        "The application must respond within 2 seconds.\n"
        "The website should be very easy to use.\n"
        "Users should be able to upload reports.\n",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        automation,
        "REQUIREMENTS_FILE",
        str(requirements_file)
    )

    monkeypatch.setattr(
        automation,
        "REPORT_FILE",
        str(report_file)
    )

    monkeypatch.setattr(
        automation,
        "PDF_REPORT_FILE",
        str(pdf_report_file)
    )

    monkeypatch.setattr(
        automation,
        "LOG_FILE",
        str(log_file)
    )

    automation.generate_reports()

    assert os.path.exists(
        report_file
    )

    assert os.path.exists(
        pdf_report_file
    )

    report_content = (
        report_file.read_text(
            encoding="utf-8"
        )
    )

    assert "ReqLens Report" in (
        report_content
    )

    assert "Requirement Analysis" in (
        report_content
    )

    assert (
        "Potential Conflicts"
        in report_content
    )

    assert (
        pdf_report_file.stat().st_size
        > 0
    )