import os
import argparse
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# from src.data_part import 필요 모듈명을 불러와 주세요
# from src.model_part import 필요 모듈명을 불러와 주세요
from utils.logger import get_logger
from utils.utils import load_spec_from_config

load_dotenv()

# 환경변수 설정
TIME_ZONE = ZoneInfo(os.getenv("TIME_ZONE"))

# 로그 설정
LOGGER = get_logger(
    os.getenv("LOGGING_FILE_NAME"),
    os.getenv("LOGGING_LEVEL")
)


class Crawler:

    def __init__(self, cfg_meta):

        self.cfg_meta = cfg_meta


    def run(self):

        # 실행 코드를 작성해 주세요
        # Data Part(stock_recsys/src/data_part 하위 경로), Model Part(stock_recsys/src/model_part 하위 경로)에서 개발한 모듈을 호출하여 실행하는 코드를 작성해주시면 됩니다.

        pass # TODO: 에러 방지용. 불필요시 삭제.



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="graph_sage", help="Config 파일명.")

    args = parser.parse_args()


    (
        cfg_meta,
        cfg_load,
        cfg_preprocess,
        cfg_model,
        cfg_hyp,
        cfg_train,
        cfg_evaluate,
        cfg_deploy
    ) = load_spec_from_config(args.config)

    crawler = Crawler(cfg_meta)

    crawler.run()