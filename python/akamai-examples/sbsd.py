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
        akamai_data = await client.akamai_sbsd.fetch_and_extract(
            website_url=URL,
            user_agent=USER_AGENT,
            proxy=PROXY
        )

        if not akamai_data:
            logger.error("Failed to retrieve Akamai SBSD data")
            return

        task_id = await client.task.createTask(
            task_type="AkamaiSBSDSolver",
            url=akamai_data['base_url'],
            cookie=akamai_data['cookie_value'],
            sbsd_url=akamai_data['sbsd_url'],
            script=akamai_data['script_data']
        )

        result = await client.task.getTaskResult(task_id)

        cookie = await client.akamai_sbsd.post_sbsd(
            sbsd_payload=result['payload'],
            post_url=akamai_data['sbsd_url'],
            user_agent=result['user-agent'],
            website_url=URL,
            proxy=PROXY
        )

        if cookie:
            logger.success(f"Successfully solved Akamai SBSD on {URL}")
            logger.info(f"Cookie Dict: {cookie}")

            # Set the cookie in your jar 
            # And then do your action.
        else:
            logger.error("Failed to solve Akamai SBSD")

if __name__ == "__main__":
    asyncio.run(main())