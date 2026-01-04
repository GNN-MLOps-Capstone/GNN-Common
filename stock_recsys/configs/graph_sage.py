import os
from dotenv import load_dotenv

load_dotenv()

DEPLOYMENT = os.getenv("DEPLOYMENT")

class CfgMeta:
    # 메타 정보와 관련된 설정 값을 넣어주세요

    prefix = DEPLOYMENT

    if DEPLOYMENT == "ops":
        
        schema = "스키마명"
        table = f"{prefix}_테이블명"
        output_table_1 = f"{prefix}_산출물테이블1"
        output_table_2 = f"{prefix}_산출물테이블2"
        output_table_3 = f"{prefix}_산출물테이블3"
        experiment_name = f"{prefix}_MLFlow실험명"

    elif DEPLOYMENT == "dev":
        
        schema = "스키마명"
        table = f"{prefix}_테이블명"
        output_table_1 = f"{prefix}_산출물테이블1"
        output_table_2 = f"{prefix}_산출물테이블2"
        output_table_3 = f"{prefix}_산출물테이블3"
        experiment_name = f"{prefix}_MLFlow실험명"

    elif DEPLOYMENT == "test_cs":
    
        schema = "스키마명"
        table = f"{prefix}_테이블명"
        output_table_1 = f"{prefix}_산출물테이블1"
        output_table_2 = f"{prefix}_산출물테이블2"
        output_table_3 = f"{prefix}_산출물테이블3"
        experiment_name = f"{prefix}_MLFlow실험명"

    else:
        raise ValueError(".env 파일의 DEPLOYMENT 변수를 확인해주세요")
    

class CfgLoad:
    # 모델에 활용되기 위한 파일명을 넣어주세요
    # 예시로 parquet 파일을 활용한다고 가정하겠습니다.

    train_mart = "학습마트파일.parquet"
    test_mart = "검증마트파일.parquet"


class CfgPreprocess:
    # 전처리 관련 설정 값이 있다면 넣어주세요

    pass # TODO: 에러 방지용. 불필요시 삭제.

class CfgModel:
    # 모델 관련 설정 값이 있다면 넣어주세요

    name = "GraphSAGE"


class CfgHyperparameter:
    # 하이퍼파라미터 관련 설정 값이 있다면 넣어주세요

    hidden_dim = 100
    num_layers = 10
    learning_rate = 0.0005


class CfgTrain:
    # 학습 관련 설정 값이 있다면 넣어주세요

    num_workers = 4
    num_epochs = 10
    

class CfgEvaluate:
    # 검증 관련 설정 값이 있다면 넣어주세요

    pass # TODO: 에러 방지용. 불필요시 삭제.


class CfgDeploy:
    # 배포 관련 설정 값이 있다면 넣어주세요

    model_name = "GraphSAGE"
    model_alias = "Champion"