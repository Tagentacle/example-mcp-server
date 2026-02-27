"""
Example MCP Server: Weather Service via Streamable HTTP.

Demonstrates how to build an MCP Server Node in a Tagentacle workspace
using the MCPServerNode base class. The server:
  - Inherits MCPServerNode (LifecycleNode + FastMCP + uvicorn)
  - Registers tools in on_configure() via self.mcp
  - Automatically exposes Streamable HTTP and publishes to /mcp/directory

Tool schemas are auto-generated from Python type hints by the MCP SDK.
"""

import asyncio
import logging
import os
from typing import Annotated

from pydantic import Field
from tagentacle_py_mcp import MCPServerNode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock weather data
WEATHER_DATA = {
    "Shenzhen": "32°C, Sunny",
    "Beijing": "15°C, Cloudy",
    "Tokyo": "22°C, Clear",
    "London": "12°C, Rainy",
    "New York": "18°C, Partly Cloudy",
}


class WeatherServer(MCPServerNode):
    """Weather MCP Server Node."""

    def __init__(self, mcp_port: int = 8200):
        super().__init__(
            "mcp_server_node",
            mcp_name="weather-server",
            mcp_port=mcp_port,
            description="Weather tool server (mock data)",
        )

    def on_configure(self, config):
        # Register tools BEFORE calling super (which reads port overrides)
        @self.mcp.tool(description="Get current weather for a given city (mock data)")
        def get_weather(
            city: Annotated[str, Field(description="City name")],
        ) -> str:
            result = WEATHER_DATA.get(city, f"25°C, Fair (no data for {city})")
            return f"Weather in {city}: {result}"

        super().on_configure(config)


async def main():
    port = int(os.environ.get("MCP_PORT", "8200"))
    node = WeatherServer(mcp_port=port)
    await node.bringup()
    await node.spin()


if __name__ == "__main__":
    asyncio.run(main())
