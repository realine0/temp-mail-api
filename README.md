# Temp Mail API

Temp Mail API is a Python toolkit for temporary email workflows, disposable inbox testing, signup QA, and email-list validation. It gives automation projects a clean CLI foundation for checking temp mail addresses, detecting disposable mailboxes, and producing repeatable validation reports.

The current release focuses on the stable validation layer. The project is structured so inbox creation, inbox polling, and message-reading adapters can be added behind the same `temp-mail-api` command without changing the public interface.

## Features

- SEO-friendly `temp-mail-api` CLI entrypoint
- Built for temporary email, disposable inbox, and signup testing workflows
- Checks one email per line from a text file
- Reports status, mailbox type, disposable flag, and avatar presence
- Uses checkpoint files so large runs can resume safely
- Retries transient network failures and basic rate-limit responses
- Writes a human-readable results report
- Keeps private credentials, sessions, request captures, and generated data out of the repository

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
temp-mail-api check-list examples/emails.txt
```

Write to a custom report path:

```bash
temp-mail-api check-list examples/emails.txt --output reports/results.txt
```

Tune request behavior:

```bash
temp-mail-api check-list examples/emails.txt --timeout 15 --delay 2
```

The legacy shortcut is also available:

```bash
temp-mail-check examples/emails.txt
```

## Output

The report includes separate sections for valid emails, invalid emails, and request errors. During a run, a checkpoint file is created next to the input file, for example:

```text
examples/emails.txt.checkpoint
```

Run the same command again to continue from where the previous run stopped.

## Roadmap

- Provider adapter interface for temp mail services
- `create` command for API-key based temporary inbox creation
- `inbox` and `watch` commands for polling disposable inboxes
- JSON output for automation pipelines
- Pluggable storage for generated addresses and message history

## Responsible Use

This project is intended for legitimate testing, QA, and email-list validation. It does not include credential stuffing, CAPTCHA solving, session capture, account automation, or provider bypass logic.

## License

MIT
