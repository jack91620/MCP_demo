"""Toy MCP client that interacts with :mod:`mcp_demo.server`."""

from __future__ import annotations

from typing import Any, Dict

from .server import MCPServer


class MCPClient:
    """Simple synchronous client used for demonstration.

    The client keeps a reference to an :class:`MCPServer` instance and mimics
    the handshake and invocation flow described in the protocol.
    """

    def __init__(self, server: MCPServer) -> None:
        self.server = server
        self._capabilities: Dict[str, Any] | None = None

    def handshake(self) -> Dict[str, Any]:
        """Perform a capabilities handshake with the server."""

        self._capabilities = self.server.capabilities()
        return self._capabilities

    def list_tools(self) -> Dict[str, Any]:
        """Request a list of available tools."""

        return self.server.handle_request({"action": "list_tools"})

    def call_tool(self, tool_name: str, **arguments: Any) -> Dict[str, Any]:
        """Invoke a tool exposed by the server."""

        return self.server.handle_request(
            {"action": "call_tool", "tool": tool_name, "arguments": arguments}
        )


def run_demo() -> None:
    """Execute a small end-to-end demonstration."""

    from pprint import pprint

    from .server import build_demo_server

    server = build_demo_server()
    client = MCPClient(server)

    print("== Handshake ==")
    capabilities = client.handshake()
    pprint(capabilities)

    print("\n== List tools ==")
    tools = client.list_tools()
    pprint(tools)

    print("\n== Call tool ==")
    response = client.call_tool("get_weather", city="Shanghai")
    pprint(response)


if __name__ == "__main__":  # pragma: no cover - convenience demo
    run_demo()
