from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://login.bol.com/wsp/login"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
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

# Fetch Akamai data
akamai_data = client.akamai.fetch_and_extract(website_url=URL, user_agent=USER_AGENT, proxy=PROXY)

if not akamai_data:
    logger.error("Failed to retrieve Akamai data")
    exit(1)

# Solve 3 sensors (requires 3 API calls, you pay per sensor)
# For better pricing, use the private endpoint: support@salamoonder.com
data = ""
for i in range(3):
    task_id = client.task.createTask(
        task_type="AkamaiWebSensorSolver",
        url=akamai_data['base_url'],
        abck=akamai_data['abck'],
        bmsz=akamai_data['bm_sz'],
        script=akamai_data['script_data'],
        sensor_url=akamai_data['akamai_url'],
        user_agent=USER_AGENT,
        count=i,
        data=data
    )
    
    result = client.task.getTaskResult(task_id)
    payload = result['payload']
    data = result['data']

    cookie = client.akamai.post_sensor(
        akamai_url=akamai_data['akamai_url'],
        sensor_data=payload,
        user_agent=USER_AGENT,
        website_url=URL,
        proxy=PROXY
    )

# Verify and set cookies
# Note: Some sites don't use ~0~ even after solving, this doesn't mean it failed, in this specific example we can check it via ~0~.
if "~0~" in cookie['abck']:
    logger.success(f"Successfully solved Akamai on {URL}")
    for k, v in cookie.items():
        client.session.cookies.set(k, str(v), domain=".bol.com")

    # Your action here.
else:
    logger.error("Failed to solve Akamai")