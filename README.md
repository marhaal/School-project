# Shareboi

## Local setup

### Requirements
* Make sure to have installed python3
* install pillow (for images) using the command: pip3 install Pillow
* install the rest of the requirements using the command: pip install -r requirements.txt

### Setup og activation of virtual environment - pprevents python packages from being installed globaly on the machine
* pip3 install virtualenv
* python3 -m venv <name of virtual environment>
* source env/bin/activate (activates the virtual environment with name 'env')

### Migrate database
* python manage.py migrate

### Create admin/superuser
* Create a local admin user by entering the following command:
* python manage.py createsuperuser
* Only username and password is required

### Initiate the application
* python manage.py runserver
* If this doesn't work, check that you have activated the virtual environment (source env/bin/activate) or specify the python version (write python3 instead of just python)
