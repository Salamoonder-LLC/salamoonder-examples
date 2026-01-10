from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://www.pokemoncenter.com/"
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

# Initialize client
client = Salamoonder(API_KEY)

# Get initial response
response = client.get(URL, headers=HEADERS)

if "Pardon Our Interruption" not in response.text:
    logger.info("No challenge detected")
    exit(0)

logger.info("Incapsula challenge detected")

# Solve the challenge
task_id = client.task.createTask(
    task_type="IncapsulaReese84Solver",
    website=URL,
    submit_payload=True,
    user_agent=USER_AGENT
)

result = client.task.getTaskResult(task_id)

if "token" not in result:
    logger.error(f"Failed to solve challenge: {result}")
    exit(1)

token = result["token"]

# Set token cookie
client.session.cookies.set(
    name="reese84",
    value=token,
    domain=".pokemoncenter.com",
    path="/",
    secure=True
)

# Verify bypass
response = client.get(URL, headers=HEADERS)

if "Pardon Our Interruption" not in response.text:
    logger.success("Successfully bypassed Incapsula!")
else:
    logger.error("Bypass failed")