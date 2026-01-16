```
root                                    # Root directory
│
├── /airflow                            # Docker configs for Airflow
│   ├── /Dockerfile                     # Airflow Dockerfile
│   └── /requirements.txt               # Libraries for Airflow service
│       
├── /bash                               # Shell script
│   └── /create_mlflow_db.sh            # Create table for MLFlow (Example)
│       
├── /dags                               # DAGs for Airflow
│   ├── /crawling_workflow.py           # Workflow for web crawling
│   ├── /inference_workflow.py          # Workflow for inference
│   └── /train_workflow.py              # Workflow for train model
│       
├── /mlflow                             # Docker configs for MLFlow
│   └── /Dockerfile                     # MLFlow Dockerfile
│       
├── /stock_recsys                       # Store for project files
│   ├── /configs                        # Config files for project
│   │   └── /graph_sage.py              # Config file for Graph SAGE model (Example)
│   │       
│   ├──/logs                            # Store for log file
│   │   └── /logging.log                # Log (Example)
│   │       
│   ├── /sql                            # Store for query file
│   │   └── /query.sql                  # Query (Example)
│   │       
│   ├──/src                             # Store for source code
│   │   ├── /data_part                  # Source code from data part (Example)
│   │   │    
│   │   ├── /model_part                 # Source code from model part (Example)
│   │   │   ├── /deploy                 # Deploy (Example)
│   │   │   │   └──deploy.py            # Functions for model deploy (Example)
│   │   │   │    
│   │   │   ├── /evaluate               # Evaluate (Example)
│   │   │   │   └──evaluator.py         # Functions for model evaluate (Example)
│   │   │   │    
│   │   │   ├── /load                   # Load
│   │   │   │   └──loader.py            # Functions for data load (Example)
│   │   │   │    
│   │   │   ├── /model                  # Model (Example)
│   │   │   │   └──sage.py              # Store for graph model (Example)
│   │   │   │    
│   │   │   ├── /preprocess             # Preprocess
│   │   │   │   └──preprocessor.py      # Functions for data preprocessing
│   │   │   │    
│   │   │   └── /train                  # Train
│   │   │       └──trainer.py           # Functions for model training
│   │   │       
│   ├── /utils                          # Utils
│   │   ├── /logger.py                  # Functions for log file (Example)
│   │   └── /utils.py                   # Functions for project (Example)
│   │    
│   ├── /.env                           # Environment for project
│   ├── /README.md                      # This file
│   ├── /run_1_crawling_task.py         # First task (Example)
│   ├── /run_2_silter_layer_task.py     # Second task (Example)
│   ├── /run_3_gold_layer_task.py       # Third task (Example)
│   ├── /run_4_train_task.py            # Fourth task (Example)
│   ├── /run_5_deploy_task.py           # Fifth task (Example)
│   └── /run_6_inference_task.py        # Sixth task (Example)
│    
└── /docker-compose.yaml                # Service for Docker
```