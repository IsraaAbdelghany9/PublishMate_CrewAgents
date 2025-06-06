from Config.shared import *


output_dir = './PublishMate_agent_ouput/outputs'
os.makedirs(output_dir, exist_ok=True)


# Always store logs in a fixed directory like ~/my_project/logs
BASE_DIR = os.path.expanduser("~/PublishMate_CrewAgents/logs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

AGENT_LOG_FILE = os.path.join(LOGS_DIR, "agents.log")
