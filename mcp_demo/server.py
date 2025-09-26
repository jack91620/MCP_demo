"""Minimal Model Context Protocol (MCP) server implementation for demo purposes.

This module mimics the core ideas of the MCP protocol without implementing the
full specification. It allows registering tools (functions) and responding to
simple JSON-compatible requests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class Tool:
    """Represents a callable tool exposed by the MCP server."""

    name: str
    description: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]

    def run(self, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the tool with the given arguments."""

        arguments = arguments or {}
        return self.func(arguments)


class MCPServer:
    """Very small in-memory MCP server.

    The server keeps track of the registered tools and implements enough of the
    handshake protocol to be used for demonstrations. Requests and responses
    are represented as simple dictionaries which can be serialized to JSON by
    the caller.
    """

    def __init__(self, name: str, version: str = "0.1.0") -> None:
        self.name = name
        self.version = version
        self._tools: Dict[str, Tool] = {}

    # ------------------------------------------------------------------
    # Handshake helpers
    # ------------------------------------------------------------------
    def capabilities(self) -> Dict[str, Any]:
        """Return server capabilities similar to the MCP spec."""

        return {
            "name": self.name,
            "version": self.version,
            "tools": [
                {"name": tool.name, "description": tool.description}
                for tool in self._tools.values()
            ],
        }

    # ------------------------------------------------------------------
    # Tool registration and execution
    # ------------------------------------------------------------------
    def register_tool(self, tool: Tool) -> None:
        """Register a new tool that can be invoked by clients."""

        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a request from the client.

        The request is expected to contain an ``action`` field and optional
        ``arguments``. Only a subset of actions is supported for the demo.
        """

        action = request.get("action")
        if action == "list_tools":
            return {
                "status": "ok",
                "result": [
                    {"name": tool.name, "description": tool.description}
                    for tool in self._tools.values()
                ],
            }
        if action == "call_tool":
            tool_name = request.get("tool")
            arguments = request.get("arguments") or {}
            if tool_name not in self._tools:
                return {
                    "status": "error",
                    "error": f"Unknown tool '{tool_name}'",
                }
            try:
                result = self._tools[tool_name].run(arguments)
            except Exception as exc:  # pragma: no cover - demonstration only
                return {"status": "error", "error": str(exc)}
            return {"status": "ok", "result": result}

        return {"status": "error", "error": f"Unsupported action '{action}'"}


def weather_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Example tool returning fake weather data."""

    city = arguments.get("city", "Unknown")
    return {
        "city": city,
        "temperature_c": 23.5,
        "condition": "Sunny with clouds",
        "advice": "Remember to bring sunglasses!",
    }


def build_demo_server() -> MCPServer:
    """Create an ``MCPServer`` preloaded with demo tools."""

    server = MCPServer(name="Demo MCP Server", version="1.0.0")
    server.register_tool(
        Tool(
            name="get_weather",
            description="Return fake weather information for a city.",
            func=weather_tool,
        )
    )
    return server


if __name__ == "__main__":
    server = build_demo_server()
    print("Server capabilities:")
    print(server.capabilities())
    print("\nCalling the 'get_weather' tool:")
    response = server.handle_request(
        {"action": "call_tool", "tool": "get_weather", "arguments": {"city": "Shanghai"}}
    )
    print(response)
