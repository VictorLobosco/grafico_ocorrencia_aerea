# Grafico_ocorrencia_aerea.

A simple Flask and chart.js project to allow visualization of the Brazillian airfoce data in chart form.

#How it works.

This project is divided in 3 smaller projects.

- db (Pandas + SQLALCHEMY with psycopg2) 
- api (FLASK(CORS + Marshmallow) + SQLALCHEMY with psycopg2)
- chart (Backend:FLASK(CORS), Frontend: Bootstrap, Jquery, Chart.js)

The project comes with an preconfigured postgres docker-compose file that you can you use to run the project.

#What you will need to run this project.

- Python.
- Posgtresql.

#How to run.

First either run the docker-compose file comes with the project or create your one local postgres server.

if you are using the docker database you should not have any problems running the rest of the project.

if you created your one, go to both the db folder and the api folder and change the adress of the server to the one you are using, you can also change the schema to the one you want to use.

After you got the server up and running go to the db folder and install the dependences needed for the project by running pip install requirements.txt,
after that run the main.py file, once you run it pandas will attempt to read the tables on the server, since you dont have them the project will download the dataset and create them, if you want to check for updates on the dataset all you need to do is run the file again and it will update the database with the new info.

Once you have the database populated go to the api folder and install its requirements like you did with db and run app.py.

Lastly go to the chart folder installs its requeriments and run app.py.

if you did everything correctly you should be able to go to: http://localhost:5005/
and build a chart with the tables of your choice.

#Objective

I wanted to try building a more modular project that relied on an API to achieve its main goal, in this project the api is the thing that feeds the info tho the chart giving more security to the databse as the user never interacts with the database directly, also the rest of the project is made of other smaller projects meaning that if i ever want to do a huge change on some parts of the project only that part needs to be edit, the rest of the project can stay the same.

I used an older project of mine back when i was learning pandas where i used this exact same dataset to construct some simple charts with matplotlib as inspiration for this one, this time around i wanted to allow the user to create a chart of their one.

#Future Goals.

**Project Structer:** I want all the parts of the project to run of its one container but i still want to add some features that will still need some changes in parts of the code so i will do that after implementing them

**Features:** In the project that used for inspiration for this one i had a chart that showed the months with the most amount of accidents in an given state, althout i already have an idea of how to implement this i still want to try improving the code befored adding-it. 
