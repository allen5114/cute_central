# cute_central

## Dependency Setup

https://realpython.com/python-dash/

## Create Python 3 virtual environment
````
# cd to repo
python -m venv venv

# on Windows
venv\Scripts\activate.bat

# on Linux
source venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip
````

## Install required libraries
````
# Install Dash, Dash bootsrap components, Google APIs Client Library for Python, gunicorn, etc
python -m pip install -r requirements.txt
````

## Run modes
````
// run in dev mode
python app_dev.py

// serve app via waitress in production mode
python app_prod.py
````