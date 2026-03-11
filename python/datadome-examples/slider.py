import asyncio
from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://example.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

async def main():
    async with Salamoonder(API_KEY) as client:
        response = await client.get(URL, headers={"User-Agent": USER_AGENT}, proxy=PROXY, impersonate="chrome133a")
        cookies = response.cookies.get('datadome')

        if not cookies:
            print("No DataDome cookie found")
            return

        constructed_url = await client.datadome.parse_slider_url(response.text, cookies, URL)

        task_id = await client.task.createTask(
            task_type="DataDomeSliderSolver",
            captcha_url=constructed_url,
            user_agent=USER_AGENT,
            country_code="ch"
        )

        result = await client.task.getTaskResult(task_id)

        if 'cookie' in result:
            solved_cookie = result['cookie'].split("datadome=")[1].split(";")[0]
        else:
            logger.error(f"Failed to solve {result}")
            return

        client.session.cookies.set(
            name="datadome",
            value=solved_cookie,
            domain=".example.com",
            path="/",
            secure=True
        )

        response = await client.get(URL, headers={"User-Agent": USER_AGENT})

        if response.status_code == 200:
            logger.success("[+] Successfully bypassed DD Slider.")
            logger.success(f"[+] Status Code: {response.status_code}")
        else:
            logger.error("Bypass failed")

if __name__ == "__main__":
    asyncio.run(main())