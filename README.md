# Examen DVC et Dagshub

```bash       
project-dvc-dagsHUB/
├── .dvc/
│   ├── cache/
│   ├── tmp/
│   ├── .gitignore
│   ├── config
│   └── config.local
├── data/
│   ├── .gitignore
│   ├── processed_data/
│   │   ├── scaled_data/
│   │   │   ├── X_test_scaled.csv
│   │   │   └── X_train_scaled.csv
│   │   └── split_data/
│   │       ├── X_test.csv
│   │       ├── X_train.csv
│   │       ├── y_test.csv
│   │       └── y_train.csv
│   └── raw_data/
│       ├── .gitignore
│       └── raw.csv
├── metrics/
│   └── scores.json
├── models/
│   ├── deployment_model/
│   │   └── deployment_trained_model.pkl
│   └── initial_model/
│       └── grid_initial_model.pkl
├── my_env/
├── src/
│   ├── data/
│   │   ├── correlation.py
│   │   ├── preprocessing.py
│   │   └── splitting.py
│   └── models/
│       ├── evaluation.py
│       ├── gridsearch.py
│       ├── training.py
│       └── XGB_regressor.py
├── .dvcignore
├── .gitignore
├── dvc.yaml
├── dvc.lock
├── README.md
├── requirements.txt
└── run_pipeline.sh

     
```

## Steps to follow 
Convention : All python scripts must be run from the root specifying the relative file path.

### Create a virtual environment using Virtualenv.
    `python -m venv my_env`
### Activate it 
    `./my_env/Scripts/activate`
    or
    `source my_env/Scripts/activate`

### Install the packages from requirements.txt
    `pip install -r requirements.txt`

### OPTIONAL: run the pipeline locally before starting DVC to ensure it runs smoothly:
    `chmod +x run_pipeline.sh` ### It will give permission.    
    ./run_pipeline.sh ### it will create (splitting>preprocessing>gridsearch>training>evaluation)

### the files src/models/XGB_regressor.py and src/data/correlation.py are meant to explore different paths to increase R2 but they aren't used in this workflow

### initialize dvc
'dvc.init'

### connect DAGsHub to GitHub repo if not yet connected
follow instructions on https://dagshub.com/docs/integration_guide/github/

### make DagsHub the remote
the precise code is ready in DagsHub reomte button:
'dvc remote add origin s3://dvc'
'dvc remote modify origin endpointurl https://dagshub.com/nom_utilisateur/Template_MLOps_accidents.s3'
'dvc remote modify origin --local access_key_id your_token'
'dvc remote modify origin --local secret_access_key your_token'

### make origin as the default remote:
'dvc remote default origin'

### .gitignore
modify content:
/my_env
/data
/models

### add stages and then repro
this will create the pipeline as .dvc file then repro will create dvc.lock file:

retriving stage: '
dvc stage add -n retrieving \
  -d src/data/retrieve_raw.py \
  -o data/raw_data/raw.csv \
  python src/data/retrieving.py
'
splitting stage: '
dvc stage add -n splitting \
  -d src/data/splitting.py \
  -d data/raw_data \
  -o data/processed_data/split_data/ \
  python src/data/splitting.py
'
preprocessing stage: '
dvc stage add -n preprocessing \
  -d src/data/preprocessing.py \
  -d data/processed_data/split_data \
  -o data/processed_data/scaled_data \
  python src/data/preprocessing.py
'
gridsearch stage: '
dvc stage add -n gridsearch \
  -d src/models/gridsearch.py \
  -d data/processed_data/split_data \
  -d data/processed_data/scaled_data \
  -o models/initial_model \
  python src/models/gridsearch.py
'
training stage: '
dvc stage add -n training \
  -d src/models/training.py \
  -d data/processed_data/split_data \
  -d data/processed_data/scaled_data \
  -d models/initial_model \
  -o models/deployment_model \
  python src/models/training.py
'
evaluation stage: '
dvc stage add -n evaluation \
  -d src/models/evaluation.py \
  -d data/processed_data/split_data \
  -d data/processed_data/scaled_data \
  -d models/deployment_model \
  -o data/prediction_data/predictions.csv \
  -M metrics/scores.json \
  python src/models/evaluation.py
'

### see the workflow
to see the workflow use:
'dvc dag'

                                              +------------+                                              
                                              | retrieving |                                              
                                              +------------+                                              
                                                     *                                                    
                                                     *                                                    
                                                     *                                                    
                                              +-----------+                                               
                                            **| splitting |*****                                          
                                     *******  +-----------+ *************                                 
                               ******                *          *****    **********                       
                        *******                      *               ****          *********              
                    ****                             *                   ****               *********     
    +---------------+                                *                       ***                     *****
    | preprocessing |***                             *                         *                         *
    +---------------+   ******                       *                         *                         *
      **           **         *******                *                         *                         *
    **               **              ******          *                         *                         *
  **                   **                  ****      *                         *                         *
**                       ****                 +------------+                 ***                         *
*                            ****             | gridsearch |             ****                            *
*                                *****        +------------+         ****                                *
*                                     ****           *          *****                                    *
*                                         ****       *      ****                                         *
*                                             ***    *   ***                                             *
*****                                          +----------+                                          *****
     *********                                 | training |                                 *********     
              **********                       +----------+                        *********              
                        *********                    *                    *********                       
                                 *********           *           *********                                
                                          *****      *      *****                                         
                                              +------------+                                              
                                              | evaluation |                                              
                                              +------------+  

### reproduce the workflow
eventually run the pipeline by using:
'dvc repro'
or to reproduce a specific stage:
'dvc repro any_stage'

### NEXT STEPS:
'git add .'  # stage all the files except those in gitignore
'git commit -m "pipeline: RFRegressor, R2=0.24459"' # commit the pipeline
'dvc commit'
'dvc push'
'git push origin master'

### push error fix
in windows when running 'dvc push' a compatibility issue might arise. to solve:
'pip uninstall pyopenssl cryptography -y
pip install cryptography==41.0.7
pip install pyopenssl==23.2.0'