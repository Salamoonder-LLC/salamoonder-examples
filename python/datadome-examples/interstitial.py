import asyncio
from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://example.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

HEADERS = {
    "User-Agent": USER_AGENT,
    "sec-ch-ua": '"Google Chrome";v="139", "Not-A.Brand";v="8", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "accept-language": "en-US,en;q=0.9",
}

async def main():
    async with Salamoonder(API_KEY) as client:
        response = await client.get(URL, headers=HEADERS, proxy=PROXY, impersonate="chrome133a")
        cookies = response.cookies.get('datadome')

        if not cookies:
            logger.error("No DataDome cookie found")
            return

        constructed_url = client.datadome.parse_interstitial_url(response.text, cookies, URL)

        task_id = await client.task.createTask(
            task_type="DataDomeInterstitialSolver",
            captcha_url=constructed_url,
            user_agent=USER_AGENT,
            country_code="us"
        )

        result = await client.task.getTaskResult(task_id)

        if "cookie" not in result:
            logger.error(f"Failed to solve challenge: {result}")
            return

        cookie_str = result["cookie"]
        solved_cookie = cookie_str.split("datadome=", 1)[1].split(";", 1)[0] if "datadome=" in cookie_str else cookie_str.split(";", 1)[0]

        client.session.cookies.set(
            name="datadome",
            value=solved_cookie,
            domain=".example.com",
            path="/",
            secure=True
        )

        response = await client.get(URL, headers=HEADERS, proxy=PROXY, impersonate="chrome133a")

        if response.status_code == 200:
            logger.success(response.text)
            logger.success("Successfully bypassed Interstitial!")
        else:
            logger.error(f"Bypass failed (response: {response.text})")

if __name__ == "__main__":
    asyncio.run(main())