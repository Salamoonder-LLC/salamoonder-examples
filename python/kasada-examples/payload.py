import salamoonder

# Keep in mind not using the same USER-AGENT as displayed as our docs will result in bad responses.
# https://apidocs.salamoonder.com/tasks/kasada/payload

URL = "https://yourdomain.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fp?x-kpsdk-v=j-1.2.170"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
PROXY = "http://user:pass@ip:port"
API_KEY = "sr-YOUR-KEY"

# Initialize client
client = salamoonder.Salamoonder(API_KEY)
data = client.kasada.parse_kasada_script(url=URL, user_agent=USER_AGENT, proxy=PROXY)

task_id = client.task.createTask(
    task_type="KasadaPayloadSolver",
    url="https://yourdomain.com",
    script_url=data["script_url"],
    script_content=data["script_content"],
)

result = client.task.getTaskResult(task_id)

post_solution = client.kasada.post_payload(
    url="https://yourdomain.com",
    solution=result,
    user_agent=USER_AGENT,
    proxy=PROXY,
    mfc=False
)

print("Solve result:", post_solution)