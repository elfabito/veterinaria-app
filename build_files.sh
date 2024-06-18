echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
python3.9 -m pip install pip

# pip install psycopg2-binary
# pip install python-dotenv

# pip install -r requirements.txt
pip install django
# collect static files using the Python interpreter from venv

python manage.py collectstatic --noinput

echo "BUILD END"