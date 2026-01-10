from salamoonder import Salamoonder
from loguru import logger

# Configuration
URL = "https://supercard.ch"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

# Initialize client
client = Salamoonder(API_KEY)

# Get initial response with DataDome challenge
response = client.get(URL, headers={"User-Agent": USER_AGENT}, proxy=PROXY, impersonate="chrome133a")
cookies = response.cookies.get('datadome')

if not cookies:
    print("No DataDome cookie found")
    exit(1)

# Parse slider challenge
constructed_url = client.datadome.parse_slider_url(response.text, cookies, URL)

# Solve the challenge
task_id = client.task.createTask(
    task_type="DataDomeSliderSolver",
    captcha_url=constructed_url,
    user_agent=USER_AGENT,
    country_code="ch"
)

result = client.task.getTaskResult(task_id)

if 'cookie' in result:
    solved_cookie = result['cookie'].split("datadome=")[1].split(";")[0]
else:
    logger.error(f"Failed to solve {result}")
    exit(1)

# Set solved cookie
client.session.cookies.set(
    name="datadome",
    value=solved_cookie,
    domain=".supercard.ch",
    path="/",
    secure=True
)

# Verify bypass
response = client.get(URL, headers={"User-Agent": USER_AGENT})

if response.status_code == 200:
    logger.success("[+] Successfully bypassed DD Slider.")
    logger.success(f"[+] Status Code: {response.status_code}")
else:
    logger.error("Bypass failed")
