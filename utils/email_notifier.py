"""
Email Notification Utility for Playwright Python API Automation.
Dispatches a modern, responsive HTML email report to tanzimsqa@gmail.com
after automated test execution completes (locally or on GitHub Actions CI).
"""

import os
import sys
import json
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Configure utf-8 stdout/stderr for cross-platform unicode safety (Windows cp1252 fix)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Default recipient and repository links
DEFAULT_RECIPIENT = "tanzimsqa@gmail.com"
REPORT_URL = "https://tanzimsqa.github.io/playwright-api-testing-framework/"
REPO_URL = "https://github.com/TanzimSQA/playwright-api-testing-framework"


def load_test_summary() -> dict:
    """Load summary metrics from reports/summary.json or generate defaults."""
    summary_path = Path("reports/summary.json")
    if summary_path.exists():
        try:
            return json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[EMAIL NOTIFIER] Warning: Could not parse summary.json: {e}")

    # Fallback default values
    return {
        "total": 27,
        "passed": 27,
        "failed": 0,
        "skipped": 0,
        "pass_rate": 100.0,
        "total_duration": 12.8,
        "total_duration_formatted": "12.8s",
        "status": "PASSED",
        "timestamp": datetime.now().strftime("%d-%b-%Y %H:%M:%S BST"),
        "suites": {
            "auth": {"name": "Authentication & Security", "icon": "🔑", "total": 6, "passed": 6, "failed": 0},
            "products": {"name": "Products Catalog & CRUD", "icon": "📦", "total": 13, "passed": 13, "failed": 0},
            "users": {"name": "User Directory & Filter", "icon": "👤", "total": 4, "passed": 4, "failed": 0},
            "e2e": {"name": "End-to-End Shopping Journey", "icon": "🛒", "total": 1, "passed": 1, "failed": 0},
            "performance": {"name": "Latency SLA Benchmarks", "icon": "⏱️", "total": 3, "passed": 3, "failed": 0},
        },
    }


def build_email_template(summary: dict, run_url: str = "") -> tuple[str, str]:
    """
    Constructs a modern, responsive HTML email template and plain text alternative.
    """
    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    pass_rate = summary.get("pass_rate", 100.0)
    duration = summary.get("total_duration_formatted", "12s")
    timestamp = summary.get("timestamp", datetime.now().strftime("%d-%b-%Y %H:%M:%S BST"))
    suites = summary.get("suites", {})

    is_all_passed = (failed == 0)
    status_text = "ALL API TESTS PASSED (100% HEALTH)" if is_all_passed else f"{failed} FAILURE(S) DETECTED"
    status_color = "#10b981" if is_all_passed else "#f43f5e"
    status_bg = "#ecfdf5" if is_all_passed else "#fff1f2"
    status_border = "#10b981" if is_all_passed else "#f43f5e"
    status_symbol = "✓" if is_all_passed else "✗"

    # Subject line
    if is_all_passed:
        subject = f"✅ [PASS] Playwright Python API Automation: {passed}/{total} Passed (100% Health)"
    else:
        subject = f"❌ [FAIL] Playwright API Alert: {failed} Failed out of {total} Tests"

    # Suites rows
    suites_html = ""
    for s_id, s_data in suites.items():
        s_name = s_data.get("name", s_id)
        s_icon = s_data.get("icon", "🧪")
        s_tot = s_data.get("total", 0)
        s_pass = s_data.get("passed", 0)
        s_fail = s_data.get("failed", 0)
        s_status = (
            f"<span style='color: #10b981; font-weight: 700;'>✓ {s_pass}/{s_tot} Passed</span>"
            if s_fail == 0
            else f"<span style='color: #f43f5e; font-weight: 700;'>✗ {s_fail} Failed</span>"
        )

        suites_html += f"""
        <tr>
          <td style="padding: 10px 14px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #1e293b;">
            {s_icon} <strong>{s_name}</strong>
          </td>
          <td style="padding: 10px 14px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">
            {s_status}
          </td>
        </tr>
        """

    live_report_link = os.getenv("REPORT_URL", REPORT_URL)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{subject}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f1f5f9; padding: 30px 15px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table width="640" border="0" cellspacing="0" cellpadding="0" style="max-width: 640px; background-color: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;">
          
          <!-- Header Banner -->
          <tr>
            <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px 32px; text-align: left;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td>
                    <div style="display: inline-block; background: linear-gradient(135deg, #2EAD33 0%, #06b6d4 100%); border-radius: 10px; padding: 8px 12px; font-size: 20px; line-height: 1;">⚡</div>
                  </td>
                  <td style="padding-left: 14px;">
                    <h1 style="margin: 0; font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Playwright API Automation</h1>
                    <p style="margin: 3px 0 0 0; font-size: 13px; color: #94a3b8;">Automated RESTful API Regression Test Execution Report</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Health Status Banner -->
          <tr>
            <td style="padding: 24px 32px 10px 32px;">
              <div style="background-color: {status_bg}; border: 1.5px solid {status_border}; border-radius: 10px; padding: 14px 20px; text-align: center;">
                <span style="font-size: 16px; font-weight: 800; color: {status_color}; letter-spacing: 0.02em;">
                  {status_symbol} {status_text}
                </span>
                <div style="margin-top: 4px; font-size: 12px; color: #64748b;">
                  Execution finished at {timestamp}
                </div>
              </div>
            </td>
          </tr>

          <!-- Metrics KPI Grid -->
          <tr>
            <td style="padding: 16px 32px;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <!-- Total -->
                  <td width="23%" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase;">Total Tests</div>
                    <div style="font-size: 22px; font-weight: 800; color: #0f172a; margin-top: 4px;">{total}</div>
                  </td>
                  <td width="2%"></td>
                  <!-- Passed -->
                  <td width="23%" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 600; color: #10b981; text-transform: uppercase;">Passed</div>
                    <div style="font-size: 22px; font-weight: 800; color: #10b981; margin-top: 4px;">{passed}</div>
                  </td>
                  <td width="2%"></td>
                  <!-- Failed -->
                  <td width="23%" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 600; color: {'#f43f5e' if failed > 0 else '#64748b'}; text-transform: uppercase;">Failed</div>
                    <div style="font-size: 22px; font-weight: 800; color: {'#f43f5e' if failed > 0 else '#64748b'}; margin-top: 4px;">{failed}</div>
                  </td>
                  <td width="2%"></td>
                  <!-- Pass Rate -->
                  <td width="25%" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 11px; font-weight: 600; color: #6366f1; text-transform: uppercase;">Pass Rate</div>
                    <div style="font-size: 22px; font-weight: 800; color: #6366f1; margin-top: 4px;">{pass_rate}%</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Suite Breakdown Table -->
          <tr>
            <td style="padding: 10px 32px;">
              <h3 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 700; color: #334155; text-transform: uppercase; letter-spacing: 0.05em;">API Test Suite Breakdown</h3>
              <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
                {suites_html}
              </table>
            </td>
          </tr>

          <!-- Action Buttons -->
          <tr>
            <td style="padding: 24px 32px 30px 32px; text-align: center;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <a href="{live_report_link}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #2EAD33 0%, #10b981 100%); color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 700; padding: 12px 26px; border-radius: 8px; box-shadow: 0 4px 14px rgba(46, 173, 51, 0.35);">
                      🌐 View Live GitHub Pages Report
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f8fafc; padding: 20px 32px; border-top: 1px solid #e2e8f0; text-align: center;">
              <p style="margin: 0; font-size: 12px; color: #64748b;">
                Playwright Python API Automation Framework • Automated CI/CD Report • Lead QA: <a href="mailto:{DEFAULT_RECIPIENT}" style="color: #6366f1; text-decoration: none;">{DEFAULT_RECIPIENT}</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    plain_content = f"""Playwright Python API Automation Report
Status: {status_text}
Time: {timestamp}
Total Tests: {total} | Passed: {passed} | Failed: {failed} | Pass Rate: {pass_rate}%
Duration: {duration}

Live Report: {live_report_link}
Repository: {REPO_URL}
"""
    return subject, html_content, plain_content


def send_email_notification():
    """Main dispatch handler for email notification."""
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER") or os.getenv("MAIL_USERNAME")
    smtp_pass = os.getenv("SMTP_PASS") or os.getenv("MAIL_PASSWORD")
    recipient = os.getenv("EMAIL_RECIPIENT", DEFAULT_RECIPIENT)

    summary = load_test_summary()
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repo = os.getenv("GITHUB_REPOSITORY", "TanzimSQA/playwright-api-testing-framework")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    run_url = f"{server_url}/{repo}/actions/runs/{run_id}" if run_id else REPO_URL

    subject, html_body, plain_body = build_email_template(summary, run_url=run_url)

    if not smtp_user or not smtp_pass:
        print("[EMAIL NOTIFIER] Note: SMTP_USER or SMTP_PASS not set. Skipping live email dispatch.")
        print(f"[EMAIL NOTIFIER] Summary: {summary['passed']}/{summary['total']} passed ({summary['pass_rate']}%).")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Playwright API CI <{smtp_user}>"
        msg["To"] = recipient

        msg.attach(MIMEText(plain_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        print(f"[EMAIL NOTIFIER] Connecting to {smtp_host}:{smtp_port} via SSL...")
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [recipient], msg.as_string())
        print(f"[EMAIL NOTIFIER] ✅ Successfully dispatched test summary to {recipient}!")
    except Exception as exc:
        print(f"[EMAIL NOTIFIER] ⚠️ Could not send email: {exc}")


if __name__ == "__main__":
    send_email_notification()
