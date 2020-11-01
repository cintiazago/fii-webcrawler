from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

URL_TO_PARSE = os.getenv("URL_TO_PARSE")
REQUEST_WAIT_TIME_IN_SECONDS = os.getenv("REQUEST_WAIT_TIME_IN_SECONDS")
WEB_DRIVER_OPTION_HEADLESS = os.getenv("WEB_DRIVER_OPTION_HEADLESS")
