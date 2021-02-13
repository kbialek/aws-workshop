# Prerequisites
## Install virtualenv
```shell
pip3 install virtualenv
pip3 install virtualenvwrapper
```

## Setup environment
```shell
source virtualenvwrapper.sh
mkvirtualenv aws-workshop-app
workon aws-workshop-app
mkdir app
cd app
pip3 install flask
pip3 install flask-sqlalchemy
pip3 install PyMySQL
pip3 install flask-login
pip3 install flask-migrate
pip3 freeze > requirements.txt

pip3 install -r requirements.txt
```

# Requests
```shell
curl localhost:5000/api/vehicles -XPOST -H'Content-Type: application/json' -d '{"brand":"Kia", "model":"Ceed", "year":2015}'
curl localhost:5000/api/vehicles -XPOST -H'Content-Type: application/json' -d '{"brand":"Fiat", "model":"Tipo", "year":2017}'

curl localhost:5000/api/vehicles -XGET -H'Accept: application/json' 

curl localhost:5000/api/vehicles/1 -XGET -H'Accept: application/json' 

curl localhost:5000/api/vehicles/1 -XPUT -H'Content-Type: application/json' -d '{"brand":"Kia", "model":"Ceed", "year":2016}'

####

echo '{"brand":"Kia", "model":"Ceed", "year":2015}' | http POST localhost:5000/api/vehicles
echo '{"brand":"Fiat", "model":"Tipo", "year":2017}' | http POST localhost:5000/api/vehicles

http localhost:5000/api/vehicles 

http localhost:5000/api/vehicles/1

echo '{"brand":"Kia", "model":"Ceed", "year":2016}' | http PUT localhost:5000/api/vehicles/1

```
