import asyncio
from mcp import ClientSession , StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    #define session parameters
    session_parameters = StdioServerParameters(
        command = "python", #expects a string not a list
        args=["server.py"]
    )

    #connect to the server
    async with stdio_client(session_parameters) as (read_stream , write_stream): #demarrage du sous-processus server.py in our case
        async with ClientSession(read_stream , write_stream) as session: #Session qui gere le protocole de comminucation (MCP Communication)
            await session.initialize()

            tools = await session.list_tools()
            print("Available Tools")
            for tool in tools.tools:
                print(f"- {tool.name} : {tool.description}")

            result = await session.call_tool("add" , arguments= {"a" : 2 , "b" : 3})
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())

