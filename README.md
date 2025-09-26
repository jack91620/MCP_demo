# MCP Demo

这是一个极简的 Model Context Protocol (MCP) 演示项目，使用纯 Python 模拟了
一个 MCP 服务端与客户端之间的交互流程。

## 功能概述

- `MCPServer`：注册工具、汇报能力并处理请求。
- `MCPClient`：执行握手、列出工具并调用工具。
- 示例工具 `get_weather` 用于演示如何暴露函数给客户端调用。

## 运行示例

```bash
python -m mcp_demo.server
```

或者运行客户端侧的完整演示：

```bash
python -m mcp_demo.client
```

## 项目结构

```
mcp_demo/
  __init__.py
  server.py
  client.py
README.md
```

## 开发环境

- Python 3.11+

这是一个示例项目，没有外部依赖。
