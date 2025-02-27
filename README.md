# PROJ0021-1 - Data Science Project

## Preparation
1. Download the dataset by running:  
   ```sh
   python dataset_downloader.py
   ```
2. Compress the dataset by running:  
   ```sh
   python dataset_compress.py
   ```

## Installation
1. Navigate to the project folder.
2. Run the following command to build and start the Docker container:  
   ```sh
   docker-compose up --build -d
   ```
3. Ensure the Docker container is running and contains the `init.sql` script.
4. Set up the database by running the `import_db.ipynb` notebook and wait for it to complete.

## Connexion into pgAdmin
1. Open your browser and go to:  
   ```
   http://localhost:5050
   ```
2. Use the following credentials:
   - **Email:** `a@a.com`
   - **Password:** `a`

### Add the database into pgAdmin
1. Click on **"Add New Server"**.
2. Go to the **Connection** tab and enter the following details:
   ```
   Host name/address: localhost
   Port: 5432
   Maintenance Database: postgres
   Username: postgres
   Password: postgres
   ```
3. Click **Save** to connect.

## Documentation

The main part of Exploratory Data Analysis is done in those two files
- `eda.ipynb` : Exploratory Data Analysis for everything related to trains.
- `eda_meteo.ipynb` : Exploratory Data Analysis for only the weather.

Files listed here are for setup purposes
- `download_dataset.py` : Simple file that will scrape the dataset using every link found in dataset.csv
- `compress_dataset.py`: The compression of the dataset is done by converting most of the string by int using maps, in order to decrease the size of the dataset.
- `add_regions.ipynb` : This file is used to map the stations to their respective regions, along with the longitude and latitude of each station and store it in the file better_station.csv
- `date.ipynb` : This file will check for each day if they are either a day of the week, a week-end day a school holiday or a national holiday
- `init.sql` : SQL script to initialise tables in the database
- `meteo.ipynb` : This file scrapes the meteo for each region using the open-meteo api
- `import_db.ipynb` : Import every csv file into their respective table in the database.


## Authors
- Hormat Saïd
- Yang Lei
- Houyon Manuel