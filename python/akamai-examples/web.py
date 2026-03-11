import asyncio
from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://example.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

HEADERS = {
    "User-Agent": USER_AGENT,
    "sec-ch-ua": '"Google Chrome";v="141", "Not-A.Brand";v="8", "Chromium";v="141"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "accept-language": "en-US,en;q=0.9",
}

async def main():
    async with Salamoonder(API_KEY) as client:
        akamai_data = await client.akamai.fetch_and_extract(website_url=URL, user_agent=USER_AGENT, proxy=PROXY)

        if not akamai_data:
            logger.error("Failed to retrieve Akamai data")
            return

        # Solve 3 sensors (requires 3 API calls, you pay per sensor)
        # For better pricing, use the private endpoint: support@salamoonder.com
        data = ""
        for i in range(3):
            task_id = await client.task.createTask(
                task_type="AkamaiWebSensorSolver",
                url=akamai_data['base_url'],
                abck=akamai_data['abck'],
                bmsz=akamai_data['bm_sz'],
                script=akamai_data['script_data'],
                sensor_url=akamai_data['akamai_url'],
                user_agent=USER_AGENT,
                count=i,
                data=data
            )
            
            result = await client.task.getTaskResult(task_id)
            payload = result['payload']
            data = result['data']

            cookie = await client.akamai.post_sensor(
                akamai_url=akamai_data['akamai_url'],
                sensor_data=payload,
                user_agent=USER_AGENT,
                website_url=URL,
                proxy=PROXY
            )

        logger.success(f"Successfully solved Akamai on {URL}")

        for k, v in cookie.items():
            client.session.cookies.set(k, str(v), domain=".example.com")

if __name__ == "__main__":
    asyncio.run(main())