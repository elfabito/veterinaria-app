echo "BUILD START"

# Instala las dependencias del proyecto
python3.9 -m pip install -r requirements.txt

# Ejecuta las migraciones
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Recolecta los archivos estáticos
python manage.py collectstatic --noinput

echo "BUILD END"