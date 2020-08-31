import train_model
import subprocess
import os
import sys

if __name__ == "__main__":
    tm = train_model.train_model('gs://cloud-samples-data/ai-platform/iris/','iris_data.csv','iris_target.csv', 'ml-eng-model-staging' )
    subprocess.run(['gsutil', 'cp', 'gs://cloud-samples-data/ai-platform/iris/iris_data.csv', "C:\\Users\\hercheu\\Desktop\\git\\iris_data.csv"], check=True, stderr=sys.stdout)


