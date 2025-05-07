# 🎧Data Engineering Project |Building Spotify ETL using Python and Airflow

Create an Extract Transform Load pipeline using python and automate with airflow.

![Screenshot 2025-05-05 223629](https://github.com/user-attachments/assets/2da73bdb-45d0-4117-b866-d467b9700e05)


# Tech Stack / Skill used:

1.  Python
2.  API’s
3.  Docker
4.  Airflow
5.  PostgreSQL


# Building ETL Pipeline:

**Dataset:** In this project, we are using Spotify’s API,we need the token

## Extract.py

We are using this token to Extract the Data from Spotify. We are Creating a function return_dataframe(). The Below python code explains how we extract API data and convert it to a Dataframe.

## Transform.py

Here we are exporting the Extract file to get the data.
Cleans and reshapes the data (e.g., renaming columns, formatting dates)

## Load.py

In the load step, we are using sqlalchemy and SQLite to load our data into a database and save the file in our project directory.

Finally, we have completed our ETL pipeline successfully. The structure of the project folder should look like this(inside the project folder we have 3 files)

![Screenshot 2025-05-07 170749](https://github.com/user-attachments/assets/bced09af-6caa-4c0b-b684-642790fc032b)

After running the  **Load.py**  you could see this: 

![Screenshot 2025-05-01 160610](https://github.com/user-attachments/assets/0309da12-6d91-4469-95da-352f77825266)

![yesssss](https://github.com/user-attachments/assets/8cc86ccf-6eb6-4e8e-95d5-7e0f2c44fe4d)

# Automating through Airflow

Now we are going to extend this with airflow using docker

![Screenshot 2025-05-07 171120](https://github.com/user-attachments/assets/36c72d3f-fb08-443c-9b38-79a730f1f9a6)

So inside our dag, we need to create tasks to get our job done. To keep it simple I will use two tasks i.e. one to create Postgres Table and another to load the Data to the Table our dag will look like this.

![Screenshot 2025-05-07 171300](https://github.com/user-attachments/assets/58b34dbe-7320-453d-954c-eee009b2d40d)

![Screenshot 2025-05-07 171406](https://github.com/user-attachments/assets/1e321030-edb5-49ac-b124-24715cf4966d)

## spotify_etl.py

In this Python File will write a logic to extract data from API → Do Quality Checks →Transform Data.

1.  **def spotify_etl()**  → Core function which returns the Data Frame to the DAG python file.
2.  This file needs to be placed inside the dags folder

## dag.py

This is the most important section you need to pay attention to. First, learn the basics about airflow DAG’s  [here](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)  it might take around 15 mins or you can search for it on youtube. After the basics please follow the below guideline.

1.  **from airflow.operators.python_operator import PythonOperator**  → we are using the python operator to perform python functions such as inserting DataFrame to the table.
2.  **from airflow.providers.postgres.operators.postgres import PostgresOperator**  → we are using the Postgres operator to create tables in our Postgres database.
3.  **from airflow. hooks.base_hook import BaseHook**  → A hook is an abstraction of a specific API that allows Airflow to interact with an external system. Hooks are built into many operators, but they can also be used directly in DAG code. We are using a hook here to connect Postgres Database from our python function
4.  **from spotify_etl import spotify_etl**  → Importing spotify_etl function from spotify_etl.py

![Screenshot 2025-05-07 171623](https://github.com/user-attachments/assets/b3bb5d4c-8c90-410a-8ba8-4721aec0c00a)


## Finally

![Screenshot 2025-05-07 171828](https://github.com/user-attachments/assets/dfb65dd9-be6c-4018-a872-c3c9781266ce)






