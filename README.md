Setup and activation of virtualenv (env that prevents python packages from being installed globaly on the machine)
pip3 install virtualenv
python3 -m venv <name of virtual environment>
source env/bin/activate (activates the virtual environment with name 'env')

Migrate database
python manage.py migrate

Create superuser
Create a local admin user by entering the following command:
python manage.py createsuperuser
Only username and password is required

Start the app
python manage.py runserver
If this doesn't work, check that you have activated the virtual environment (source env/bin/activate) or specify the python version (write python3 instead of just python)