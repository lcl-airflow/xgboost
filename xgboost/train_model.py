import datetime
import os
import subprocess
import sys
import pandas as pd
import xgboost as xgb

MODEL_FILENAME= 'model.bst'

class train_model: 
    # Constructor 
    def __init__(self, data_dir, data_filename, target_filename, staging_bucket ):  
        self.data_dir=data_dir
        self.data_filename=data_filename
        self.target_filename=target_filename
        self.staging_bucket= staging_bucket
    # To get name 

    def fetch(self):
        print( os.path.join(self.data_dir, self.data_filename) )
        subprocess.check_call(['gsutil', 'cp', os.path.join(self.data_dir, self.data_filename), self.data_filename], stderr=sys.stdout)
        subprocess.check_call(['gsutil', 'cp', os.path.join(self.data_dir, self.target_filename), self.target_filename], stderr=sys.stdout)    

    def load(self):
        self.data = pd.read_csv(self.data_filename).values
        self.target = pd.read_csv(self.target_filename).values
        self.target = target.reshape((self.target.size,))

    def train(self):
        self.dtrain = xgb.DMatrix(iris_data, label=iris_target) # Load data into DMatrix object
        self.bst = xgb.train({}, dtrain, 20)                         # Train XGBoost model

    def save(self):
        self.bst.save_model(MODEL_FILENAME)

    def upload(self):
        gcs_model_path = os.path.join('gs://',  self.staging_bucket,
        datetime.datetime.now().strftime('iris_%Y%m%d_%H%M%S'), MODEL_FILENAME)
        subprocess.check_call(['gsutil', 'cp', MODEL_FILENAME, gcs_model_path], stderr=sys.stdout)