# Contributing to TeleBot Studio MCP

Thank you for helping improve TeleBot Studio MCP! Whether you are fixing a bug, adding a REST API tool, refreshing official documentation, or contributing a reusable TBS implementation pattern, this guide covers everything you need.

## How to Contribute

1. Fork the repository (`https://github.com/harshi79/telebotstudio-mcp`)
2. Create a feature branch from `main`: `git checkout -b feature/my-change`
3. Make your changes and add/update unit tests
4. Run validation, lint, type checks, and tests locally
5. Open a Pull Request against `main`

## Development Setup

Python **3.11+** is required.

```bash
git clone https://github.com/harshi79/telebotstudio-mcp.git
cd telebotstudio-mcp
python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Verification Suite

Run all checks locally before opening a Pull Request (matching `.github/workflows/ci.yml`):

```bash
# 1. Validate documentation corpus & BM25 index (must pass with zero issues)
python build_index.py --validate

# 2. Run Ruff linter
ruff check .

# 3. Run MyPy static type checker
python -m mypy server.py loader.py search.py api/ agent/ tools/ --ignore-missing-imports

# 4. Run full Pytest suite (offline, mocked HTTP — no live credentials required)
python -m pytest tests/ -v --tb=short
```

## Contributing Documentation & Patterns

### Refreshing Official TeleBot Studio Docs

```bash
python crawler.py                   # Crawls help.telebotstudio.com -> urls.txt
python download_docs.py             # Downloads & sanitizes clean .md files into docs/
python build_index.py --validate    # Verifies every chunk cleanly
```

Note: `download_docs.py` strips GitBook escape artifacts (`\*`, `\_`) and boilerplate `?ask=` footers automatically. Always review diffs in `docs/readme.md` so live-verified API v2 endpoints (`POST /v2/bots/{botid}/command/by-name` and `GET /v2/bots/{botid}/commands/list`) remain intact.

### Adding an Implementation Pattern (`docs/patterns/`)

1. Copy [`docs/patterns/TEMPLATE.md`](docs/patterns/TEMPLATE.md) into the appropriate category folder (`ui/`, `admin/`, `systems/`, `commerce/`, `storage/`, `integrations/`, or `utilities/`)
2. Name the file using lowercase kebab-case (e.g., `inline-keyboard-menu.md`)
3. Provide complete, runnable TBS code — never placeholders or pseudocode
4. Keep `verified: false` until tested against a live TeleBot Studio bot (and record the bot/environment under `tested_with`)
5. Add the new pattern to both the category `README.md` and [`docs/patterns/README.md`](docs/patterns/README.md)
6. Run `python build_index.py --validate` and `pytest tests/`

## Code Style & Architecture Conventions

- Start every Python module with `from __future__ import annotations`
- **Type hints** required on all public function/method signatures
- **Docstrings** required on all public modules, classes, and MCP tool functions
- Never persist credentials to disk or log raw API keys / bot tokens (`api/utils.py` provides `mask_credential` and `mask_value`)
- Destructive MCP tools **must** default to `confirm: bool = False` and return a preview when `confirm=False`
- All API wrappers obtain clients via `TeleBotStudioClient.from_pool(api_key=...)`
- Never perform real network calls inside `tests/` — mock `httpx` / `TeleBotStudioClient` responses cleanly

## Pull Request Requirements

- All `pytest`, `ruff check .`, `mypy`, and `build_index.py --validate` checks pass
- No breaking tool signature changes without prior discussion in a GitHub Issue
- Focused scope (one feature or fix per PR) with clear description
- Unit tests included for new behavior or bug fixes

## Bug Reports & Feature Requests

Use the GitHub Issue templates (`.github/ISSUE_TEMPLATE/`). Include steps to reproduce, Python version, OS, MCP client, and sanitized logs (never include raw tokens or API keys).
