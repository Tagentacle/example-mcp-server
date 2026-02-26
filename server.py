"""
Example MCP Server: Weather Service over Tagentacle Bus.

This demonstrates how to run an MCP Server that serves tools over the
Tagentacle message bus using tagentacle_server_transport + FastMCP.

The server provides a "get_weather" tool that returns mock weather data.
Tool schemas are auto-generated from Python type hints by the official
MCP SDK — no hand-written JSON-Schema needed.
"""

import asyncio
import logging
from typing import Annotated

from pydantic import Field
from mcp.server.fastmcp import FastMCP
from tagentacle_py_core import Node
from tagentacle_py_mcp.transport import tagentacle_server_transport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server — tool schemas are auto-derived from type hints
mcp = FastMCP("weather-server")

# Mock weather data
WEATHER_DATA = {
    "Shenzhen": "32°C, Sunny",
    "Beijing": "15°C, Cloudy",
    "Tokyo": "22°C, Clear",
    "London": "12°C, Rainy",
    "New York": "18°C, Partly Cloudy",
}


@mcp.tool(description="Get current weather for a given city (mock data)")
def get_weather(
    city: Annotated[str, Field(description="City name")],
) -> str:
    result = WEATHER_DATA.get(city, f"25°C, Fair (no data for {city})")
    return f"Weather in {city}: {result}"


async def main():
    node = Node("mcp_server_node")
    await node.connect()
    spin_task = asyncio.create_task(node.spin())

    logger.info("Starting Weather MCP Server over Tagentacle bus...")

    async with tagentacle_server_transport(node) as (read_stream, write_stream):
        await mcp._mcp_server.run(
            read_stream,
            write_stream,
            mcp._mcp_server.create_initialization_options(),
        )

    spin_task.cancel()
    try:
        await spin_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
