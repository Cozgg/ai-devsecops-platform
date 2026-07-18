from collections import Counter

from ai_agents.models import AIReport
from findings.models import ScanFinding


MOCK_FINDINGS = [
    {
        "title": "Hardcoded secret detected",
        "severity": "HIGH",
        "description": "A secret value appears to be hardcoded in source code.",
        "file_path": "settings.py",
        "line_number": 23,
        "code_snippet": "SECRET_KEY = 'hardcoded-secret'",
    },
    {
        "title": "Debug mode enabled",
        "severity": "MEDIUM",
        "description": "Debug mode should not be enabled in production.",
        "file_path": "settings.py",
        "line_number": 12,
        "code_snippet": "DEBUG = True",
    },
]


SEVERITY_ORDER = {
    "CRITICAL": 5,
    "HIGH": 4,
    "MEDIUM": 3,
    "LOW": 2,
    "INFO": 1,
}


def get_scan_findings_payload(scan_job):
    """Return scanner findings for a scan job.

    This service supports the current MVP state: Semgrep/Trivy may not be
    integrated yet. In that case, mock findings are used so the AI report
    workflow can be developed and tested first.
    """

    findings = ScanFinding.objects.filter(scan_job=scan_job).order_by("-created_date")

    finding_data = [
        {
            "title": finding.title,
            "severity": finding.severity,
            "description": finding.description,
            "file_path": finding.file_path,
            "line_number": finding.line_number,
            "code_snippet": finding.code_snippet,
        }
        for finding in findings
    ]

    if finding_data:
        return finding_data, "scanner_findings"

    return MOCK_FINDINGS, "mock_findings"


def calculate_risk_level(findings):
    highest_score = max(
        [SEVERITY_ORDER.get(finding.get("severity", "INFO"), 1) for finding in findings],
        default=1,
    )

    if highest_score >= SEVERITY_ORDER["CRITICAL"]:
        return "CRITICAL"
    if highest_score >= SEVERITY_ORDER["HIGH"]:
        return "HIGH"
    if highest_score >= SEVERITY_ORDER["MEDIUM"]:
        return "MEDIUM"
    return "LOW"


def build_report_json(scan_job, findings, source):
    severity_count = Counter(finding.get("severity", "INFO") for finding in findings)
    risk_level = calculate_risk_level(findings)

    key_findings = [
        {
            "title": finding.get("title"),
            "severity": finding.get("severity"),
            "file_path": finding.get("file_path"),
            "line_number": finding.get("line_number"),
            "impact": finding.get("description") or "Finding cần được kiểm tra thêm.",
            "recommendation": "Kiểm tra đoạn code liên quan và ưu tiên xử lý theo severity.",
        }
        for finding in findings
    ]

    summary = (
        "Hệ thống đã tạo báo cáo phân tích bảo mật cho scan job. "
        f"Mức rủi ro tổng quan hiện tại là {risk_level}."
    )

    if source == "mock_findings":
        summary += " Báo cáo hiện đang dùng dữ liệu findings mẫu vì scanner chưa sinh findings thật."

    risk_overview = (
        "Số lượng findings theo mức độ: "
        f"CRITICAL={severity_count.get('CRITICAL', 0)}, "
        f"HIGH={severity_count.get('HIGH', 0)}, "
        f"MEDIUM={severity_count.get('MEDIUM', 0)}, "
        f"LOW={severity_count.get('LOW', 0)}, "
        f"INFO={severity_count.get('INFO', 0)}."
    )

    recommendation = (
        "Ưu tiên xử lý các findings mức CRITICAL/HIGH trước, sau đó chạy lại scan "
        "để xác nhận rủi ro đã được khắc phục."
    )

    return {
        "summary": summary,
        "risk_overview": risk_overview,
        "recommendation": recommendation,
        "risk_level": risk_level,
        "source": source,
        "scan_job": {
            "id": scan_job.id,
            "scan_type": scan_job.scan_type,
            "status": scan_job.status,
            "metadata": scan_job.metadata,
        },
        "severity_count": dict(severity_count),
        "total_findings": len(findings),
        "key_findings": key_findings,
        "priority_actions": [
            "Xử lý findings mức CRITICAL/HIGH trước.",
            "Không đưa secret trực tiếp vào source code.",
            "Kiểm tra cấu hình debug, CORS, authentication và dependency.",
            "Chạy lại scan sau khi sửa lỗi.",
        ],
    }


def generate_ai_report(scan_job):
    """Generate and persist an AIReport for a scan job.

    For now this function builds a deterministic report from findings/mock
    findings. Replace build_report_json with a real AI API call after the API
    key and provider are finalized.
    """

    findings, source = get_scan_findings_payload(scan_job)
    report_json = build_report_json(scan_job, findings, source)

    ai_report, _ = AIReport.objects.update_or_create(
        scan_job=scan_job,
        defaults={
            "summary": report_json["summary"],
            "risk_overview": report_json["risk_overview"],
            "recommendation": report_json["recommendation"],
            "report_json": report_json,
            "model_name": "mock-ai-report-service",
        },
    )

    metadata = dict(scan_job.metadata or {})
    metadata["ai_report"] = {
        "generated": True,
        "source": source,
        "risk_level": report_json["risk_level"],
        "total_findings": report_json["total_findings"],
    }
    scan_job.metadata = metadata
    scan_job.save(update_fields=("metadata", "updated_date"))

    return ai_report
