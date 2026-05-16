"""Client for checking email status through public Sonjj/YChecker endpoints."""

from __future__ import annotations

import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass(frozen=True)
class EmailCheckResult:
    email: str
    status: str
    email_type: str = "Unknown"
    disposable: str = "Unknown"
    avatar: bool = False
    error: str | None = None

    @property
    def is_valid(self) -> bool:
        return self.status == "Ok"


class EmailChecker:
    """Validate email addresses with checkpoint support for large lists."""

    def __init__(self, timeout: int = 10, delay: float = 1.5) -> None:
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (compatible; temp-mail-api/1.0)",
                "Accept": "application/json",
            }
        )

    def check_email(self, email: str, retry: int = 3) -> EmailCheckResult:
        for attempt in range(retry):
            try:
                encoded_email = urllib.parse.quote(email)
                payload_url = (
                    "https://ychecker.com/app/payload"
                    f"?email={encoded_email}&use_credit_first=0"
                )
                payload_response = self.session.get(payload_url, timeout=self.timeout)
                payload_response.raise_for_status()
                payload_data = payload_response.json()

                if payload_data.get("code") != 200:
                    message = payload_data.get("msg", "Could not create payload")
                    if self._should_retry(message, attempt, retry):
                        continue
                    return EmailCheckResult(email=email, status="ERROR", error=message)

                token = payload_data["items"]
                time.sleep(1)

                check_url = f"https://api.sonjj.com/v1/check_email/?payload={token}"
                check_response = self.session.get(check_url, timeout=self.timeout)
                check_response.raise_for_status()
                check_data = check_response.json()

                return EmailCheckResult(
                    email=email,
                    status=check_data.get("status", "Unknown"),
                    email_type=check_data.get("type", "Unknown"),
                    disposable=check_data.get("disposable", "Unknown"),
                    avatar=bool(check_data.get("avatar")),
                )

            except (requests.RequestException, ValueError, KeyError) as exc:
                if attempt < retry - 1:
                    time.sleep(2 + attempt)
                    continue
                return EmailCheckResult(email=email, status="ERROR", error=str(exc))

        return EmailCheckResult(email=email, status="ERROR", error="All retry attempts failed")

    def check_file(self, input_file: Path, output_file: Path) -> list[EmailCheckResult]:
        checkpoint_file = input_file.with_suffix(input_file.suffix + ".checkpoint")
        checked = self.load_checkpoint(checkpoint_file)
        emails = self.load_emails(input_file)
        remaining = [email for email in emails if email not in checked]

        print(f"Total emails: {len(emails)}")
        print(f"Already checked: {len(checked)}")
        print(f"Remaining: {len(remaining)}")

        results: list[EmailCheckResult] = []
        for index, email in enumerate(remaining, start=1):
            print(f"[{index}/{len(remaining)}] {email} ... ", end="", flush=True)
            result = self.check_email(email)
            results.append(result)
            self.save_checkpoint(checkpoint_file, result)

            if result.is_valid:
                print(f"valid ({result.email_type})")
            elif result.error:
                print(f"error: {result.error}")
            else:
                print(f"invalid ({result.status})")

            if index < len(remaining):
                time.sleep(self.delay)

        self.save_results(results, output_file)
        return results

    @staticmethod
    def load_emails(input_file: Path) -> list[str]:
        return [
            line.strip()
            for line in input_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and "@" in line
        ]

    @staticmethod
    def load_checkpoint(checkpoint_file: Path) -> dict[str, str]:
        if not checkpoint_file.exists():
            return {}

        checked: dict[str, str] = {}
        for line in checkpoint_file.read_text(encoding="utf-8").splitlines():
            parts = line.split("|", maxsplit=1)
            if len(parts) == 2:
                checked[parts[0]] = parts[1]
        return checked

    @staticmethod
    def save_checkpoint(checkpoint_file: Path, result: EmailCheckResult) -> None:
        with checkpoint_file.open("a", encoding="utf-8") as file:
            file.write(f"{result.email}|{result.status}\n")

    @staticmethod
    def save_results(results: list[EmailCheckResult], output_file: Path) -> None:
        valid = [result for result in results if result.is_valid]
        invalid = [result for result in results if not result.is_valid and not result.error]
        errors = [result for result in results if result.error]

        lines = [
            "EMAIL CHECK RESULTS",
            "=" * 80,
            "",
            "VALID EMAILS",
            "-" * 80,
        ]

        if valid:
            for result in valid:
                lines.extend(
                    [
                        result.email,
                        f"  Type: {result.email_type}",
                        f"  Disposable: {result.disposable}",
                        f"  Avatar: {'Yes' if result.avatar else 'No'}",
                        "",
                    ]
                )
        else:
            lines.extend(["No valid emails found.", ""])

        lines.extend(["INVALID EMAILS", "-" * 80])
        if invalid:
            lines.extend(f"{result.email} - Status: {result.status}" for result in invalid)
        else:
            lines.append("No invalid emails found.")

        if errors:
            lines.extend(["", "ERRORS", "-" * 80])
            lines.extend(f"{result.email} - Error: {result.error}" for result in errors)

        output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def _should_retry(message: str, attempt: int, retry: int) -> bool:
        if attempt >= retry - 1:
            return False

        if "rate" in message.lower() or "limit" in message.lower():
            time.sleep((attempt + 1) * 5)
            return True

        return False
