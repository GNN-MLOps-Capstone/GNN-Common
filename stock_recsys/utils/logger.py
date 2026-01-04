import os
import logging
from dotenv import load_dotenv

load_dotenv()

LOGGER_PATH = os.path.abspath(os.getenv("LOGGER_FILE_PATH"))
LOGGER_FORMAT = logging.Formatter(
    fmt = "[%(asctime)s.%(msecs)03d][%(filename)s::%(funcName)s::%(lineno)s][%(levelname)s] >> %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
)

def get_logger(name, level):

    # 로그 파일 생성 코드를 넣어주세요

    pass
