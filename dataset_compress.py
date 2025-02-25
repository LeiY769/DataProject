#The compression of the dataset is done by converting most of the string by int using maps, in order to decrease the size of the dataset.
#The column relation-direction is also split into start and end in order to facilitate later analysis.

import pandas as pd
import numpy as np
import os
import sys
import sqlalchemy as sqla
import csv

RELATION_FILE = "RELATION.csv"
STATION_FILE = "UNIQUE_STATION.csv"
TRAIN_SERV_FILE = "TRAIN_SERV.csv"

DATASET_DIR = "dataset"
DATASET_FILES = os.listdir(DATASET_DIR)

# Columns that contain dates to be converted to datetime
DATE_COLUMNS = ["DATDEP"]

# Columns in common across all datasets
COMMON_COLUMNS = ['DATDEP', 'TRAIN_NO', 'RELATION', 'TRAIN_SERV', 'PTCAR_NO',
       'LINE_NO_DEP', 'REAL_TIME_ARR', 'REAL_TIME_DEP', 'PLANNED_TIME_ARR',
       'PLANNED_TIME_DEP', 'DELAY_ARR', 'DELAY_DEP', 'PTCAR_LG_NM_NL',
       'LINE_NO_ARR', 'RELATION_DIRECTION']

# Mapping to rename columns to match the database
mapping = {
    "DATDEP" : "departure_date"  ,
    "TRAIN_NO" : "train_number" ,
    "RELATION" : "relation" ,
    "TRAIN_SERV" : "train_service" ,
    "PTCAR_NO" :  "ptcar_number",
    "LINE_NO_DEP" : "line_number_departure" ,
    "REAL_TIME_ARR" : "real_time_arrival" ,
    "REAL_TIME_DEP" : "real_time_departure" ,
    "PLANNED_TIME_ARR" : "planned_time_arrival" ,
    "PLANNED_TIME_DEP" : "planned_time_departure" ,
    "DELAY_ARR" : "delay_arrival" ,
    "DELAY_DEP" : "delay_departure" ,
    "PTCAR_LG_NM_NL" : "ptcar_name" ,
    "LINE_NO_ARR" : "line_number_arrival" ,
    "START" : "station_departure" ,
    "END" : "station_arrival" 
}

if not os.path.exists(RELATION_FILE) or not os.path.exists(STATION_FILE) or not os.path.exists(TRAIN_SERV_FILE):
    RELATION = set()
    PTCAR_LG_NM_NL = set()
    TRAIN_SERV_TYPES = set()
    
    for file in DATASET_FILES:

        df = pd.read_csv("dataset/" + file, low_memory=False)
        #Relation
        unique_values = set(df["RELATION"].unique())
        RELATION.update(unique_values)

        #PTCAR_LG_NM_NL and RELATION_DIRECTION
        df["RELATION_DIRECTION"] = df["RELATION_DIRECTION"].fillna('')  # Fill NaN with an empty string
        df["RELATION_DIRECTION"] = df["RELATION_DIRECTION"].str.replace(r"^[^:]+:\s*", "", regex=True)
        split_df = df["RELATION_DIRECTION"].str.split(" -> ", expand=True, n=1)

        df["START"] = split_df[0].fillna('')  
        df["END"] = split_df[1].fillna('') if 1 in split_df else ''
        
        df.drop("RELATION_DIRECTION", axis=1, inplace=True)
        unique_values = set(df[['PTCAR_LG_NM_NL', 'START', 'END']].values.ravel()) #transform numpy into (ravel)1d array
        PTCAR_LG_NM_NL.update(unique_values)

        #TRAIN_SERV
        unique_values = set(df["TRAIN_SERV"].unique())
        TRAIN_SERV_TYPES.update(unique_values)

    RELATION = sorted([item for item in RELATION if isinstance(item, str)])
    INDEXED_RELATION = {name: idx for idx, name in enumerate(RELATION)}

    PTCAR_LG_NM_NL = sorted([item for item in PTCAR_LG_NM_NL if isinstance(item, str)])
    INDEXED_PTCAR_LG_NM_NL = {name: idx for idx, name in enumerate(PTCAR_LG_NM_NL)}

    TRAIN_SERV_TYPES = sorted([item for item in TRAIN_SERV_TYPES if isinstance(item, str)])
    INDEXED_TRAIN_SERV_TYPES = {name: idx for idx, name in enumerate(TRAIN_SERV_TYPES)}

    with open("RELATION.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "relation"]) 
        for key, value in INDEXED_RELATION.items():
            writer.writerow([value, key])

    with open("UNIQUE_STATION.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "station"]) 
        for key, value in INDEXED_PTCAR_LG_NM_NL.items():
            writer.writerow([value, key])

    with open("TRAIN_SERV.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "service"]) 
        for key, value in INDEXED_TRAIN_SERV_TYPES.items():
            writer.writerow([value, key])
else:
    relation_df = pd.read_csv(RELATION_FILE, index_col=1, keep_default_na=False)
    INDEXED_RELATION = relation_df["ID"].to_dict()
    #print(INDEXED_RELATION)

    stations_df = pd.read_csv(STATION_FILE, index_col=1, keep_default_na=False)
    INDEXED_PTCAR_LG_NM_NL = stations_df["ID"].to_dict()
    #print(INDEXED_PTCAR_LG_NM_NL)

    train_serv_df = pd.read_csv(TRAIN_SERV_FILE, index_col=1, keep_default_na=False)
    INDEXED_TRAIN_SERV_TYPES = train_serv_df["ID"].to_dict()
    #print(INDEXED_TRAIN_SERV_TYPES)

if not os.path.exists("cleaned_dataset"):
    os.mkdir("cleaned_dataset")

for file in DATASET_FILES:
    df = pd.read_csv(f"{DATASET_DIR}/{file}", low_memory=False, usecols=COMMON_COLUMNS)

    # We transform the date column to datetime
    for d in DATE_COLUMNS:
        df[d] = pd.to_datetime(df[d], format="%d%b%Y", errors="coerce")

    # We transform the categorical columns to integers which is a mapping of the unique values
    df["RELATION"] = df["RELATION"].map(INDEXED_RELATION)

    df["TRAIN_SERV"] = df["TRAIN_SERV"].map(INDEXED_TRAIN_SERV_TYPES)

    df["PTCAR_LG_NM_NL"] = df["PTCAR_LG_NM_NL"].map(INDEXED_PTCAR_LG_NM_NL)

    # We split the RELATION_DIRECTION column into START and END columns
    df["RELATION_DIRECTION"] = df["RELATION_DIRECTION"].fillna('')  # Fill NaN with an empty string
    df["RELATION_DIRECTION"] = df["RELATION_DIRECTION"].str.replace(r"^[^:]+:\s*", "", regex=True)
    split_df = df["RELATION_DIRECTION"].str.split(" -> ", expand=True, n=1)
    df["START"] = split_df[0].fillna('')  
    df["END"] = split_df[1].fillna('') if 1 in split_df else ''
    
    # We map them to integers which is a mapping of the unique values
    df["START"] = df["START"].map(INDEXED_PTCAR_LG_NM_NL)
    df["END"] = df["END"].map(INDEXED_PTCAR_LG_NM_NL)

    # Since RELATION_DIRECTION is now useless, we drop it
    df.drop("RELATION_DIRECTION", axis=1, inplace=True)

    df = df.rename(columns=mapping)

    # we ensure that all columns has their type
    df['relation'] = df['relation'].astype('Int64')
    
    df['delay_arrival'] = df['delay_arrival'].astype('float64')
    
    df['delay_departure'] = df['delay_departure'].astype('float64')
    
    df.to_csv(f"cleaned_dataset/{file}", index=False)
    print(f"Finished cleaning {file}")