"""
TeleBot Studio API MCP Tools.

Registers 18 new MCP tools on the FastMCP server instance:

Credential Tools (3):
  - tbs_set_api_key
  - tbs_set_bot_id
  - tbs_credential_status

Bot Management Tools (3):
  - tbs_create_bot
  - tbs_delete_bot        (preview-supported)
  - tbs_update_bot_token  (preview-supported)

Command Management Tools (5):
  - tbs_create_command
  - tbs_get_command
  - tbs_update_command    (preview-supported)
  - tbs_delete_command    (preview-supported)
  - tbs_list_commands

Bot Control Tools (3):
  - tbs_start_bot
  - tbs_stop_bot
  - tbs_restart_bot

Agent Tools (2):
  - tbs_deploy_bot
  - tbs_setup_commands

Batch Tools (2):
  - tbs_batch_create_commands
  - tbs_batch_delete_commands  (preview-supported)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tools.agent_tools import register_agent_tools
from tools.batch_tools import register_batch_tools
from tools.bot_tools import register_bot_tools
from tools.command_tools import register_command_tools
from tools.control_tools import register_control_tools
from tools.credential_tools import register_credential_tools

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_api_tools(mcp: FastMCP) -> None:
    """Register all TeleBot Studio API tools on the FastMCP instance."""
    register_credential_tools(mcp)
    register_bot_tools(mcp)
    register_command_tools(mcp)
    register_control_tools(mcp)
    register_agent_tools(mcp)
    register_batch_tools(mcp)
