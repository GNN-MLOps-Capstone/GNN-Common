
from datetime import timedelta
from docker.types import Mount

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator


DAG_NAME = "Capstone_Stock_RecSys"
DEFAULT_ARGS = {
    'owner': '책임자명',
    'depends_on_past': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    DAG_NAME,
    default_args=DEFAULT_ARGS,
    description="주식 추천 시스템을 위한 GNN 모델 학습",
    start_date=pendulum.datetime(2025, 1, 8, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    tags=['Capstone 프로젝트']
) as dag:
    
    train = DockerOperator(
        task_id='train_model',
        image='학습 태스트 이미지명:latest',
        container_name='학습 태스크 컨테이너명',
        api_version='auto',
        auto_remove='success',
        command='python run_4_train_task.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='네트워크명',
        working_dir='/app',
        mount_tmp_dir=False,
        mounts=[
            Mount(source='static_volume', target='/app/static', type='volume')
        ],
        environment={
            'DB_HOST': '데이터베이스 호스트 명',
            'DB_PORT': '데이터베이스 포트',
            'DB_USER': '데이터베이스 유저 명',
            'DB_PASSWORD': '데이터베이스 PW',
            'DB_NAME': '데이터베이스 명',
            'AWS_ACCESS_KEY_ID': 'AWS 접근 키',
            'AWS_SECRET_ACCESS_KEY': 'AWS 암호 키',
            'MLFLOW_S3_ENDPOINT_URL': 'http://minio:9000'
        }
    )

    deploy = DockerOperator(
        task_id='deploy_model',
        image='crypto_deploy_image:latest',
        container_name='crypto_forecast_deploy_task',
        api_version='auto',
        auto_remove='success',
        command='python run.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='crypto_forecast_crypto_network',
        working_dir='/app',
        mount_tmp_dir=False,
        mounts=[
            Mount(source='static_volume', target='/app/static', type='volume')
        ],
        environment={
            'DB_HOST': '데이터베이스 호스트 명',
            'DB_PORT': '데이터베이스 포트',
            'DB_USER': '데이터베이스 유저 명',
            'DB_PASSWORD': '데이터베이스 PW',
            'DB_NAME': '데이터베이스 명',
            'AWS_ACCESS_KEY_ID': 'AWS 접근 키',
            'AWS_SECRET_ACCESS_KEY': 'AWS 암호 키',
            'MLFLOW_S3_ENDPOINT_URL': 'http://minio:9000'
        }
    )

    train >> deploy