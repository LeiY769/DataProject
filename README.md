# PROJ0021-1 - Data Science Project

## Preparation
1. Download the dataset by running:  
   ```sh
   python dataset_downloadey.py
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


## Authors
Said, Lei and Manu