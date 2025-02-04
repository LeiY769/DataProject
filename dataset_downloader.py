import os
import requests
import pandas as pd

df_links = pd.read_csv('dataset.csv', sep=';')

# Create a folder to store the dataset
DOWNLOAD_FOLDER = 'dataset'
os.makedirs('dataset', exist_ok=True)

for index, row in df_links.iterrows():
    url = row['Lien vers les données']
    filename = os.path.join(DOWNLOAD_FOLDER, url.split("/")[-1])
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

