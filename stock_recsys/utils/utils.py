import os
from dotenv import load_dotenv
from typing import Sequence, cast

from utils.logger import get_logger

load_dotenv()

# 로그 설정
LOGGER = get_logger(
    os.getenv("LOGGING_FILE_NAME"),
    os.getenv("LOGGING_LEVEL")
)


def load_spec_from_config(cfg_name):

    """
    stock_recsys/configs 경로에 있는 config 파일 하나를 읽어옵니다.

    Args:
        cfg_name(str): stock_recsys/configs 하위 경로에 존재하는 config 파일명. 확장자 제외.

    Returns:

    """

    meta_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgMeta

    load_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgLoad

    preprocess_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgPreprocess

    model_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgModel

    hyp_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgHyperparameter

    train_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgTrain

    evaluate_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgEvaluate

    deploy_spec = __import__(
        f"configs.{cfg_name}", fromlist=cast(Sequence[str], [None])
    ).CfgDeploy


    return meta_spec, load_spec, preprocess_spec, model_spec, hyp_spec, train_spec, evaluate_spec, deploy_spec
