# example_mcp_server

An example **MCP Server Node** that exposes tools via Streamable HTTP.

## What it does

1. Connects to the Tagentacle Daemon as `mcp_server_node`
2. Registers a `get_weather` tool via `MCPServerNode` (schema auto-generated from type hints)
3. Runs a Streamable HTTP endpoint on `MCP_PORT` (default 8200)
4. Publishes its URL to `/mcp/directory` for auto-discovery
5. Stays running until terminated

## Supported Tools

| Tool | Input | Output |
|------|-------|--------|
| `get_weather` | `{"city": "Shenzhen"}` | `"Weather in Shenzhen: 32°C, Sunny"` |

Supported cities: Shenzhen, Beijing, Tokyo, London, New York (others return a default).

## Prerequisites

- Tagentacle Daemon running (`tagentacle daemon`)

## Run

```bash
# Via CLI (recommended)
tagentacle run --pkg .
```

## Key Concepts

- **MCPServerNode**: Base class from `tagentacle-py-mcp` — handles Streamable HTTP server and `/mcp/directory` publishing.
- **FastMCP**: Tool schemas auto-generated from Python type hints — no JSON-Schema boilerplate.
- **Direct HTTP**: Agent Nodes connect directly to the server's HTTP endpoint — no bus-as-transport intermediary.
