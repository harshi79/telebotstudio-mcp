<div align="center">

# TeleBot Studio MCP

**Eliminate AI hallucinations. Let your assistant read official docs AND manage your bots.**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-1.0_Compatible-8A2BE2?style=flat-square&logo=modelcontextprotocol&logoColor=white)](https://modelcontextprotocol.io)
[![Powered by FastMCP](https://img.shields.io/badge/Powered%20by-FastMCP-005A9C?style=flat-square)](https://github.com/jlowin/fastmcp)
[![26 MCP Tools](https://img.shields.io/badge/Tools-26-FF6F00?style=flat-square)]()
[![No OpenAI Required](https://img.shields.io/badge/API-OpenAI_Not_Required-00c7b7?style=flat-square)]()

*A production-ready Model Context Protocol (MCP) server with two superpowers:*
1. **Documentation Search** — BM25-ranked search across official TeleBot Studio docs. Zero embeddings. Zero external APIs. 100% offline.
2. **Bot Management** — Full REST API integration to create, configure, and control TeleBot Studio bots directly from your AI assistant.

[Quick Start](#-quick-start) · [Documentation Tools](#-documentation-search-tools-8) · [API Tools](#-bot-management-tools-18) · [Architecture](#-architecture--how-it-works) · [Deployment](#-deployment)

</div>

---

## Why This Exists

Large Language Models are powerful, but they hallucinate API specifics. When you ask an LLM how to use TeleBot Studio, it guesses based on outdated training data. This causes **documentation drift** — the gap between what the AI says and what the official docs specify.

**TeleBot Studio MCP** solves this two ways:
- **Documentation tools** ground your AI in official docs. If the answer isn't there, the server returns nothing. No more phantom functions.
- **API tools** let your AI *do things* — create bots, write commands, start/stop them — through the official TeleBot Studio REST API v2.

---

## ✨ Features

| Category | Capabilities |
| :--- | :--- |
| **📄 Documentation** | BM25 search engine, Heading-aware chunking, Unigram + bigram tokenization, LRU caching, 100% offline search. |
| **🤖 Bot Management** | Create/delete/update bots, Create/update/delete/list commands, Start/stop/restart bots, Batch operations, Agent pipeline. |
| **🔒 Security** | Session-scoped credentials (never persisted), Token masking in logs/responses, Preview & confirmation for destructive ops. |
| **⚡ Server** | Built on FastMCP, STDIO + HTTP/Streamable HTTP, `/health` endpoint for uptime monitoring, Thread-safe credential manager. |
| **🏗️ Architecture** | Production-ready, Zero cold-start, Input validation, Structured JSON responses, Retry with exponential backoff. |

---

## 🛠️ MCP Tools (26 Total)

### Documentation Search Tools (8)

| Tool | Description |
| :--- | :--- |
| `search_docs(query, top_k)` | Primary search. Full-text BM25 across all chunks. |
| `get_page(name)` | Retrieve an entire documentation page by filename. |
| `list_pages()` | List all available documentation pages. |
| `search_examples(query, top_k)` | Scoped search for code examples and snippets. |
| `search_api(query, top_k)` | Scoped search for API references and endpoints. |
| `search_library(query, top_k)` | Scoped search for library/install info. |
| `search_functions(query, top_k)` | Scoped search for function definitions and signatures. |
| `search_errors(query, top_k)` | Scoped search for errors and troubleshooting. |

### Bot Management Tools (18)

#### Credential Tools (3)
| Tool | Description |
| :--- | :--- |
| `tbs_set_api_key(api_key)` | Set your TeleBot Studio API key (memory-only, never persisted). |
| `tbs_set_bot_id(bot_id)` | Set the active Bot ID for the session. |
| `tbs_credential_status()` | Check if credentials are set (key is masked). |

#### Bot Management (3)
| Tool | Description |
| :--- | :--- |
| `tbs_create_bot(bot_token)` | Create a new bot with a Telegram bot token. Auto-sets the bot ID. |
| `tbs_delete_bot(bot_id, confirm)` | Soft-delete a bot. **Preview supported** — set `confirm=true` to execute. |
| `tbs_update_bot_token(bot_id, new_token, confirm)` | Update a bot's token (bot restarts). **Preview supported.** |

#### Command Management (5)
| Tool | Description |
| :--- | :--- |
| `tbs_create_command(command, code, bot_id)` | Create a new command on a bot. |
| `tbs_get_command(command_name, bot_id)` | Get command details by name. |
| `tbs_update_command(command_name, code, bot_id, confirm)` | Update a command's code. **Preview supported.** |
| `tbs_delete_command(command_name, bot_id, confirm)` | Delete a command. **Preview supported.** |
| `tbs_list_commands(bot_id)` | List all commands for a bot. |

#### Bot Control (3)
| Tool | Description |
| :--- | :--- |
| `tbs_start_bot(bot_id)` | Start a bot (set webhook). |
| `tbs_stop_bot(bot_id)` | Stop a bot (remove webhook). |
| `tbs_restart_bot(bot_id)` | Restart a bot (stop + start). |

#### Agent Tools (2)
| Tool | Description |
| :--- | :--- |
| `tbs_deploy_bot(bot_token, commands_json, confirm)` | Complete deployment: create bot → add commands → start. |
| `tbs_setup_commands(commands_json, bot_id, confirm)` | Bulk create commands on an existing bot. |

#### Batch Tools (2)
| Tool | Description |
| :--- | :--- |
| `tbs_batch_create_commands(commands_json, bot_id, confirm)` | Create multiple commands in sequence. |
| `tbs_batch_delete_commands(command_names_json, bot_id, confirm)` | Delete multiple commands in sequence. **Preview supported.** |

---

## 🚀 Quick Start

### Prerequisites
* Python 3.9+
* `pip` package manager
* A [TeleBot Studio](https://telebotstudio.com) account (for API tools)

### 1. Clone & Install
```bash
git clone https://github.com/harshi79/telebotstudio-mcp.git
cd telebotstudio-mcp
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Verify
```bash
python build_index.py --validate
```

### 3. Run
```bash
# STDIO mode (Claude Desktop, Cursor, etc.)
python server.py

# HTTP mode (remote clients, web dashboards)
python server.py --transport http
```

### 4. Use API Tools
In your MCP client, call tools in this order:
1. `tbs_set_api_key` — authenticate with your TeleBot Studio API key
2. `tbs_set_bot_id` — select which bot to operate on (or let `tbs_create_bot` auto-set it)
3. Call any management tool (e.g., `tbs_create_command`, `tbs_start_bot`)

---

## ⚙️ Configuration

### Transport Modes

**STDIO** (default — for Claude Desktop, Cursor, Windsurf):
```bash
python server.py
```

**HTTP / Streamable HTTP** (for remote clients):
```bash
python server.py --transport http --host 0.0.0.0 --port 9000
```

**Environment Variables:**
- `TBS_DOCS_DIR`: Override the default docs directory
- `HOST`: Default host for HTTP mode (default: `0.0.0.0`)
- `PORT`: Default port for HTTP mode (default: `8000`)

### Claude Desktop
Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "telebotstudio": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/telebotstudio-mcp/server.py"]
    }
  }
}
```

### Cursor / Windsurf / Cline / Continue
Set the command to `python` and the argument to the absolute path of `server.py`. Select **STDIO** transport.

---

## 🏗️ Architecture & How It Works

### Two-Engine Design
```
┌─────────────────────────────────────────────────┐
│                 FastMCP Server                    │
│                                                   │
│  ┌──────────────────┐  ┌───────────────────────┐ │
│  │  Documentation    │  │  Bot Management       │ │
│  │  Engine (BM25)    │  │  Engine (REST API)    │ │
│  │                   │  │                       │ │
│  │  8 search tools   │  │  Planner → Validator  │ │
│  │  100% offline     │  │  → Preview → Executor │ │
│  │  In-memory index  │  │  18 API tools         │ │
│  └──────────────────┘  └───────────────────────┘ │
│                                                   │
│  ┌──────────────────────────────────────────────┐ │
│  │  Session Manager (thread-safe, memory-only)  │ │
│  └──────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
         │                           │
    STDIO / HTTP              HTTPS to api.telebotstudio.com
```

### Agent Pipeline (for deploy_bot, setup_commands, batch operations)
```
User Goal → Planner (decompose into steps)
          → Validator (check credentials, params)
          → Preview (show what will happen, mask secrets)
          → [confirm=true] → Executor (run steps sequentially)
                           → BatchResult (per-step success/failure)
```

### Preview & Confirmation
Destructive operations (delete bot, delete command, update token) require `confirm=true`. When `confirm=false` (default), the tool returns a preview describing what *will* happen without executing anything. This two-step pattern prevents accidental data loss.

---

## 📁 Project Structure

```
telebotstudio-mcp/
├── server.py            # Entry point — FastMCP server, doc tools, /health
├── loader.py            # Markdown loader & heading-aware chunking
├── search.py            # BM25 index builder & search engine
├── api/
│   ├── __init__.py      # Public API exports
│   ├── auth.py          # Input validation (API key, bot token, command names)
│   ├── client.py        # HTTP client with retry, timeout, error mapping
│   ├── errors.py        # Typed exception hierarchy
│   ├── models.py        # Request/response dataclasses
│   ├── session.py       # Thread-safe credential manager
│   ├── bots.py          # Bot management wrapper
│   ├── commands.py      # Command management wrapper
│   └── bot_control.py   # Start/stop/restart wrapper
├── agent/
│   ├── __init__.py      # Agent layer exports
│   ├── planner.py       # Decompose goals into execution plans
│   ├── validator.py     # Validate plans against session state
│   ├── preview.py       # Generate human-readable plan previews
│   └── executor.py      # Execute plans with rate-limit awareness
├── tools/
│   ├── __init__.py      # Tools package
│   └── api_tools.py     # 18 MCP tool definitions
├── docs/                # Official TeleBot Studio documentation (.md)
├── build_index.py       # CLI diagnostic tool
├── Dockerfile           # Container definition
├── .dockerignore        # Docker build exclusions
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
└── README.md            # This file
```

---

## 🚢 Deployment

### Docker
```bash
docker build -t telebotstudio-mcp .
docker run -p 8000:8000 telebotstudio-mcp
```
The MCP endpoint is at `http://localhost:8000/mcp` and the health check at `http://localhost:8000/health`.

### Render.com
1. Create a new **Web Service** on Render.
2. Connect your GitHub repository.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python server.py --transport http`
5. Render auto-assigns the `PORT` environment variable.

### Health Check
The `/health` endpoint returns `{"status": "ok"}` and is suitable for uptime monitoring (UptimeRobot, Render health checks, etc.). This endpoint is outside the MCP protocol and does not require authentication.

---

## 🛡️ Security & Privacy

* 🔒 **No Telemetry:** Zero analytics, tracking, or phone-home.
* 🧠 **Credentials in Memory Only:** API keys and bot tokens are stored in memory and lost on restart. Never persisted to disk, never logged in cleartext.
* 🛡️ **Token Masking:** Bot tokens and API keys are masked in all log messages and preview responses (`tbs_1...xyz`).
* ✅ **Preview Before Destructive:** Delete and update operations require explicit `confirm=true`. Default is preview-only.
* 🧹 **Input Validation:** All inputs are validated before API calls (token format, bot ID format, command name length, etc.).
* 🔐 **Thread-Safe Sessions:** Credential manager uses thread-local storage and locks for HTTP transport safety.
* 📴 **Offline Docs:** Documentation search works 100% offline — no internet required. API tools require internet to reach `api.telebotstudio.com`.

---

## 🧐 Design Decisions

<details>
<summary><b>Why BM25 instead of vector embeddings for docs?</b></summary>

For a technical documentation corpus, users search for exact function names, error codes, and class properties. BM25 mathematically outperforms semantic embeddings for exact-lexicon matching at this scale, with zero cost, zero latency, and zero external dependencies.

</details>

<details>
<summary><b>Why session-scoped credentials instead of persistent config?</b></summary>

Storing API keys in config files is a security risk — they could be committed to git, leaked in logs, or accessed by other processes. Session-scoped memory-only credentials are lost on restart, which is intentional: it forces re-authentication and prevents stale credentials from persisting.

</details>

<details>
<summary><b>Why preview & confirmation for destructive ops?</b></summary>

AI assistants can misinterpret user intent. A user saying "remove the test bot" shouldn't accidentally delete a production bot. The two-step preview→confirm pattern gives the user a chance to verify before irreversible actions.

</details>

<details>
<summary><b>Why sync HTTP client instead of async?</b></summary>

FastMCP tool handlers can be sync or async. We use sync `httpx.Client` for simplicity and reliability. The retry sleep logic is async-aware (uses `run_in_executor`) to avoid blocking the event loop under HTTP transport.

</details>

---

## ❓ Frequently Asked Questions

<details>
<summary><b>Does the documentation search work offline?</b></summary>
Yes. Once installed, the BM25 index and documentation are 100% local. The API tools require internet to reach `api.telebotstudio.com`, but the documentation tools work without any network connection.
</details>

<details>
<summary><b>Can I deploy this on Render / Railway?</b></summary>
Yes. Run `python server.py --transport http` and the server reads the `PORT` environment variable automatically.
</details>

<details>
<summary><b>Is my API key safe?</b></summary>
Your API key is stored in server memory only — never written to disk, never logged in cleartext. It is transmitted over HTTPS to `api.telebotstudio.com` and is lost when the server restarts. For multi-user HTTP deployments, see the session isolation note in `api/session.py`.
</details>

<details>
<summary><b>What happens if a batch operation partially fails?</b></summary>
The executor runs each step independently. If step 3 of 5 fails, steps 4 and 5 still execute. The `BatchResult` reports per-step success/failure so you can see exactly what happened.
</details>

---

## 🛠️ Development Guide

### How to Add a New API Endpoint Wrapper

The architecture is designed for extensibility. To add support for a new API endpoint:

1. Add request/response models in `api/models.py`
2. Add a method to the appropriate manager (`api/bots.py`, `api/commands.py`, or `api/bot_control.py`)
3. Add a tool function in `tools/api_tools.py` with the `@mcp.tool` decorator
4. If it's destructive, add preview support with `confirm` parameter
5. If it's a multi-step operation, add a planner method in `agent/planner.py`

### How to Add Documentation
1. Add `.md` files to the `docs/` directory.
2. Restart the server. The BM25 index rebuilds automatically.

### Coding Style
PEP 8 with type hints. `from __future__ import annotations` in every file. Keep functions pure where possible.

---

## 🗺️ Roadmap

### v0.2.0 (Current)
- [x] 8 documentation search tools (BM25)
- [x] 18 bot management API tools
- [x] Session-scoped credential manager
- [x] Agent pipeline (Planner → Validator → Preview → Executor)
- [x] Preview & confirmation for destructive operations
- [x] Batch operations with per-step error reporting
- [x] Thread-safe credential storage
- [x] Async-aware retry logic
- [x] Docker + Render deployment
- [x] `/health` endpoint

### Upcoming
- [ ] Connection pooling for API calls
- [ ] FastMCP session middleware for per-client credential isolation
- [ ] Exact phrase match boosting for search
- [ ] Heading hierarchy boosting (H1 > H3)

### Future
- [ ] GitHub Actions CI/CD pipeline
- [ ] Pytest unit and integration test suite
- [ ] Abstract into a Generic Documentation MCP Framework

---

## 📝 Changelog

### v0.2.0
* Added 18 TeleBot Studio API management tools.
* Session-scoped, thread-safe credential manager.
* Agent pipeline with Planner → Validator → Preview → Executor.
* Preview & confirmation for destructive operations.
* Batch command create/delete.
* Async-aware retry with exponential backoff.
* Token masking in logs and responses.
* Updated README with Phase 2 documentation.

### v0.1.0
* Initial release: 8 documentation search tools.
* BM25 ranking with unigram + bigram tokenization.
* LRU caching, input validation, path traversal prevention.
* STDIO and HTTP/Streamable HTTP transports.
* Docker support, `/health` endpoint.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Ensure your code passes basic linting.
4. Write a clear, descriptive commit message.
5. Open a Pull Request against the `main` branch.

---

## 🙏 Credits

* **[FastMCP](https://github.com/jlowin/fastmcp)** — Python framework for building MCP servers.
* **[rank-bm25](https://github.com/dorianbrown/rank_bm25)** — Pure Python BM25 implementation.
* **[TeleBot Studio](https://telebotstudio.com)** — The platform and documentation.
* **[Model Context Protocol](https://modelcontextprotocol.io)** — Anthropic's standard for AI tool integration.

---

<div align="center">

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Made with ❤️ by the community. Grounding AI in reality, one chunk at a time.

</div>
