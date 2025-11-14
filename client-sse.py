import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def main():
    async with sse_client("http://0.0.0.0:8050/sse") as (read_stream , write_stream):
        async with ClientSession(read_stream , write_stream) as session:
            await session.initialize()


            print("Available tools : ")
            tools_list = await session.list_tools()
            for tool in tools_list.tools:
                print(f" - {tool.name} : {tool.description}")
            

            result = await session.call_tool("add" , {"a" : 15 , "b" : 20})
            print(result.content[0].text)



if __name__ == "__main__":
    asyncio.run(main())