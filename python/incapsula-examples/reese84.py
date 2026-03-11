import asyncio
from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://example.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

HEADERS = {
    "User-Agent": USER_AGENT,
    "sec-ch-ua": '"Google Chrome";v="142", "Not-A.Brand";v="8", "Chromium";v="142"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "accept-language": "en-US,en;q=0.9",
}

async def main():
    async with Salamoonder(API_KEY) as client:
        response = await client.get(URL, headers=HEADERS)

        if "Pardon Our Interruption" not in response.text and "Incapsula incident ID" not in response.text:
            logger.info("No challenge detected")
            return

        logger.info("Incapsula challenge detected")

        # Solve the challenge
        task_id = await client.task.createTask(
            task_type="IncapsulaReese84Solver",
            website=URL,
            submit_payload=True,
            # Optional parameters
            # reese_url="..." <- https://apidocs.salamoonder.com/tasks/incapsula/reese84#what-if-your-response-doesn't-match-ours
            # user_agent=USER_AGENT
        )

        result = await client.task.getTaskResult(task_id)

        if "token" not in result:
            logger.error(f"Failed to solve challenge: {result}")
            return

        token = result["token"]

        client.session.cookies.set(
            name="reese84",
            value=token,
            domain=".example.com",
            path="/",
            secure=True
        )

        response = await client.get(URL, headers=HEADERS)

        if "Pardon Our Interruption" not in response.text and "Incapsula incident ID" not in response.text:
            logger.success("Successfully bypassed Incapsula!")
        else:
            logger.error("Bypass failed")

if __name__ == "__main__":
    asyncio.run(main())