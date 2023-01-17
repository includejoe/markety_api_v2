
# Build the project
echo "Building project..."
python3.11.0 -m pip install -r requirements.txt

echo "Make Migration..."
python3.11.0 manage.py makemigrations --noinput
python3.11.0 manage.py migrate --noinput

echo "Collect Static..."
python3.11.0 manage.py collectstatic --noinput --clear