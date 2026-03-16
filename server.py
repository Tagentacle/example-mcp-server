"""
Example MCP Server: Weather Service via Streamable HTTP.

Demonstrates how to build an MCP Server in a Tagentacle workspace using
LifecycleNode + MCPServerComponent (composition pattern). The server:
  - Composes MCPServerComponent for FastMCP + uvicorn management
  - Registers tools in on_configure() via self.mcp_server.mcp
  - Automatically exposes Streamable HTTP and publishes to /mcp/directory

Tool schemas are auto-generated from Python type hints by the MCP SDK.
"""

import asyncio
import logging
import os
from typing import Annotated, Any, Dict

from pydantic import Field
from tagentacle_py_core import LifecycleNode
from tagentacle_py_mcp import MCPServerComponent

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


class WeatherServer(LifecycleNode):
    """Weather MCP Server — LifecycleNode + MCPServerComponent."""

    def __init__(self, mcp_port: int = 8200):
        super().__init__("mcp_server_node")
        self.mcp_server = MCPServerComponent(
            "mcp_server_node",
            mcp_name="weather-server",
            mcp_port=mcp_port,
            description="Weather tool server (mock data)",
        )

    def on_configure(self, config: Dict[str, Any]):
        # Register tools on the MCPServerComponent's FastMCP instance
        @self.mcp_server.mcp.tool(
            description="Get current weather for a given city (mock data)"
        )
        def get_weather(
            city: Annotated[str, Field(description="City name")],
        ) -> str:
            result = WEATHER_DATA.get(city, f"25°C, Fair (no data for {city})")
            return f"Weather in {city}: {result}"

        self.mcp_server.configure(config)

    async def on_activate(self):
        await self.mcp_server.start(publish_fn=self.publish)

    async def on_deactivate(self):
        await self.mcp_server.stop(publish_fn=self.publish)

    async def on_shutdown(self):
        await self.mcp_server.shutdown()


async def main():
    port = int(os.environ.get("MCP_PORT", "8200"))
    node = WeatherServer(mcp_port=port)
    await node.bringup()
    await node.spin()


if __name__ == "__main__":
    asyncio.run(main())
