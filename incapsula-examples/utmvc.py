from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://www.apria.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
API_KEY = "sr-YOUR-KEY"

HEADERS = {
    "User-Agent": USER_AGENT,
    "sec-ch-ua": '"Google Chrome";v="139", "Not-A.Brand";v="8", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "accept-language": "en-US,en;q=0.9",
}

# Initialize client
client = Salamoonder(API_KEY)

# Solve the challenge
task_id = client.task.createTask(
    task_type="IncapsulaUTMVCSolver",
    website=URL,
    user_agent=USER_AGENT
)

result = client.task.getTaskResult(task_id)

if "utmvc" not in result:
    logger.error(f"Failed to solve challenge: {result}")
    exit(1)

utmvc = result["utmvc"]

# Set token cookie
client.session.cookies.set(
    name="___utmvc",
    value=utmvc,
    domain="CHANGE_TO_CORRECT_DOMAIN",
    path="/",
    secure=True
)

logger.success(f"Successfully solved UTMVC challenge: {utmvc[:150]}")
logger.success(f"User-Agent: {result['user-agent']}")

# Your action here.
