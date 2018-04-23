# Woodstock: a flask powered snooping facility

Assumes:
1. You have postgres installed 
2. Database called woodstock
3. User running the app have previliges to create/drop table on that db
4. database.py contains the connection string in case there is a need to change it
Also:
1. pipenv is used..install using pip3
2. run pipenv install and pipenv shell
3. run export FLASK_APP=woodstock.py; export FLASK_DEBUG=1; flask run
4. curl 127.0.0.1:5000/api/woodstock/list/5
