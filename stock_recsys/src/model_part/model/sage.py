import os
from dotenv import load_dotenv

from utils.logger import get_logger

load_dotenv()

LOGGER = get_logger(
    os.getenv("LOGGING_FILE_NAME"),
    os.getenv("LOGGING_LEVEL")
)