# Grafico_ocorrencia_aerea.
![Gif](https://user-images.githubusercontent.com/87736256/208995021-035a9cf2-821c-4486-ba51-90796ac5e8ea.gif)

<!-- A simple Flask and chart.js project to allow visualization of the Brazilian airfoce data in chart form. -->
A data sourcing project that simulates the construction of a data visualization application based on open data from the Brazilian airfoce that allow anyone to generet charts using that data.

# Project Strutcture.

This project is divided in 3 smaller projects.

- db (Airflow + Pandas + SQLALCHEMY with psycopg2) 
- api (FLASK(CORS) + SQLALCHEMY with psycopg2)
- chart (Backend:FLASK(CORS), Frontend: Bootstrap, Jquery, Chart.js)

# How to run.

if you prefere a video tutorial you can watch one here:

[<img src="https://i.ytimg.com/vi/fYejLcLEQT0/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=fYejLcLEQT0 "Video Tutorial")

- DB:
First run docker compose up on the db folder, this will create the airflow containers and the postgres db container, all of them run in the same network named "ocorrencia", its recomended to have the project file extract in the same partition as your OS in a folder that has write permission as airflow creates a log after each run, and if it fails to do that it will not be able to run.
after all the containers are up, open you browser of preference and acess http://localhost:8080/, log-in using airflow for both username and password, after login in find the dag_ocorrencia on the Dag list and activate the switch on the left, after that the dag should run automatically, if it dosent start automatically simply press the play button on right side of the screen.

- API:
After the database is created go to the api folder and run docker compose up, if you want to make sure the api is working justo acess http://172.21.0.7:5000/db_info/ and you should be able to see all the tables and columns returned in json form.

- Chart
Lastly go the chart folder and run docker compose up, after the container is up you can create a chart of you preference by acessing http://172.21.0.8:5000.


# How it works.
The ideia behind this project is to create an data sourcing backend that will be used to feed an data visualization tool in order to create a chart to help visualize the data at hand.

The data in question is a series of of 5 datasets disponibilized by the brazillin airforce about air accidents occurred on the country, i used pandas to clean the data a bit and then created a database table with each of the datasets.

To make sure the dataset is always up to date i am relaying on airflow to schedule the run of the script that both creates and updates the dataset, the script is runned on a daily bases and it checks the md5 hash of the newest dataset availbe and if its different then the last one used to create the databaset.
The update process works by creating a dataframe with the newest dataset and creating one with the data on the db and then removing primary keys from each entry from the new dataset who exist in both the db and the new dataset and then upload what is left to the db, this way removing any info that is already in the db so as to not create duplicate data.

I am using an Flask API to comunicate between an application and the database to allow for more flexibility when it comes to what tools to you use to visualize the data, The api gives 3 simple endpoints one giving a list of all the tables and its columns and the other return the data of a specific column on a specific table and one that allows you to do a WHERE query with a count statement.

And i am using a chart js based solution to display the data and allow for the creation of charts.

# Details.

---------------------

<img src="https://user-images.githubusercontent.com/87736256/208761583-e6ba3b01-0557-4169-8fe1-df228a58dc69.jpeg" width="50%" height="50%" />


**DB**: This project is mainly centers around using airflow to control the execution of an dag that creates or updates the database, the dag is runned on daily basis and is compose of 4 task:
* check_for_update:
    Type: BranchPythonOperator
    Description: First download one of the csvs and creates an MD5 hash of the file and then it compares it to the hash of the last csv used to create or update
    the database if the hash is the same it means that there are no updates to the dataset and theres no need to update and the task up_to_date is called, if it is different then is assumed that the db is outdate and then the branch operator changes the task to write_on_db
* up_to_date:
    Type: DummyOperator
    Description: Simple DummyOperator to ilustrate that the db is up to date, after its execution the task done is called.

* writes_db:
    Type: PythonOperator
    Description: This is the task that do most of the work of the project it handles downloading cleaning and then uploads the data to a database, it does that by first creating a pandas dataframe with each of the 5 files that compose the dataset and then cleaning up and if its creating the database it proceeds to create a table for each of the files that compose the datase on the database,
    if the code is updating an existing database it then creates a dataframe using each of the tables correlated to its csv counterparts, it then procedes from deleting from dataframe created with the updated dataset all the data belonging to an primary key that is already in the database, this way creating a dataframe that only contains new data, after that thoses dataframes
    are uploaded on the database to its respectives tables.

* done:
    Type: DummyOperator
    Description: This task is always executed if there no problem on the task before, this only exists to signal the end dag


---------------------

<img src="https://user-images.githubusercontent.com/87736256/208763923-b9a5fe8b-78c7-40b0-9d56-0253f5d12dc4.png" width="30%" height="30%" />



**API**:
Api that handles all the comunication between the database and the user, this is a important part of the project as it allows for a greater mudularity of the project allowing to use the info on the database with data visualization tools other than the one sent with this project.
-- Endpoints:

* /v1/data/query/structure/:
  Parameters: None
  Description: Return all the tables and its columns only excluind its keys.

* /v1/data/query/column/: 
  Parameters: 'table', 'column', and 'sort'
  Description: Return info from a given colum by sending both the table and column as parameters, you can also chose between the data being order by descending by sending 'sort' = 1 as a parameters.
  Example: By sending a query with the parameters 'table' = "ocorrencia", 'column' = "ocorrencia_uf", you can get the amount of air crash per state in total.

* /v1/data/query/where/:
  Parameters: 'table', 'column', 'tableWhere', 'columWhere', 'equalTo' and 'sort'
  Description:  This endpoint return a query based on 2 columns that can be either from the same table or a join between two tables that are filter by the parameters equalTo, you can also chose between the data being order by descending by sending 'sort' = 1 as a parameters
  Example: By sending a query with the parameters 'table' = "aeronave", 'column' = "aeronave_tipo_veiculo", 'tableWhere' = "ocorrencia", 'columWhere' = "ocorrencia_uf" and 'equalTo' = "RJ", you will get the info about the type of vehicles and the amount of them that have being in a air crash in the state of Rio de Janeiro, you can also get this info in a descending order by sending 'sort' = 1.

---------------------

<img src="https://user-images.githubusercontent.com/87736256/208772226-0cd8f760-bd72-4e91-bb86-15754b66efd4.png" width="50%" height="50%" />


**Chart**:
A basic visualization tool hosted on flask using chart js to allow the creation of a chart based on one or more tables of the database.

-- Endpoints:

* / :
  Description: Main page of the project, all the code runs on this, it creates a chart by using the info return from the api, you can either create a chart with a single table chosing the table and the column and cliking on the generate button, or creating a more complxe chart by clicking on the complex button chosing table and columns and then clicking on the generate button.
  
 ---------------------
