import datetime
import os
import subprocess
import sys
import pandas as pd
import xgboost as xgb
import argparse

MODEL_FILENAME= 'model.bst'

class model: 
    # Constructor 
    def __init__(self, data_dir, data_filename, target_filename, staging_bucket, staging_directory ):  
        self.data_dir=data_dir
        self.data_filename=data_filename
        self.target_filename=target_filename
        self.staging_bucket= staging_bucket
        self.staging_directory= staging_directory
    # To get name 
    def fetch(self):
        print( os.path.join(self.data_dir, self.data_filename) )
        subprocess.check_call(['gsutil', 'cp', os.path.join(self.data_dir, self.data_filename), self.data_filename], stderr=sys.stdout)
        subprocess.check_call(['gsutil', 'cp', os.path.join(self.data_dir, self.target_filename), self.target_filename], stderr=sys.stdout)    

    def load(self):
        self.data = pd.read_csv(self.data_filename).values
        self.target = pd.read_csv(self.target_filename).values
        self.target = self.target.reshape((self.target.size,))

    def train(self):
        self.dtrain = xgb.DMatrix(self.data, label=self.target)
        self.bst = xgb.train({}, self.dtrain, 20)

    def save(self):
        self.bst.save_model(MODEL_FILENAME)

    def upload(self):
        gcs_model_path = os.path.join('gs://',  self.staging_bucket, self.staging_directory , MODEL_FILENAME)
        subprocess.check_call(['gsutil', 'cp', MODEL_FILENAME, gcs_model_path], stderr=sys.stdout)
        
def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-d", "--input", help="gs://<bucketname>")
    parser.add_argument("-i", "--data", help="Your data set file")
    parser.add_argument("-i2", "--target", help="Your data target set file")
    parser.add_argument("-s", "--staging", help="gs://<bucketname>")
    parser.add_argument("-sd", "--stagedir", help="gs://<bucketname>/<your input>")
    options = parser.parse_args(args)
    return options

if __name__ == "__main__":
    options = getOptions(sys.argv[1:])
    tm = model.model(options.input,options.data, options.target, options.job-dir , options.stagedir )
    tm.fetch()
    tm.load()
    tm.train()
    tm.save()
    tm.upload()