import asyncio
from mcp import ClientSession , StdioServerParameters
from mcp.client.stdio import stdio_client
import json

from google import genai
client = genai.Client(api_key = "")

CITY_TO_STATE = {
    "new york": "NY",
    "los angeles": "CA",
}
CITY_TO_COORDS = {
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
}

async def ask_llm(question : str) -> json:
    """Ask the LLM tool to call and with which parameters. """
    prompt = f"""
You are a routing assistant. The user asked: "{question}".

You MUST respond with a JSON object ONLY, with this structure:

{{
  "tool": "get_alerts" or "get_forecast",
  "args": {{
      "city": "<city name>"
  }}
}}

Rules:
- If the user asks about weather alerts, choose "get_alerts".
- If the user asks about normal weather/forecast, choose "get_forecast".
- Valid cities: {list(CITY_TO_STATE.keys())}

Respond with ONLY valid JSON. No explanations.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    text = response.text
    return json.loads(text)



async def main():
    parameters = StdioServerParameters(
        command= 'python',
        args=['server.py']
    )


    async with stdio_client(parameters) as (read_stream , write_stream):
        async with ClientSession(read_stream , write_stream) as session:
            await session.initialize()

            user_question = "What is the weather in New York?"
            decision = await ask_llm(user_question)


            city = decision["args"]["city"].lower()
            tool = decision["tool"]

            if tool == "get_alerts" :
                args = {
                    "state" : CITY_TO_STATE[city]
                }
            else:
                args = {
                    "latitude": CITY_TO_COORDS[city][0], "longitude": CITY_TO_COORDS[city][1]
                }

            result = await session.call_tool(tool , args)
            print("answer:" , result)




if __name__ == '__main__':
    asyncio.run(main())
