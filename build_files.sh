echo "BUILD START"



# collect static files using the Python interpreter from venv

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
echo "BUILD END"