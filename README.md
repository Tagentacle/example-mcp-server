# example_mcp_server

An example **MCP Server Node** that exposes tools over the Tagentacle message bus.

## What it does

1. Connects to the Tagentacle Daemon as `mcp_server_node`
2. Registers a `get_weather` tool via FastMCP (schema auto-generated from type hints)
3. Serves incoming MCP JSON-RPC requests via `tagentacle_server_transport`
4. Stays running until terminated

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

- **FastMCP**: Tool schemas auto-generated from Python type hints — no JSON-Schema boilerplate.
- **`tagentacle_server_transport`**: Registers a Tagentacle Service at `/mcp/{node_id}/rpc` and bridges inbound JSON-RPC to the local MCP Server instance.
- **Standard MCP SDK**: Uses `@mcp.tool()` decorators — no bus-specific code in tool implementations.
