from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

URL_TO_PARSE = os.getenv("URL_TO_PARSE")
WAIT_TIME_IN_SECONDS = os.getenv("WAIT_TIME_IN_SECONDS")
