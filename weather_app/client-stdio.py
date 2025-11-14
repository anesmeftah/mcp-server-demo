import asyncio
from mcp import ClientSession , StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    parameters = StdioServerParameters(
        command= 'python',
        args=['server.py']
    )


    async with stdio_client(parameters) as (read_stream , write_stream):
        async with ClientSession(read_stream , write_stream) as session:
            await session.initialize()

            state = "CA"
            alerts = await session.call_tool("get_alerts", {"state": state})
            print(f"Weather alerts for {state}:\n{alerts.content[0].text}")




if __name__ == '__main__':
    asyncio.run(main())