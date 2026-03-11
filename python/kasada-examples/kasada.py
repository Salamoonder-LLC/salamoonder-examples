import asyncio
from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://example.com/auth/v2/customer/login"
API_KEY = "sr-YOUR-KEY"
headers = {}

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

async def main():
    async with Salamoonder(API_KEY) as client:
        task_id = await client.task.createTask(
            task_type="KasadaCaptchaSolver", 
            pjs_url="https://example.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/p.js",
            cd_only="false"
        )

        result = await client.task.getTaskResult(task_id)

        if "x-kpsdk-ct" not in result:
            logger.error(f"Failed to solve challenge: {result}")
            return

        headers.update({
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "ocp-apim-subscription-key": "b4d9f36380184a3788857063bce25d6a",
            "x-kpsdk-cd": result['x-kpsdk-cd'],
            "x-kpsdk-ct": result['x-kpsdk-ct'],
            "user-agent": result['user-agent'],
            "Referer": "https://www.example.com/"
        })

        payload = {
            "ShouldTimeout": False,
            "UserName": USERNAME,
            "Password": PASSWORD,
            "OriginRoute": 'home'
        }

        response = await client.session.post(URL, headers=headers, json=payload)

        if response.status_code != 429:
            logger.success(f"Successfully solved Kasada. {response.text}")
        else:
            logger.error(f"Failed to solve Kasada {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
