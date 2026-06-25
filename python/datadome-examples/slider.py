import asyncio
from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://example.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

HEADERS = {
    "User-Agent": USER_AGENT,
    "sec-ch-ua": '"Google Chrome";v="146", "Not-A.Brand";v="8", "Chromium";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "accept-language": "en-US,en;q=0.9",
}

async def main():
    async with Salamoonder(API_KEY) as client:
        response = await client.get(URL, headers=HEADERS, proxy=PROXY, impersonate="chrome133a")
        cookies = response.cookies.get('datadome')

        if not cookies:
            print("No DataDome cookie found")
            return

        challenge = await client.datadome.get_slider_challenge(
            html=response.text,
            datadome_cookie=cookies,
            referer=URL,
            user_agent=USER_AGENT,
        )

        task_id = await client.task.createTask(
            task_type="DataDomeSliderSolver",
            captcha_url=challenge['captcha_url'],
            challenge_page=challenge['challenge_page'],
            user_agent=USER_AGENT,
        )

        result = await client.task.getTaskResult(task_id)

        if 'url' not in result:
            logger.error(f"Failed to solve {result}")
            return

        cookie_response = await client.get(result['url'], headers=HEADERS, proxy=PROXY, impersonate="chrome133a")
        print(cookie_response.text)


if __name__ == "__main__":
    asyncio.run(main())