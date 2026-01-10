from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://services.chipotle.com/auth/v2/customer/login"
API_KEY = "sr-YOUR-KEY"
headers = {}

CHIPOTLE_USERNAME = "REAL_CHIPOTLE_USERNAME"
CHIPOTLE_PASSWORD = "REAL_CHIPOTLE_PASSWORD"

# Initialize client
client = Salamoonder(API_KEY)

# Solve the Kasada challenge
task_id = client.task.createTask(
    task_type="KasadaCaptchaSolver", 
    pjs_url="https://services.chipotle.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/p.js",
    cd_only="false"
)

result = client.task.getTaskResult(task_id)

if "x-kpsdk-ct" not in result:
    logger.error(f"Failed to solve challenge: {result}")
    exit(1)

headers.update({
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "ocp-apim-subscription-key": "b4d9f36380184a3788857063bce25d6a",
    "x-kpsdk-cd": result['x-kpsdk-cd'],
    "x-kpsdk-ct": result['x-kpsdk-ct'],
    "user-agent": result['user-agent'],
    "Referer": "https://www.chipotle.com/"
})

payload = {
    "ShouldTimeout": False,
    "UserName": CHIPOTLE_USERNAME,
    "Password": CHIPOTLE_PASSWORD,
    "OriginRoute": 'home'
}

# Verify bypass
response = client.session.post(URL, headers=headers, json=payload)

if response.status_code != 429:
    logger.success(f"Successfully solved Kasada. {response.text}")
else:
    logger.error(f"Failed to solve Kasada {response.text}")
    exit(1)

