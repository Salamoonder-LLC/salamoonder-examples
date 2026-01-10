from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://passport.twitch.tv/protected_login"
API_KEY = "sr-YOUR-KEY"
headers = {}

TWITCH_USERNAME = "REAL_TWITCH_USERNAME"
TWITCH_PASSWORD = "REAL_TWITCH_PASSWORD"

# Initialize client
client = Salamoonder(API_KEY)

# Solve the Kasada challenge
task_id = client.task.createTask(
    task_type="KasadaCaptchaSolver", 
    pjs_url="https://k.twitchcdn.net/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/p.js",
    cd_only="false"
)

result = client.task.getTaskResult(task_id)

if "x-kpsdk-ct" not in result:
    logger.error(f"Failed to solve challenge: {result}")
    exit(1)

headers.update({
    "x-kpsdk-cd": result['x-kpsdk-cd'],
    "x-kpsdk-ct": result['x-kpsdk-ct'],
    "user-agent": result['user-agent'],
})

payload = {
    "username": TWITCH_USERNAME,
    "password": TWITCH_PASSWORD,
    "undelete_user": False,
    "client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko"
}

# Verify bypass
response = client.session.post(URL, headers=headers, json=payload)

if '5025' not in response.text:
    logger.success(f"Successfully solved Kasada. {response.text}")
else:
    logger.error(f"Failed to solve Kasada {response.text}")
    exit(1)

