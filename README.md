# weather_alert
# setup

python3 -m venv env
pip install -r requirements.txt
cd app
python manage.py migrate
python manage.py makemigrations
python manage.py runserver 

# test

pytest

# Api Documentation

https://documenter.getpostman.com/view/11807094/UyxjF5ur

