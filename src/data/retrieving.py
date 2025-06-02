import os
import urllib.request

url = "https://datascientest-mlops.s3.eu-west-1.amazonaws.com/mlops_dvc_fr/raw.csv"
output_dir = "data/raw_data"
output_path = os.path.join(output_dir, "raw.csv")

os.makedirs(output_dir, exist_ok=True)
urllib.request.urlretrieve(url, output_path)
