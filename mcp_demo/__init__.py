"""Simple MCP demo package."""

from .server import MCPServer, Tool, build_demo_server

__all__ = ["MCPServer", "Tool", "build_demo_server", "MCPClient"]


def __getattr__(name: str):  # pragma: no cover - convenience helper
    if name == "MCPClient":
        from .client import MCPClient as _MCPClient

        return _MCPClient
    raise AttributeError(name)
