from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://bol.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port" # Important: Use The Netherlands as country in your proxy for bol.com
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

# Fetch Akamai SBSD data
akamai_data = client.akamai_sbsd.fetch_and_extract(
    website_url=URL,
    user_agent=USER_AGENT,
    proxy=PROXY
)

if not akamai_data:
    logger.error("Failed to retrieve Akamai SBSD data")
    exit(1)

# Solve the challenge
task_id = client.task.createTask(
    task_type="AkamaiSBSDSolver",
    url=akamai_data['base_url'],
    cookie=akamai_data['cookie_value'],
    sbsd_url=akamai_data['sbsd_url'],
    script=akamai_data['script_data']
)

result = client.task.getTaskResult(task_id)

# Post sensor data
cookie = client.akamai_sbsd.post_sbsd(
    sbsd_payload=result['payload'],
    post_url=akamai_data['sbsd_url'],
    user_agent=result['user-agent'],
    website_url=URL,
    proxy=PROXY
)

if cookie:
    logger.success(f"Successfully solved Akamai SBSD on {URL}")
    logger.info(f"Cookie Dict: {cookie}")

    # Set the cookie in your jar client.session.cookie.set()
    # And then your action. client.session.post()
else:
    logger.error("Failed to solve Akamai SBSD")