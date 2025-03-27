from kaggle.api.kaggle_api_extended import KaggleApi
import os

os.makedirs("data", exist_ok=True)
api = KaggleApi(); api.authenticate()
api.dataset_download_files(
    "naveenkumar20bps1137/predict-students-dropout-and-academic-success",
    path="data",
    unzip=True
)
print("Done — files in data/")
