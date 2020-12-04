# Les fruits du Baobab

This is the code for [lesfruitsdubaobab.ca](lesfruitsdubaobab.ca)'s website's API.

### About the website
Check out [https://github.com/Baobab-team/baobab-client](https://github.com/Baobab-team/baobab-client)


#### Why Open source?
THe idea is to build a strong community. Quite often projects like these fail, 
but with open source everything is transparent and everybody is welcome to contribute. So it increase the 
likelihood that the project stays alive for a long period with the help of its 
multiple contributors.
If you have any questions, [let us know](mailto:contact@lesfruitsdubaobab.ca?Subject=Github520question).


#### Setup
Install virtual environment
```
python3 -m pip install --user virtualenv # Linux, MacOS
py -m pip install --user virtualenv # Windoes

python3 -m venv env # Linux, MacOS 
py -m venv env # Windows
```
Activate the virtual environment
```
source venv/bin/activate
```
Install the requirements
```
pip install requirements.txt
```
Create your local .env file.
[Generate a secret key](https://djecrety.ir) 
```
echo "SECRET_KEY=<<YOUR SECRET KEY>>" >> .env" 
```
Run the database migrations
```
python manage.py migrate
```
Run the project
```
python manage.py runserver
```

### Libraries
* [Django](https://www.djangoproject.com)
* [Django Rest framework](http://django-rest-framework.org)
* For the others, check out [requirements.txt](requirements.txt)
