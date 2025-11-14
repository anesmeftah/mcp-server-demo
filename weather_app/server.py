from mcp.server.fastmcp import FastMCP
import httpx
import asyncio
import typing


NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

mcp = FastMCP("weather")

async def make_nws_request(url : str) -> dict[str , any] | None:
    """ Make a request to the weather AI """
    headers = {
        "User-Agent" : USER_AGENT ,
        "Accept" : "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = client.get(url , headers= headers , timeout= 30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        

def format_alert(feature : dict) -> str:
    """ Converts results into str """
    props = feature["propreties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state : str) -> str:
    """Fetch weather alerts for USA state"""
    url = f"https://api.weather.gov/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    
    if not data["features"]:
        return "no active alerts found for this state."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


def run_server():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    run_server()
