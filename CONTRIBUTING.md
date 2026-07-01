# Contributing to TeleBot Studio MCP

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-change`
3. Make your changes
4. Submit a pull request

## Development Setup

```bash
git clone https://github.com/telebotstudio/telebotstudio-mcp.git
cd telebotstudio-mcp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build_index.py --validate
```

## Code Style

- Follow the existing code style
- **Type hints required** on all function signatures
- **Docstrings required** for all public functions and classes
- Use `ruff` for linting if available
- Keep functions focused and small

## Pull Request Requirements

- All existing tests must pass
- No breaking changes without prior discussion in an issue
- One feature or fix per PR
- Include a clear description of the change
- Add tests for new functionality when applicable

## Bug Reports

Use the GitHub issue template. Include:

- Steps to reproduce
- Expected vs actual behavior
- Python version, OS, and MCP client
- Relevant logs

## Questions

Open a GitHub Discussion for questions or ideas that are not bug reports.
